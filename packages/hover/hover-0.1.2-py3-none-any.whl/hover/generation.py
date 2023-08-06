"""
Submodule that handles the generation of rules and instantiations.
Generation recipes:
    text --[apply existing rule]--> (text, label)
    text --[apply SpaCy model]--> (text, label)
    (text, label) --[apply transformation]--> (another_text, label)
    A list of instantiations --[tf-idf analysis]--> rules based on keywords
    A list of instantiations --[embedding]--> rules based on high-dimensional vectors
    A list of instantiations --[tf-idf-lsa / count-lda]--> rules based on custom-dimensional vectors
    A list of instantiations --[tf-idf-lsa / count-lda -> t-SNE/UMAP]--> rules based on 2-dimensional manifolds
"""

import re
import numpy as np
import random
from abc import ABC, abstractmethod
from tqdm import tqdm
from hover.utils.snorkel_helper import labeling_function
from sklearn.feature_extraction.text import TfidfVectorizer
from hover import module_params

logger = module_params.default_logger()

def boltzmann_sample(
    candidates,
    scores,
    size,
    beta=1.0,
    replace=False,
    normalize=True,
    overflow_thresh=200.0,
):
    """
    Sample from a Boltzmann distribution where scores are equivalent to negative energies. Essentially softmax.
    :param candidates: list containing the candidates to sampled from.
    :type candidates: list
    :param scores: scores for each candidate.
    :type scores: list or numpy.array
    :param size: the number of samples to take.
    :type size: int
    :param beta: 'inverse temperature' in the Boltzmann ensemble.
    :type beta: float
    :param replace: whether to take replacement in sampling.
    :type beta: bool
    :param normalize: whether to normalize the scores to zero mean and unity standard deviation.
    :type normalize: bool
    :param overflow_thresh: threshold above which an exponent is considered to overflow.
    :type overflow_thresh: float
    """

    # ensure float data type and compute effective scores
    eff_scores = np.array(scores).astype(float)
    if normalize:
        eff_scores -= np.mean(eff_scores)
        std_dev = np.std(eff_scores)
        if std_dev > 1e-8:
            eff_scores /= std_dev
    eff_scores *= beta

    # precaution to handle numerical stability with exponents
    scale_down = np.amax(np.absolute(eff_scores)) / overflow_thresh
    if scale_down > 1.0:
        logger.warn(
            f"Numerical instability warning: about to raise an exponent to {scale_down*overflow_thresh} power. Now scaling down to {overflow_thresh}"
        )
        eff_scores /= scale_down

    prob = np.exp(eff_scores)
    prob /= prob.sum()

    return np.random.choice(candidates, size=size, replace=replace, p=prob)


def keyword_overlap(lower_text, keyword_list, threshold):
    """
    Boolean that determines whether a piece of text contains at least a certain number of given keywords. Excludes prefix and suffix.
    :param lower_text: text in lower case.
    :type lowet_text: str
    :param keyword_list: keywords to look for.
    :type keyword_list: list or str
    :param threshold: the number of distinct keywords required to be present.
    :type threshold: int

    :returns: bool -- whether the text has enough keyword instances.
    """
    count = 0
    for _keyword in keyword_list:
        if re.search(f"(^| ){_keyword}($| )", lower_text):
            count += 1
    return count >= threshold


def ellipse(vectors, x_center, y_center, x_radius, y_radius, tilt_angle):
    """
    Boolean that determines whether a collections of 2D vectors sit inside an ellipse that might be tilt (counter-clockwise) by an angle.
    :param vectors: x, y-coordinates of the vectors.
    :type vectors: numpy.array
    :param x_center: x-coordinate of the center of the ellipse.
    :type x_center: float or numpy.float
    :param y_center: y-coordinate of the center of the ellipse.
    :type y_center: float or numpy.float
    :param x_radius: radius of the ellipse in the x-direction before tilting.
    :type x_radius: float or numpy.float
    :param y_radius: radius of the ellipse in the y-direction before tilting.
    :type y_radius: float or numpy.float
    :param tilt_angle: the angle to rotate the ellipse counterclockwise in radians (instead of degree).
    :type tilt_angle: float or numpy.float

    :returns: numpy.array of bool -- whether each vector is in the ellipse.
    """

    assert x_radius > 0.0 and y_radius > 0.0
    # treat the single-vector case
    if vectors.ndim == 1:
        return ellipse(
            vectors[np.newaxis, :], x_center, y_center, x_radius, y_radius, tilt_angle
        )[0]

    assert vectors.ndim == 2
    shift = vectors - np.array([x_center, y_center])
    distance = np.linalg.norm(shift, axis=1)
    angle = np.arctan2(shift[:, 1], shift[:, 0])
    effective_angle = angle - tilt_angle
    effective_x = np.multiply(distance, np.cos(effective_angle))
    effective_y = np.multiply(distance, np.sin(effective_angle))
    return np.square(effective_x / x_radius) + np.square(effective_y / y_radius) <= 1.0


