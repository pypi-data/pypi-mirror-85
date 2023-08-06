from hover.evaluation import (
    classification_accuracy,
    composite_accuracy,
    compute_on_df,
    agreement,
    agreement_matrix
)
from hover import module_params
import pandas as pd
import numpy as np


def test_classification_accuracy():
    true = np.array([0, 1, 1, 2])
    pred = np.array([0, 1, 2, 2])
    acc = classification_accuracy(true, pred)
    assert abs(acc - 0.75) < 1e-8


def test_compute_on_df():
    data = {"Acc": [0.9, 0.8, 0.7], "Cov": [0.2, 0.25, 0.3]}
    df = pd.DataFrame(data)
    df["CompAcc"] = compute_on_df({"accuracy": "Acc", "coverage": "Cov"})(
        composite_accuracy
    )(df)
    computed_values = df["CompAcc"].tolist()
    assert len(computed_values) == df.shape[0]


def test_agreement():
    ABSTAIN = module_params.ABSTAIN_ENCODED
    vec_u = np.array([ABSTAIN, 1, 2, 3, 4])
    vec_v = np.array([ABSTAIN, 1, 2, 0, 4])
    vec_w = np.array([0, 1, 2, 3, ABSTAIN])
    np.testing.assert_almost_equal(agreement(vec_u, vec_v), 0.50)
    np.testing.assert_almost_equal(agreement(vec_v, vec_w), 0.25)
    np.testing.assert_almost_equal(agreement(vec_w, vec_u), 0.75)

    mat = np.array([vec_u, vec_v, vec_w]).T
    agree_mat = agreement_matrix(mat)
    assert agree_mat.trace() == mat.shape[1]
    
