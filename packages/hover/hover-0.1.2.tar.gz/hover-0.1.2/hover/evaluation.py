"""
Submodule that handles evaluation of rules and instantiations.
Metrics:
    for rules:
        -accuracy: the percentage of gold instantiations that the rule gets right.
        -local accuracy: accuracy measured on a specific subset.
        -diversity: the distance, measured by prediction agreement, to its nearest gold rule.
    for instantiations:
        -confidence: probability predicted by a SpaCy model, or a Snorkel label model.
        -coverage: the number of labels that current set of rules is able to put.
"""

# make use of Snorkel to build metrics for rules.
# Snorkel has straightforward accuracy measure;
# Slicing function gives access to local accuracy;
# predictions easily lead to agreement measures.

# given a warmed-up model, Prodigy already handles confidence evaluation.
# however, one might want to filter by Snorkel's label model confidence too.

from hover import module_params
import numpy as np
import pandas as pd
import numba
import wasabi


def classification_accuracy(true, pred):
    """
    Accuracy measure on two arrays. Intended primarily for classification problems.
    :param true: true labels.
    :type true: Numpy array
    :param pred: predicted labels.
    :type pred: Numpy array
    """
    assert true.shape[0] == pred.shape[0]
    correct = np.equal(true, pred).sum()
    return float(correct) / float(true.shape[0])


def composite_accuracy(accuracy, coverage, acc_power=2):
    """
    When acc_power equals 2, this expression is equivalent to:
    (Portion of correct predictions out of all golds) * (Portion of correct predictions out of all predictions).
    """
    return (accuracy ** acc_power) * coverage


def compute_on_df(arg_mapping):
    """
    Usage example:
    Suppose df is a DataFrame returned by Snorkel's LFAnalysis().lf_summary() method.
    burner_func = compute_on_df({'accuracy': 'Emp. Acc.', 'coverage': 'Coverage'})(composite_accuracy)
    df['composite_accuracy'] = burner_func(df)
    """

    def wrapper(func):
        def wrapped(df):
            def burner(row):
                args = {_func_arg: row[_col] for _func_arg, _col in arg_mapping.items()}
                return func(**args)

            return df.apply(burner, axis=1)

        return wrapped

    return wrapper


@numba.jit(nopython=True)
def agreement(vec_u, vec_v, abstain=module_params.ABSTAIN_ENCODED):
    """
    "Categorical inner product" that element-wise yields 1 for agreement, -1 for disagreement, and 0 for abstain.
    Determine the agreement between vector u and vector v, according to the following rules:
    agreement = numerator / denominator
        numerator = positive - negative
            positive  = (# i WHERE vec_u[i] == vec_v[i] AND neither equals abstain)
            negative  = (# i WHERE vec_u[i] != vec_v[i] AND neither equals abstain)
        denominator = sqrt(# i WHERE vec_u[i] != abstain) * sqrt(# i WHERE vec_v[i] != abstain)
    """
    eff_u = np.not_equal(vec_u, abstain)
    eff_v = np.not_equal(vec_v, abstain)
    eff_uv = np.logical_and(eff_u, eff_v)
    positive = np.logical_and(np.equal(vec_u, vec_v), eff_uv).sum()
    negative = np.logical_and(np.not_equal(vec_u, vec_v), eff_uv).sum()
    denominator = np.sqrt(eff_u.sum() * eff_v.sum())

    # use small epsilon in case of division by zero
    return (positive - negative) / max(denominator, 1e-8)


@numba.jit(nopython=True)
def agreement_matrix(label_matrix, abstain=module_params.ABSTAIN_ENCODED):
    """
    Calls the agreement() subroutine to compute pair-wise agreements between labeling functions (or between data points, if the input matrix is transposed).
    @param label_matrix: 2-D array where:
        label_matrix[i, :] gives the outputs of the i-th data point.
        label_matrix[:, j] gives the outputs of the j-th labeling function.
    """
    dim = label_matrix.shape[1]
    mat = np.zeros((dim, dim))
    for j_u in range(0, dim):
        for j_v in range(j_u, dim):
            value = agreement(
                label_matrix[:, j_u], label_matrix[:, j_v], abstain=abstain
            )
            mat[j_u][j_v] = value
            mat[j_v][j_u] = value
    return mat


def lf_analysis(
    lfs,
    df_train=None,
    df_dev=None,
    label_column=module_params.ENCODED_LABEL_KEY,
    abstain=module_params.ABSTAIN_ENCODED,
):
    """
    Uses Snorkel to evaluate labeling functions.
    @param lfs: list of Snorkel labeling functions.
    @df_train: train-set df containing the "X", i.e. features that labeling functions require.
    @df_dev: dev-set df containing "X", as well as "y", i.e. categorically encoded labels.
    @label_column: the column name for the encoded label.
    @abstain: the encoded label corresponding to abstain.
    """
    from snorkel.labeling import PandasLFApplier, LFAnalysis

    assert df_train is not None or df_dev is not None
    applier = PandasLFApplier(lfs=lfs)

    if df_train is not None:
        L_train = applier.apply(df=df_train)
        coverage = (L_train != abstain).mean(axis=0)
    else:
        L_train = None
        coverage = None

    if df_dev is not None:
        L_dev = applier.apply(df=df_dev)
        y_dev = df_dev[label_column].to_numpy(copy=True)
        summary = LFAnalysis(L=L_dev, lfs=lfs).lf_summary(Y=y_dev)
        if coverage is not None:
            summary["Coverage"] = pd.Series(coverage.tolist(), index=summary.index)
    else:
        L_dev = None
        summary = None

    return {
        "L_train": L_train,
        "coverage": coverage,
        "L_dev": L_dev,
        "summary": summary,
    }


def lf_ensemble(
    L_train,
    cardinality,
    L_dev=None,
    y_dev=None,
    fit_kwargs={"n_epochs": 1000, "lr": 0.001, "seed": 0},
    majority_threshold=0.02,
):
    """
    Uses Snorkel's LabelModel to ensemble labeling function outputs.
    @param L_train: the output matrix of labeling functions on the train set.
    @param cardinality: the number of classes in the classfication.
    @param L_dev: the output matrix of labeling function on the dev set.
    @param y_dev: the label values on the dev set.
    @param fit_kwargs: keyword arguments for the LabelModel.fit() function.
    """
    from snorkel.labeling import LabelModel, MajorityLabelVoter

    logger = wasabi.Printer()

    with logger.loading("Fitting a label model..."):
        label_model = LabelModel(cardinality=cardinality, verbose=True)
        label_model.fit(L_train=L_train, **fit_kwargs)

    if not L_dev is None:
        majority_model = MajorityLabelVoter(cardinality=cardinality)
        assert y_dev.shape[0] == L_dev.shape[0]
        majority_acc = majority_model.score(L=L_dev, Y=y_dev)["accuracy"]
        lm_acc = label_model.score(L=L_dev, Y=y_dev)["accuracy"]
        logger.info(f"Evaluating on {y_dev.shape[0]} dev set examples:")
        logger.info(f"Label model acc = {lm_acc}")
        logger.info(f"Majority model acc = {majority_acc}")
        if lm_acc + majority_threshold < majority_acc:
            logger.info(
                f"Label model has inferior accuracy by more than {majority_threshold}"
            )
            logger.info(f"Switching to majority vote instead.")
            label_model = majority_model

    probs_train = label_model.predict_proba(L=L_train)
    return probs_train, label_model