class LabelingFunctionGenerator(ABC):
    """
    Handles automatic creation of labeling functions.
    This is an abstract base class.
    """

    def __init__(self):
        self.logger = module_params.default_logger()

    @abstractmethod
    def _bio(*args, **kwargs):
        pass

    @abstractmethod
    def _get_param(*args, **kwargs):
        pass

    @abstractmethod
    def _mutate_param(*args, **kwargs):
        pass

    @abstractmethod
    def _build(*args, **kwargs):
        pass

    @abstractmethod
    def generate(*args, **kwargs):
        pass

    @abstractmethod
    def mutate(*args, **kwargs):
        pass


class TfidfLFG(LabelingFunctionGenerator):
    """
    Supervised labeling function.
    Uses the top TF-iDF words from each class.
    """

    def __init__(self, corpus, **kwargs):
        """
        Uses a corpus to compute document frequencies.
        :param corpus: a collection of text to fit the document frequency.
        :type corpus: list of str
        """
        super().__init__()
        self.vectorizer = TfidfVectorizer(**kwargs)
        self.vectorizer.fit(corpus)
        self.index_to_word = np.array(self.vectorizer.get_feature_names())

    @staticmethod
    def dataset_to_lfs(
        dataset,
        num_per_class=10,
        vectorizer_kwargs={"min_df": 5, "max_df": 0.1, "stop_words": "english"},
    ):
        """
        End-to-end generation from a hover Dataset to labeling functions.
        Intended for dynamically updated datasets.
        :param dataset: dataset to extract text from.
        :type dataset: hover.workflow.Dataset
        :param num_per_class: number of labeling functions to generate for each class.
        :type num_per_class: int
        :param vectorizer_kwargs: keyword parameters for sklearn's TfidfVectorizer.
        :type vectorizer_kwargs: dict

        :returns: list -- candidate labeling functions.
        """
        corpus = (
            dataset.dfs["train"]["text"].tolist() + dataset.dfs["dev"]["text"].tolist()
        )
        generator = TfidfLFG(corpus, **vectorizer_kwargs)
        lf_candidates = []
        for _target in dataset.classes:
            _subset = dataset.dfs["dev"][dataset.dfs["dev"]["label"] == _target][
                "text"
            ].tolist()
            lf_candidates += generator.generate(
                _subset, dataset.label_encoder[_target], dataset.label_decoder, num=num_per_class
            )
        return lf_candidates

    def _score_words(self, text_list):
        """
        Sort the words of a list of text, in TF-iDF descending order.
        :param text_list: a collection of text to compute TF-iDF.
        :type text_list: list of str

        :returns: list, list -- sorted keywords and scores.
        """
        feature_matrix = self.vectorizer.transform(text_list).toarray()
        reduced = np.mean(feature_matrix, axis=0)
        sort_indices = np.argsort(reduced)[::-1]
        sort_words = self.index_to_word[sort_indices].tolist()
        sort_scores = [reduced[_idx] for _idx in sort_indices]
        return sort_words, sort_scores

    def _bio(self, keyword_list, threshold, decoded_target):
        """
        Create a full logical description of a labeling function.
        :param keyword_list: keywords to look for.
        :type keyword_list: list or str
        :param threshold: the number of keywords required to show up.
        :type threshold: int
        :param decoded_target: the (decoded) label to apply when specified criterion is met.
        :type decoded_target: str

        :returns: dict -- a description of what the labeling function does.
        """
        return {
            "method": "keyword_overlap",
            "keyword_list": sorted(keyword_list),
            "threshold": threshold,
            "target": decoded_target,
        }

    def _get_param(
        self, sorted_words, sorted_scores, topk_range=(3, 20), beta_range=(0.5, 4.0)
    ):
        """
        Generate parameters for keyword-based rules, i.e. essentially extremely sparse linear classifiers based on TF-iDF. Uses noisy top-k via a Boltzmann distribution.
        :param sorted_words: a list of words in descending order.
        :type sorted_words: list of str
        :param sorted_scores: a list of scores, corresponding to words, in descending order.
        :type sorted_scores: list of float or numpy.float
        :param topk_range: the range of top-k values to sample from.
        :type topk_range: tuple (int, int)
        :param beta_range: the range of beta ("inverse temperature") values to sample from.
        :type beta_range: tuple (float, float)

        :returns: dict -- {callable: tuple} that holds functions and parameters.
        """
        topk = np.random.randint(*topk_range)
        assert topk > 0
        topk_words = boltzmann_sample(
            sorted_words,
            sorted_scores,
            topk,
            beta=np.random.uniform(*beta_range),
            replace=False,
        ).tolist()
        overlap_threshold = 1 + np.random.randint(0, topk // 3)

        return {keyword_overlap: (topk_words, overlap_threshold)}

    def _mutate_param(
        self, positional_param_dict, drop_word_prob=0.8, lower_thresh_prob=0.5
    ):
        """
        Mutate a parameter dict so that it produces a different labeling function.
        NOTE: this mutation is not ergodic as it will not increase the pool of keywords.
        :param positional_param_dict: dict holding the positional arguments to each function.
        :type positional_param_dict: dict {callable: tuple}
        :param drop_word_prob: probability to drop a word from the keyword list.
        :type drop_word_prob: float
        :param lower_thresh_prob: probability to lower the keyword threshold by 1.
        :type lower_thresh_prob: float

        :returns: dict -- mutated version of positional_param_dict.
        """
        # load parameters
        mutated_dict = positional_param_dict.copy()
        topk_words, overlap_threshold = mutated_dict[keyword_overlap]
        # perturb parameters; be careful with edge cases
        if len(topk_words) > 1 and np.random.uniform(0, 1) < drop_word_prob:
            topk_words.pop(np.random.randint(len(topk_words)))
        if overlap_threshold > 1 and np.random.uniform(0, 1) < lower_thresh_prob:
            overlap_threshold -= np.random.randint(0, 1)
        mutated_dict[keyword_overlap] = (topk_words, overlap_threshold)
        return mutated_dict

    def _build(self, positional_param_dict, target, label_decoder):
        """
        Build labeling function with supplied parameters.
        :param positional_param_dict: dict holding the positional arguments to each function.
        :type positional_param_dict: dict {callable: tuple}
        :param target: the label that the labeling function is intended to create.
        :type target: int
        :param label_decoder: {encoded_label -> decoded_label} mapping.
        :type label_decoder: dict

        :returns: Snorkel LabelingFunction -- labeling function.
        """

        @labeling_function([target], label_decoder)
        def generated_lf(x):
            return (
                target
                if keyword_overlap(
                    x.text.lower(), *positional_param_dict[keyword_overlap]
                )
                else module_params.ABSTAIN_ENCODED
            )
        
        generated_lf.name = str(generated_lf.uuid)
        generated_lf.param_dict = {
            keyword_overlap: positional_param_dict[keyword_overlap]
        }
        generated_lf.bio = self._bio(
            *(*positional_param_dict[keyword_overlap], label_decoder[target])
        )
        return generated_lf

    def generate(self, text_list, target, label_decoder, num=1):
        """
        End-to-end generation from a list of text to keyword-based rules.

        :param text_list: a collection of text to compute TF-iDF.
        :type text_list: list of str
        :param target: the (decoded) label to apply when specified criterion is met.
        :type target: int
        :param label_decoder: {encoded_label -> decoded_label} mapping.
        :type label_decoder: dict
        :param num: number of functions to produce.
        :type num: int

        :returns: generator -- labeling functions.
        """
        words, scores = self._score_words(text_list)

        def _generation_subroutine():
            _param_dict = self._get_param(words, scores)
            return self._build(
                _param_dict,
                target,
                label_decoder,
            )

        for i in range(num):
            yield _generation_subroutine()

    def mutate(self, lf, num=1):
        """
        End-to-end mutation from a labeling function that uses keyword overlap.
        :param lf: the labeling function to mutate from.
        :type lf: Snorkel LabelingFunction
        :param num: number of functions to produce.
        :type num: int

        :returns: generator -- labeling functions.
        """
        assert len(lf.targets) == 1
        def _mutation_subroutine():
            _param_dict = self._mutate_param(lf.param_dict)
            return self._build(
                _param_dict,
                lf.targets[0],
                lf.label_decoder,
            )

        for i in range(num):
            yield _mutation_subroutine()


class EllipseLFG(LabelingFunctionGenerator):
    """
    Supervised labeling function.
    Uses the 2D representation of data points from each class.
    """

    def __init__(self, vectors, labels, label_decoder):
        """
        Uses a corpus to compute document frequencies.
        :param vectors: N-by-2 array containing N 2-dimensional vectors.
        :type vectors: numpy.ndarray 
        :param labels: encoded labels that match the vectors.
        :type labels: list of int
        :param label_decoder: {encoded_label: decoded_label} mapping.
        :type label_decoder: dict
        """
        super().__init__()
        self.vectors = vectors
        self.labels = labels
        self.label_decoder = label_decoder
        self.x_std, self.y_std = np.std(self.vectors, axis=0)

    @staticmethod
    def dataset_to_lfs(
        dataset, num=10,
    ):
        """
        End-to-end generation from a hover Dataset to labeling functions.
        Intended for dynamically updated datasets.
        :param dataset: dataset to extract text from.
        :type dataset: hover.workflow.Dataset
        :param text_to_2d: precomputed {text->vector} mapping.
        :type text_to_2d: dict
        :param num: number of labeling functions to generate.
        :type num: int

        :returns: list -- candidate labeling functions.
        """
        df = dataset.dfs["dev"]
        labels = df[module_params.ENCODED_LABEL_KEY].tolist()
        vectors = np.array(df[["x", "y"]].values)

        generator = EllipseLFG(vectors, labels, dataset.label_decoder)
        lf_candidates = list(generator.generate(num=num))
        return lf_candidates

    def _ellipse_to_target(self, ellipse_params):
        """
        Determine a target label given the ellipse parameters.
        :param ellipse_params: x_center, y_center, x_radius, y_radius, tilt_angle
        :type ellipse_params: tuple
        """
        import random
        from collections import Counter

        mask = ellipse(self.vectors, *ellipse_params)
        labels_in_ellipse = [_label for i, _label in enumerate(self.labels) if mask[i]]
        labels_count = Counter(labels_in_ellipse)

        # when there's nothing in the ellipse, randomly pick a target
        if not labels_count:
            return random.choice(list(self.label_decoder.keys()))

        # pick a target using label population in the ellipse
        candidates, scores = list(labels_count.keys()), list(labels_count.values())
        target = boltzmann_sample(candidates, scores, size=1, beta=2.0)[0]
        return target

    def _bio(self, x_center, y_center, x_radius, y_radius, tilt_angle, decoded_target):
        """
        Create a full logical description of a labeling function.
        :param x_center: x-coordinate of the center of the ellipse.
        :type x_center: float or numpy.float
        :param y_center: y-coordinate of the center of the ellipse.
        :type y_center: float or numpy.float
        :param x_radius: radius of the ellipse in the x-direction before tilting.
        :type x_radius: float or numpy.float
        :param y_radius: radius of the ellipse in the y-direction before tilting.
        :type y_radius: float or numpy.float
        :param tilt_angle: the angle to rotate the ellipse counterclockwise in radius (instead of degree).
        :type tilt_angle: float
        :param decoded_target: the (decoded) label to apply when specified criterion is met.
        :type decoded_target: str

        :returns: dict -- a description of what the labeling function does.
        """
        return {
            "method": "ellipse",
            "x_center": float(x_center),
            "y_center": float(y_center),
            "x_radius": float(x_radius),
            "y_radius": float(y_radius),
            "tilt_angle": float(tilt_angle),
            "target": decoded_target,
        }

    def _get_param(self, x_radius_range=(0.01, 0.5), y_radius_range=(0.01, 0.5)):
        """
        Generate parameters for ellipse-based rules.
        :param x_radius_range: the range of x-radius proportional to std(x).
        :type x_radius_range: tuple (float, float)
        :param y_radius_range: the range of y-radius proportional to std(y).
        :type y_radius_range: tuple (float, float)

        :returns: dict -- {callable: tuple} that holds functions and parameters.
        """
        # choose a random point as the center of the ellipse
        x_center, y_center = self.vectors[np.random.choice(self.vectors.shape[0])]
        x_radius = np.random.uniform(*x_radius_range) * self.x_std
        y_radius = np.random.uniform(*y_radius_range) * self.y_std
        tilt_angle = np.random.uniform(-np.pi, np.pi)
        return {ellipse: (x_center, y_center, x_radius, y_radius, tilt_angle)}

    def _mutate_param(
        self,
        positional_param_dict,
        x_center_increment_range=(-0.1, 0.1),
        y_center_increment_range=(-0.1, 0.1),
        x_radius_scale_range=(-1.0, 1.0),
        y_radius_scale_range=(-1.0, 1.0),
        angle_increment_range=(-0.314, 0.314),
    ):
        """
        Mutate a parameter dict so that it produces a different labeling function.
        :param positional_param_dict: dict holding the positional arguments to each function.
        :type positional_param_dict: dict {callable: tuple}
        :param x_center_increment_range: the range of center displacement in x-coord, proportional to std(x)
        :type x_center_increment_range: tuple (float, float)
        :param y_center_increment_range: the range of center displacement in y-coord, proportional to std(y)
        :type y_center_increment_range: tuple (float, float)
        :param x_radius_scale_range: the log-range of x-radius proportional to the current radius.
        :type x_radius_scale_range: tuple (float, float)
        :param y_radius_scale_range: the log-range of y-radius proportional to the current radius.
        :type y_radius_scale_range: tuple (float, float)
        :param angle_increment_range: the range of angular shift in radians.
        :type angle_increment_range: tuple (float, float)

        :returns: dict -- mutated version of positional_param_dict.
        """
        # load parameters
        mutated_dict = positional_param_dict.copy()
        x_center, y_center, x_radius, y_radius, tilt_angle = mutated_dict[ellipse]
        # perturb parameters
        x_center += np.random.uniform(*x_center_increment_range) * self.x_std
        y_center += np.random.uniform(*y_center_increment_range) * self.y_std
        x_radius *= np.exp(np.random.uniform(*x_radius_scale_range))
        y_radius *= np.exp(np.random.uniform(*y_radius_scale_range))
        tilt_angle += np.random.uniform(*angle_increment_range)
        mutated_dict[ellipse] = (x_center, y_center, x_radius, y_radius, tilt_angle)
        return mutated_dict

    def _build(self, positional_param_dict, target, label_decoder):
        """
        Build labeling function with supplied parameters.
        :param positional_param_dict: dict holding the positional arguments to each function.
        :type positional_param_dict: dict {callable: tuple}
        :param target: the label that the labeling function is intended to create.
        :type target: int
        :param label_decoder: {encoded_label -> decoded_label} mapping.
        :type label_decoder: dict

        :returns: Snorkel LabelingFunction -- labeling function.
        """

        @labeling_function([target], label_decoder)
        def generated_lf(x):
            return (
                target
                if ellipse(np.array([x.x, x.y]), *positional_param_dict[ellipse])
                else module_params.ABSTAIN_ENCODED
            )

        generated_lf.name = str(generated_lf.uuid)
        generated_lf.param_dict = {ellipse: positional_param_dict[ellipse]}
        generated_lf.bio = self._bio(*(*positional_param_dict[ellipse], label_decoder[target]))
        return generated_lf

    def generate(self, num=1):
        """
        Generate ellipse-based rules.

        :param num: number of functions to produce.
        :type num: int

        :returns: generator -- labeling functions.
        """

        def _generation_subroutine():
            _param_dict = self._get_param()

            # use majority vote to choose a target in the ellipse
            target = self._ellipse_to_target(_param_dict[ellipse])

            return self._build(
                _param_dict,
                target,
                self.label_decoder,
            )

        for i in range(num):
            yield _generation_subroutine()

    def mutate(self, lf, num=1):
        """
        End-to-end mutation from a labeling function that uses ellipse.
        :param lf: the labeling function to mutate from.
        :type lf: Snorkel LabelingFunction
        :param num: number of functions to produce.
        :type num: int

        :returns: generator -- labeling functions.
        """
        assert len(lf.targets) == 1
        def _mutation_subroutine():
            _param_dict = self._mutate_param(lf.param_dict)
            return self._build(
                _param_dict,
                lf.targets[0],
                lf.label_decoder,
            )

        for i in range(num):
            yield _mutation_subroutine()
