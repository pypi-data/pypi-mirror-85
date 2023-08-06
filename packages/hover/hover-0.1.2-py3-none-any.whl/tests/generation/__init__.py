from hover.generation import (
    boltzmann_sample,
    keyword_overlap,
    ellipse,
    TfidfLFG,
    EllipseLFG,
)
import numpy as np


def test_boltzmann_sample():
    def unstable_subroutine():
        """
        A test where we expect an outcome with probability close but not equal to one.
        """
        candidates = ["apple", "banana", "citrus"]

        draw = boltzmann_sample(candidates, [1.0, 0.0, 0.0], size=1, beta=20).tolist()
        if draw != ["apple"]:
            return False

        draw = boltzmann_sample(
            candidates, [1.0, 0.0, 0.0], size=2, beta=20, replace=True
        ).tolist()
        if draw != ["apple", "apple"]:
            return False

        draw = boltzmann_sample(
            candidates, [2.0, 2.0, 0.0], size=2, beta=20, replace=False
        ).tolist()
        if sorted(draw) != ["apple", "banana"]:
            return False
        return True

    # exponentially decrease the probability to fail
    assert unstable_subroutine() or unstable_subroutine() or unstable_subroutine()


def test_keyword_overlap():
    assert keyword_overlap("hello", ["hello"], 1)
    assert keyword_overlap(" hello", ["hello"], 1)
    assert keyword_overlap("hello ", ["hello"], 1)
    assert keyword_overlap(" hello ", ["hello"], 1)
    assert keyword_overlap("hello hello hello", ["hello"], 1)
    assert not keyword_overlap("hello hello hello", ["hell"], 1)
    assert keyword_overlap("hello hell hello", ["hello", "hell"], 2)


def test_ellipse():
    expected = [
        # displacement
        ((np.array([1.8, 3.0]), 1.0, 3.0, 1.0, 1.0, 0.0), True),
        # skewed ellipse
        ((np.array([0.8, 0.0]), 0.0, 0.0, 1.0, 0.1, 0.0), True),
        # rotation
        ((np.array([0.8, 0.0]), 0.0, 0.0, 1.0, 0.1, np.pi / 2), False),
    ]

    for args, retval in expected:
        assert ellipse(*args) == retval

    # array form
    assert ellipse(np.array([[1.8, 0.0], [1.0, 0.9]]), 1.0, 0.0, 1.0, 1.0, 0.0).all()


def test_TfidfLFG(dataset_20ng, lfs_per_class=5):
    # refer to fixture
    dataset = dataset_20ng

    # create LF generator
    corpus = dataset.dfs["train"]["text"].tolist() + dataset.dfs["dev"]["text"].tolist()
    tfidf_kwargs = {"min_df": 5, "max_df": 0.1, "stop_words": "english"}
    generator = TfidfLFG(corpus, **tfidf_kwargs)

    # generate LFs
    lf_candidates = []
    for _class in dataset.classes:
        _subset = dataset.dfs["dev"][dataset.dfs["dev"]["label"] == _class][
            "text"
        ].tolist()
        assert len(_subset) > 0
        lf_candidates += generator.generate(
            _subset, dataset.label_encoder[_class], dataset.label_decoder, num=lfs_per_class
        )

    # check the number of generated LFs
    assert len(lf_candidates) == len(dataset.classes) * lfs_per_class

    # check that every LF is callable
    for _lf in lf_candidates:
        assert callable(_lf)


def test_EllipseLFG(vectors_with_labels_square2x2):
    vectors, labels = vectors_with_labels_square2x2
    label_decoder = {_label: f"label_{_label}" for _label in labels}
    generator = EllipseLFG(vectors, labels, label_decoder)

    lf_candidates = list(generator.generate(num=20))

    assert len(lf_candidates) == 20

    for _lf in lf_candidates:
        assert callable(_lf)
