import pytest

def pytest_addoption(parser):
    parser.addoption(
        "--rundormant", action="store_true", default=False, help="run dormant tests"
    )


def pytest_configure(config):
    config.addinivalue_line("markers", "dormant: mark test as inactive by default")


def pytest_collection_modifyitems(config, items):
    if config.getoption("--rundormant"):
        # --rundormant given in cli: do not skip dormant tests
        return
    skip_dormant = pytest.mark.skip(reason="need --rundormant option to run")
    for item in items:
        if "dormant" in item.keywords:
            item.add_marker(skip_dormant)


@pytest.fixture(scope="module")
def dataset_20ng():
    from hover.utils.public_dataset import (
        newsgroups_dictl,
        newsgroups_reduced_dictl,
    )
    from hover.workflow import Dataset
    import pandas as pd

    my_20ng, label_encoder, label_decoder = newsgroups_reduced_dictl()
    train_dev_size = len(my_20ng["train"])
    split_idx = int(0.9 * train_dev_size)

    dataset = Dataset(
        train_dictl=my_20ng["train"][:split_idx],
        label_encoder=label_encoder,
        dev_dictl=my_20ng["train"][split_idx:],
        test_dictl=my_20ng["test"],
    )

    dataset.dfs["train"] = dataset.dfs["train"].drop(["label"], axis=1)
    dataset.synchronize_df_to_dictl()

    return dataset


@pytest.fixture(scope="module")
def vectors_with_labels_square2x2():
    import numpy as np

    arr = np.random.rand(1000, 2)
    discretized = np.around(arr)
    labels = discretized[:, 0] + discretized[:, 1] * 2
    labels = labels.astype(int).tolist()

    return arr, labels
