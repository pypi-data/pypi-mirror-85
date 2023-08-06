"""
Submodule that handles the standard workflow, which features more automation and less flexibility.
"""
import numpy as np
import pandas as pd
from collections import Counter, defaultdict
from tqdm import tqdm
from hover import module_params
from hover.evaluation import (
    lf_analysis,
    lf_ensemble,
    compute_on_df,
    agreement_matrix,
    composite_accuracy,
)
from hover.proposal import metric_sort, fitness_diversity
from hover.future.core.neural import create_text_vector_net_from_module, TextVectorNet
from hover.utils.torch_helper import vector_dataloader, one_hot, label_smoothing
from hover.workflow.subroutine import (
    lf_string_representation,
    deduplicate_lfs,
    get_composite_accuracy,
    default_candidate_ranking_function,
    default_incumbent_ranking_function,
    split_lfs_by_unique_target,
)
from wrappy import probe, todo


class Dataset(object):
    """
    (raw_train, gold_dev, gold_test) dataset with two forms:
        -Pandas DataFrame for interaction with Snorkel;
        -list of dictionaries for interaction with Prodigy.
    During initialization, the dev set and test set are optional.
    The goal is to build
        -a size-effective gold set;
        -a batch-supervised, minimally noisy train set.
    """

    @todo("This class is deprecated and a new version is in hover.future.core.dataset")
    def __init__(
        self,
        train_dictl,
        label_encoder,
        dev_dictl=[],
        test_dictl=[],
        text_key="text",
        label_key="label",
    ):
        """
        Initialize the dataset with dictl and df forms; initialize the mapping between categorical-int and string labels.
        :param train_dictl: a list of dicts holding the raw train set that DO NOT have annotation.
        :param label_encoder: {'LABEL: A': 0, 'LABEL_B': 1, ...} dict holding the labels and their categorical representations.
        :param dev_dictl: a list of dicts holding the gold dev set.
        :param test_dictl: a list of dicts holding the gold test set.
        :param text_key: key in each piece of dict mapping to the text.
        :param label_key: key in each piece of dict mapping to the ground truth, which must be in label_encoder.keys().
        """
        key_transform = {text_key: "text", label_key: "label"}

        def dictl_transform(dictl):
            """
            Burner function to transform the input list of dictionaries into standard format.
            """
            return [
                {
                    key_transform.get(_key, _key): _value
                    for _key, _value in _dict.items()
                }
                for _dict in dictl
            ]

        self.logger = module_params.default_logger()
        self.dictls = {
            "train": dictl_transform(train_dictl),
            "dev": dictl_transform(dev_dictl),
            "test": dictl_transform(test_dictl),
        }

        self.label_encoder = label_encoder.copy()
        self.label_encoder[
            module_params.ABSTAIN_DECODED
        ] = module_params.ABSTAIN_ENCODED
        self.label_decoder = {
            _value: _key for _key, _value in self.label_encoder.items()
        }
        self.classes = [
            _class
            for _class in self.label_encoder.keys()
            if _class != module_params.ABSTAIN_DECODED
        ]
        self.synchronize_dictl_to_df()
        self.df_deduplicate()
        self.df_flush_annotations()
        self.synchronize_df_to_dictl()

    def df_flush_annotations(self, subset=["dev", "test"]):
        """
        Encode labels and set answer status of annotated data pieces.
        """
        for _key in subset:
            self.dfs[_key][module_params.ENCODED_LABEL_KEY] = self.dfs[_key][
                "label"
            ].apply(lambda x: self.label_encoder[x])
            self.dfs[_key]["answer"] = self.dfs[_key]["label"].apply(lambda x: "accept")

    def df_deduplicate(self, ordered_subset=["test", "dev", "train"]):
        """
        Cross-deduplicate data entries by text between subsets.
        :param ordered_subset: the subset and priority in descending order.
        :type ordered_subset: list of str in ["test", "dev", "train"]
        """
        self.logger.divider("Deduplicating dataset")
        # keep track of which df has which columns and which rows came from which subset
        columns = dict()
        for _key in ordered_subset:
            self.logger.info(
                f"--subset {_key} has {self.dfs[_key].shape[0]} entries before."
            )
            columns[_key] = self.dfs[_key].columns
            self.dfs[_key]["__subset"] = _key

        # concatenate in order and deduplicate
        overall_df = pd.concat(
            [self.dfs[_key] for _key in ordered_subset], axis=0, sort=False
        )
        overall_df.drop_duplicates(subset=["text"], keep="first", inplace=True)
        overall_df.reset_index(drop=True, inplace=True)

        # cut up slices
        for _key in ordered_subset:
            self.dfs[_key] = overall_df[overall_df["__subset"] == _key].reset_index(
                drop=True, inplace=False
            )[columns[_key]]
            self.logger.info(
                f"--subset {_key} has {self.dfs[_key].shape[0]} entries after."
            )
        self.logger.divider()

    def synchronize_dictl_to_df(self):
        """
        Re-make dataframes from lists of dictionaries.
        """
        self.dfs = dict()
        for _key, _dictl in self.dictls.items():
            self.dfs[_key] = pd.DataFrame(_dictl)

    def synchronize_df_to_dictl(self):
        """
        Re-make lists of dictionaries from dataframes.
        """
        self.dictls = dict()
        for _key, _df in self.dfs.items():
            self.dictls[_key] = _df.to_dict(orient="records")


