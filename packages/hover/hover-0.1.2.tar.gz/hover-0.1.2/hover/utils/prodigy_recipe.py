"""
Submodule for Prodigy custom recipes.
"""

from __future__ import unicode_literals

import prodigy
from prodigy.components.loaders import JSONL
from prodigy.components.sorters import (
    prefer_uncertain,
    prefer_low_scores,
    prefer_high_scores,
)
from hover.utils.prodigy_model import (
    ProdigyTextVectorNet,
    create_text_vector_net_from_module,
)

# Recipe decorator with argument annotations: (description, argument type,
# shortcut, type / converter function called on value before it's passed to
# the function). Descriptions are also shown when typing --help.
@prodigy.recipe(
    "lf.accept_reject",
    dataset=("The dataset to use", "positional", None, str),
    source=("The source data as a JSONL file", "positional", None, str),
)
def lf_accept_reject(dataset, source):
    """
    :param dataset: name of a Prodigy dataset.
    :type dataset: str
    :param source: jsonl source for Prodigy.
    :type source: str
    """
    stream = JSONL(source)

    def label_attacher(stream):
        """
        Process example to make it compatible with Prodigy's classification interface.
        """
        for _eg in stream:
            _eg["label"] = "VALID"
            yield _eg

    def no_update(answers):
        pass

    return {
        "view_id": "classification",  # Annotation interface to use
        "dataset": dataset,  # Name of dataset to save annotations
        "stream": label_attacher(stream),  # Incoming stream of examples
        "update": no_update,  # Update callback, called with batch of answers
        "config": {  # Additional config settings, mostly for app UI
            "label": ", ".join(["VALID"])
        },
    }


@prodigy.recipe(
    "textcat.text_vector_net",
    dataset=("The dataset to use", "positional", None, str),
    source=("The source data as a JSONL file", "positional", None, str),
    model_module_name=("Local module name holding the model", "positional", None, str),
    labels=("Labels for classification", "positional", None, list),
    selection_scheme=(
        "High, low, or medium in terms of entropy",
        "positional",
        None,
        str,
    ),
)
def textcat_text_vector_net(
    dataset, source, model_module_name, labels, selection_scheme="medium"
):
    """
    :param dataset: name of a Prodigy dataset.
    :type dataset: str
    :param source: jsonl source for Prodigy.
    :type source: str
    :param model_module_name: path to a local Python module in the working directory whose __init__.py file contains a get_text_to_vec() callable, get_architecture() callable, and a get_state_dict_path() callable.
    :type model_module_name: str
    :param labels: the classification labels, e.g. ["POSITIVE", "NEGATIVE"].
    :type labels: list of str
    :param selection_scheme: high, low, or medium entropy to prefer when selecting examples.
    :type selection_scheme: str in ['high', 'low', 'medium']
    """

    model = create_text_vector_net_from_module(
        ProdigyTextVectorNet, model_module_name, labels
    )

    # Load the stream from a JSONL file and return a generator that yields a
    # dictionary for each example in the data.
    stream = JSONL(source)

    # decide selection scheme and generate examples in a 'sorted' manner
    scheme_mapping = {
        "high": prefer_high_scores,
        "low": prefer_low_scores,
        "medium": prefer_uncertain,
    }
    scheme_function = scheme_mapping[selection_scheme]
    stream = scheme_function(model(stream))

    # The update method is called every time Prodigy receives new answers from
    # the web app. It can be used to update the model in the loop.
    update = model.update

    return {
        "view_id": "classification",  # Annotation interface to use
        "dataset": dataset,  # Name of dataset to save annotations
        "stream": stream,  # Incoming stream of examples
        "update": update,  # Update callback, called with batch of answers
        "config": {  # Additional config settings, mostly for app UI
            "label": ", ".join(labels)
        },
    }
