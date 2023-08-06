from hover.proposal import metric_sort, entropy
import numpy as np


def test_metric_sort():
    candidates = ["apple", "banana", "citrus"]
    obj_func = lambda arr: [abs(value) for value in arr]
    obj_args = ([-3, 1, 2],)
    candidates_with_metric = metric_sort(candidates, obj_func, obj_args)
    expected = [("apple", 3), ("citrus", 2), ("banana", 1)]
    assert candidates_with_metric == expected


def test_entropy():
    certainty = np.array([1.0, 0.0, 0.0])
    less_certain = np.array([0.8, 0.1, 0.1])
    uniform = np.array([0.333, 0.333, 0.334])

    concat = np.array([certainty, less_certain, uniform])
    assert entropy(concat).shape == (3,)
    assert entropy(certainty) < entropy(less_certain) < entropy(uniform)