class LabelingFunctionPopulation(object):
    """
    Group of labeling functions, divided into a 'candidate' pool and an 'incumbent' pool.
    """

    def __init__(self, candidates=[], incumbents=[], **kwargs):
        self.candidates = candidates
        self.incumbents = incumbents
        self.set_params(**kwargs)

    def set_params(self, min_lf_per_target=10):
        """
        Set parameters for the LF population.
        """
        self.min_lf_per_target = min_lf_per_target

    @property
    def candidates(self):
        return self.__candidates

    @property
    def incumbents(self):
        return self.__incumbents

    @candidates.setter
    def candidates(self, candidates):
        self.__candidates = candidates[:]
        self.__statistics_outdated = True

    @incumbents.setter
    def incumbents(self, incumbents):
        self.__incumbents = incumbents[:]
        self.__statistics_outdated = True

    def deduplicate(self):
        """
        Deduplicate LFs first among incumbents, then between incumbents and candidates.
        """
        self.incumbents = deduplicate_lfs(self.incumbents)
        self.candidates = deduplicate_lfs(
            self.candidates,
            lookup_set=set([lf_string_representation(_lf) for _lf in self.incumbents]),
        )

    def num_candidates(self):
        return len(self.__candidates)

    def num_incumbents(self):
        return len(self.__incumbents)

    def statistics(self, keep_keys=["summary", "agreement"]):
        """
        Read-only.
        """
        assert (
            not self.__statistics_outdated
        ), "Please re-run self.get_statistics() on a dataset"
        return {_key: self.__statistics[_key] for _key in keep_keys}

    def run_statistics(self, dataset, use_train=True, custom_functions=[]):
        """
        Compute and store LF statistics on a dataset.
        :param dataset: dataset to evaluate the label functions on.
        :type dataset: hover.workflow.Dataset
        :param use_train: whether to involve the train set in evaluation.
        :type use_train: bool
        :param custom_functions: functions that calculate custom statistics on a dataframe.
        :type custom_functions: list of callable
        """
        if not self.__statistics_outdated:
            return

        # determine whether the statistics should be calculated on the dev set only
        df_train = dataset.dfs["train"] if use_train else None
        agreement_key = "L_train" if use_train else "L_dev"

        # calculate statistics: LF empirical accuracy, coverage, and agreement
        temp_df_dev = dataset.dfs["dev"].copy()
        temp_df_dev[module_params.ENCODED_LABEL_KEY] = temp_df_dev["label"].apply(
            lambda x: dataset.label_encoder[x]
        )
        analysis_result = lf_analysis(
            self.__incumbents + self.__candidates,
            df_train=df_train,
            df_dev=temp_df_dev,
            label_column=module_params.ENCODED_LABEL_KEY,
        )
        for _func in [get_composite_accuracy] + custom_functions:
            analysis_result = _func(analysis_result)
        self.__statistics = analysis_result
        self.__statistics["agreement"] = agreement_matrix(
            self.__statistics[agreement_key]
        )
        self.__statistics_outdated = False

    def split_candidates(self, ranking_function, hire_ratio=0.2, drop_ratio=0.5):
        """
        Put candidates into three groups: suggested for hire, suggested to keep, and suggested to drop.
        :param ranking_function: takes self, and returns a sorted list of candidates with metrics.
        :type ranking_function: callable
        """
        import math

        assert hire_ratio + drop_ratio <= 1.0

        # rank candidates, ensuring that candidates with unique targets get selected regardless of ratios
        ranked_candidates = [_lf for _lf, _metric in ranking_function(self)]
        unique_candidates, ranked_candidates = split_lfs_by_unique_target(
            ranked_candidates, seen_targets=Counter([]), threshold=1
        )

        hire_end = math.ceil(hire_ratio * len(ranked_candidates))
        drop_start = len(ranked_candidates) - math.floor(
            drop_ratio * len(ranked_candidates)
        )
        return (
            unique_candidates + ranked_candidates[:hire_end],
            ranked_candidates[hire_end:drop_start],
            ranked_candidates[drop_start:],
        )

    def split_incumbents(self, ranking_function, keep_ratio=0.5, drop_ratio=0.2):
        """
        Put incumbents into three groups: suggested to keep, suggested to be put back to candidates, and suggested to drop.
        :param ranking_function: takes self and returns a sorted list of candidates with metrics.
        :type ranking_function: callable
        """
        import math

        assert keep_ratio + drop_ratio <= 1.0

        # rank incumbents, ensuring that incumbents with unique targets get kept regardless of ratios
        ranked_incumbents = [_lf for _lf, _metric in ranking_function(self)]
        unique_incumbents, ranked_incumbents = split_lfs_by_unique_target(
            ranked_incumbents,
            seen_targets=Counter([]),
            threshold=self.min_lf_per_target,
        )

        keep_end = math.ceil(keep_ratio * len(ranked_incumbents))
        drop_start = len(ranked_incumbents) - math.floor(
            drop_ratio * len(ranked_incumbents)
        )
        return (
            unique_incumbents + ranked_incumbents[:keep_end],
            ranked_incumbents[keep_end:drop_start],
            ranked_incumbents[drop_start:],
        )


class Automated(object):
    """
    End-to-end workflow where the only hands-on part is annotation in Prodigy.
    """

    def __init__(self, dataset, model_module_name):
        """
        Start an automated workflow with essential components only.
        :param dataset: workflow.Dataset object.
        :param model_module_name: path to save and load an in-the-loop model.
        """
        self.logger = module_params.default_logger()
        self.dataset = dataset
        self.model_module_name = model_module_name
        self.__addon_flags = defaultdict(lambda: False)

    @todo()
    def run(self, iterations=10):
        """
        Iteratively update the dataset, the active-learning model, and labeling functions.
        """
        self.update_dataset()

    def update_dataset(self, ratio_for_test_set=0.5):
        """
        Update the annotated dataset using active learning.
        """

        self.annotate_dataset()
        self.accumulate_dataset(ratio_for_test_set)

    def annotate_dataset(self):
        """
        Launch Prodigy for annotation on the train set.
        This is step 1/2 for updating the dataset.
        """
        from hover.annotation import CustomTextcatSession

        self.session = CustomTextcatSession(
            self.dataset.dictls["train"], "temp", "text"
        )
        self.session.serve(self.model_module_name, self.dataset.classes, drop=False)
        self.logger.good(
            f"Finished annotation with Prodigy. Run self.accumulate_dataset() if you haven't."
        )

    def accumulate_dataset(self, ratio_for_test_set=0.5):
        """
        Collect annotated examples from Prodigy.
        This is step 2/2 for updating the dataset.
        """
        import random

        annotated = self.session.collect(drop=True)

        # shuffle annotated data and split for dev/test sets
        random.shuffle(annotated)
        accepted = [_d for _d in annotated if _d["answer"] == "accept"]
        num_for_test = int(ratio_for_test_set * len(accepted))

        self.dataset.dictls["dev"] += accepted[num_for_test:]
        self.dataset.dictls["test"] += accepted[:num_for_test]

        # finalize changes in the df view and synchronize to the dictl view
        self.dataset.synchronize_dictl_to_df()
        self.dataset.df_deduplicate()
        self.dataset.df_flush_annotations()
        self.dataset.synchronize_df_to_dictl()
        self.logger.good(f"Finished dataset accumulation.")

    def noisy_train_set(self):
        """
        Apply Snorkel's weak supervision to the train set and estimate label probabilities.
        """
        assert self.__addon_flags["LF"], "No labeling function population set up"
        self.lf_population.run_statistics(self.dataset)
        columns_to_take = self.lf_population.num_incumbents()
        statistics = self.lf_population.statistics(keep_keys=["L_train", "L_dev"])
        probs_train, _ = lf_ensemble(
            L_train=statistics["L_train"][:, :columns_to_take],
            cardinality=len(self.dataset.classes),
            L_dev=statistics["L_dev"][:, :columns_to_take],
            y_dev=np.array(
                self.dataset.dfs["dev"][module_params.ENCODED_LABEL_KEY].tolist()
            ),
        )
        return self.dataset.dfs["train"]["text"].tolist(), probs_train

    def get_loader(self, key, vectorizer, smoothing_coeff=0.0):
        """
        Prepare a Torch Dataloader for training or evaluation.
        :param key: the subset of dataset to use.
        :type key: str
        :param vectorizer: callable that turns a string into a vector.
        :type vectorizer: callable
        :param smoothing_coeff: the smoothing coeffient for soft labels.
        :type smoothing_coeff: float
        """
        if key == "train":
            # the train set is typically large and noisy -- use larger batch size
            texts, output_vectors = self.noisy_train_set()
            batch_size = 64 if len(texts) > 1000 else min(16, len(texts))
        elif key in ["dev", "test"]:
            labels = (
                self.dataset.dfs[key]["label"]
                .apply(lambda x: self.dataset.label_encoder[x])
                .tolist()
            )
            texts = self.dataset.dfs[key]["text"].tolist()
            output_vectors = one_hot(labels, num_classes=len(self.dataset.classes))
            if key == "dev":
                # the dev set is typically small and clean -- use smaller batch size in case of training on it
                batch_size = 16 if len(texts) > 200 else min(4, len(texts))
            else:
                # for the test set, batch size doesn't quite matter unless there is a memory problem
                batch_size = 64
        else:
            raise KeyError(f"Invalid key: '{key}' for retrieving dataset")
        self.logger.info(f"Preparing input vectors...")
        input_vectors = [vectorizer(_text) for _text in tqdm(texts)]
        output_vectors = label_smoothing(
            output_vectors,
            num_classes=len(self.dataset.classes),
            coefficient=smoothing_coeff,
        )
        self.logger.info(f"Preparing data loader...")
        loader = vector_dataloader(input_vectors, output_vectors, batch_size=batch_size)
        self.logger.good(
            f"Prepared {key} loader consisting of {len(texts)} examples with batch size {batch_size}"
        )
        return loader

    def model_from_dev(self, **kwargs):
        """
        Train a Prodigy-compatible model from the dev set.
        """
        model = create_text_vector_net_from_module(
            TextVectorNet, self.model_module_name, self.dataset.classes
        )
        dev_loader = self.get_loader("dev", model.vectorizer, smoothing_coeff=0.1)
        train_info = model.train(dev_loader, dev_loader, **kwargs)
        return model, train_info

    def compute_text_to_2d(self, method, **kwargs):
        """
        Calculate a 2D manifold of the train/dev set.
        :param method: the dimensionality reduction method to use.
        :type method: str, "umap" or "ivis"
        """
        from hover.representation.reduction import DimensionalityReducer

        vectorizer = create_text_vector_net_from_module(
            TextVectorNet, self.model_module_name, self.dataset.classes
        ).vectorizer

        # prepare input vectors to manifold learning
        subset = ["raw", "train", "dev"]
        fit_texts = []
        for _key in subset:
            _df = self.dataset.dfs[_key]
            if _df.empty:
                continue
            fit_texts += _df["text"].tolist()
        fit_arr = np.array([vectorizer(_text) for _text in tqdm(fit_texts)])

        # initialize and fit manifold learning reducer
        reducer = DimensionalityReducer(fit_arr)
        embedding = reducer.fit_transform(method, **kwargs)

        # assign x and y coordinates to dataset
        start_idx = 0
        for _key in subset:
            _df = self.dataset.dfs[_key]
            _length = _df.shape[0]
            _df["x"] = pd.Series(embedding[start_idx : (start_idx + _length), 0])
            _df["y"] = pd.Series(embedding[start_idx : (start_idx + _length), 1])
            start_idx += _length

    def lf_activate(self, lf_population=None, *args, **kwargs):
        """
        Set up the labeling-function add-on utility.
        :param lf_population: workflow.LabelingFunctionPopulation object.
        """
        if lf_population:
            assert isinstance(
                lf_population, LabelingFunctionPopulation
            ), f"Expected LabelingFunctionPopulation, got {type(lf_population)}"
            self.lf_population = lf_population
        else:
            self.lf_population = LabelingFunctionPopulation(*args, **kwargs)
        self.__addon_flags["LF"] = True

    def model_from_lf(self, **kwargs):
        """
        Train a Prodigy-compatible model from the train set based on labeling functions.
        Can be useful for cold-starting a model when annotated data is limited.
        """
        assert self.__addon_flags["LF"], "No labeling function population set up"
        model = create_text_vector_net_from_module(
            TextVectorNet, self.model_module_name, self.dataset.classes
        )
        train_loader = self.get_loader("train", model.vectorizer, smoothing_coeff=0.01)
        dev_loader = self.get_loader("dev", model.vectorizer, smoothing_coeff=0.1)
        train_info = model.train(train_loader, dev_loader, **kwargs)
        return model, train_info

    def lf_rerank(self):
        """
        Score, split, and reorganize LF incumbents and candidates.
        """

        assert self.__addon_flags["LF"], "No labeling function population set up"
        self.logger.divider("Re-ranking labeling functions")
        prev_num_incu, prev_num_cand = (
            self.lf_population.num_incumbents(),
            self.lf_population.num_candidates(),
        )
        incu_to_incu, incu_to_cand, incu_to_drop = self.lf_population.split_incumbents(
            default_incumbent_ranking_function
        )
        cand_to_incu, cand_to_cand, cand_to_drop = self.lf_population.split_candidates(
            default_candidate_ranking_function
        )

        self.lf_population.incumbents = incu_to_incu + cand_to_incu
        self.lf_population.candidates = incu_to_cand + cand_to_cand
        num_incu_dup, num_cand_dup = (
            self.lf_population.num_incumbents(),
            self.lf_population.num_candidates(),
        )

        self.lf_population.deduplicate()
        num_incu, num_cand = (
            self.lf_population.num_incumbents(),
            self.lf_population.num_candidates(),
        )

        self.logger.good(
            f"Incumbents: {prev_num_incu}(prev) - {len(incu_to_cand)}(demoted) - {len(incu_to_drop)}(dropped) + {len(cand_to_incu)}(promoted) - {num_incu_dup - num_incu}(duplicate) = {num_incu}"
        )
        self.logger.good(
            f"Candidates: {prev_num_cand}(prev) - {len(cand_to_incu)}(promoted) - {len(cand_to_drop)}(dropped) + {len(incu_to_cand)}(demoted) - {num_cand_dup - num_cand}(duplicate) = {num_cand}"
        )

    def lf_refill(
        self, dataset_to_lfs, *args, metric_threshold=0.0, autoaccept=True, **kwargs
    ):
        """
        Get more LF candidates.
        :param dataset_to_lfs: function that takes a hover Dataset as an argument and returns a list of labeling functions.
        :type dataset_to_lfs: callable
        :param metric_threshold: threshold on the metric function that evaluates generated LF candidates.
        :type metric_threshold: float
        :param autoaccept: whether generated LFs get automatically accepted into candidates, i.e. without manual annotation.
        :type autoaccept: bool
        """
        from hover.annotation import LabelingFunctionSession

        assert self.__addon_flags["LF"], "No labeling function population set up"
        self.logger.divider("Refilling labeling functions")
        prev_num_cand = self.lf_population.num_candidates()
        raw_candidates = dataset_to_lfs(self.dataset, *args, **kwargs)

        # automated analysis that computes composite accuracy and agreement statistics on the dev set
        temp_df_dev = self.dataset.dfs["dev"].copy()
        temp_df_dev[module_params.ENCODED_LABEL_KEY] = temp_df_dev["label"].apply(
            lambda x: self.dataset.label_encoder[x]
        )
        analysis_result = lf_analysis(raw_candidates, df_train=None, df_dev=temp_df_dev)
        burner_func = compute_on_df({"accuracy": "Emp. Acc.", "coverage": "Coverage"})(
            composite_accuracy
        )
        analysis_result["summary"]["Composite"] = burner_func(
            analysis_result["summary"]
        )
        agreement_mat = agreement_matrix(analysis_result["L_dev"])
        ranked_candidates_with_metric = metric_sort(
            raw_candidates,
            fitness_diversity,
            (analysis_result["summary"]["Composite"].values, agreement_mat),
        )

        # keep a lookup table, then strip off labeling functions from metrics
        metric_lookup = {
            _lf.name: _metric for _lf, _metric in ranked_candidates_with_metric
        }
        ranked_candidates = [_lf for _lf, _metric in ranked_candidates_with_metric]

        # keep labeling function with unique targets from the metric filter
        unique_candidates, ranked_candidates = split_lfs_by_unique_target(
            ranked_candidates, seen_targets=Counter([]), threshold=3
        )

        # preliminary candidates are determined automatically
        prelim_candidates = unique_candidates + [
            _lf
            for _lf in ranked_candidates
            if metric_lookup[_lf.name] >= metric_threshold
        ]

        # manual accept/reject session, if specified
        if autoaccept:
            accepted_lfs = prelim_candidates
        else:
            from hover.annotation import LabelingFunctionSession

            sess = LabelingFunctionSession(prelim_candidates, "dummy")
            sess.serve(drop=True)
            accepted_lfs = sess.collect(drop=True)

        self.lf_population.candidates += accepted_lfs
        num_cand = self.lf_population.num_candidates()
        self.logger.good(
            f"Candidates: {prev_num_cand}(prev) + {len(accepted_lfs)}(accepted) = {num_cand}"
        )
