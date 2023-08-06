"""
Submodule for a Prodigy-compliant transfer learning model along with a Prodigy recipe to use it.
"""

from __future__ import unicode_literals

import prodigy
from prodigy.components.loaders import JSONL
from prodigy.components.sorters import (
    prefer_uncertain,
    prefer_low_scores,
    prefer_high_scores,
)
import random
from copy import deepcopy
import torch
import torch.nn.functional as F
from hover.utils.torch_helper import vector_dataloader, one_hot, label_smoothing
from hover.evaluation import classification_accuracy
from hover.proposal import unit_scale_entropy
from hover.module_params import PRODIGY_KEY_TRANSFORM_PREFIX, default_logger
from sklearn.metrics import confusion_matrix
from snorkel.classification import cross_entropy_with_probs
import numpy as np
from hover.future.core.neural import TextVectorNet


class ProdigyTextVectorNet(TextVectorNet):
    """
    Prodigy flavor of the transfer learning model.
    Implements a __call__() method and a update() method for Prodigy.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cache_accepted = []
        self.cache_rejected = []
        self.base_batch_size = kwargs.get('batch_size', 4)
        self.base_update_threshold = kwargs.get('update_threshold', 16)
        assert self.base_update_threshold // self.base_batch_size >= 1, "Need at least one batch to prepare updates"
        assert self.base_update_threshold % self.base_batch_size == 0, "Whole batches are required to prevent bugs that may occur in custom architectures"

    def __call__(self, stream):
        """
        Generate examples for annotation. Accepts pre-computed overrides by a "proposed" dict.
        :param stream: generator of data entries managed by Prodigy in dictionary format.
        :type stream: iterable
        """
        for _eg in stream:
            _text = _eg.get("text", "")
            # if there is a precomputed override, pop it
            if f"{PRODIGY_KEY_TRANSFORM_PREFIX}proposed" in _eg:
                _proposed_dict = _eg.pop("proposed")
                _label = proposed_dict["label"]
                # attempt to decode the label if it is not already decoded
                _label = self.label_decoder.get(_label, _label)
                _score = proposed_dict["score"]
            else:
                # forward propagation to get class probabilities
                _probs = self.predict(_text).detach().numpy().flatten()

                # finalize label and score
                # the label is sampled rather than argmax so that unbalanced wrong predictions get less troublesome
                _encoded_label = np.random.choice(self.num_classes, p=_probs)
                _label = self.label_decoder[_encoded_label]
                # the score is an unit-scale entropy measure of the class probabilities, i.e. consistent regardless of the number of classes
                _score = unit_scale_entropy(_probs)
            _eg["label"] = _label
            yield (_score, _eg)

    def update(self, answers):
        """
        Update the model weights with the new answers. This method receives
        the examples with an added "answer" key that either maps to "accept",
        "reject" or "ignore".
        :param answers: iterable of Prodigy dicts.
        """
        # update with accepted answers
        self._update_accepted(answers)
        
        # update with rejected answers
        self._update_rejected(answers)
            
    def _update_subroutine(self, send_to_update, batch_size):
        """
        Low-level subroutine for training the active learning model given a list of dicts containing annotations.
        """
        input_vectors = [self.vectorizer(_d["text"]) for _d in send_to_update]
        output_labels = [self.label_encoder[_d["label"]] for _d in send_to_update]
        onehot_labels = one_hot(output_labels, num_classes=self.num_classes)
        output_vectors = label_smoothing(onehot_labels, num_classes=self.num_classes)
        train_loader = vector_dataloader(input_vectors, output_vectors, batch_size=batch_size)
        self.logger.info(
            f"Updating model on {len(send_to_update)} examples with batch size {batch_size}"
        )
        self.train(train_loader, verbose=1)
        self.save()
        
    def _update_accepted(self, answers):
        """
        Train the active learning model with accepted annotations.
        """
        accepted = [_d for _d in answers if _d["answer"] == "accept"]
        self.cache_accepted.extend(accepted)
        
        # if enough samples are present, update parameters
        update_threshold = self.base_update_threshold * 1
        batch_size = self.base_batch_size * 1
        
        num_ready_updates = len(self.cache_accepted) // update_threshold
        if num_ready_updates >= 1:
            update_split = update_threshold * num_ready_updates
            send_to_update = self.cache_accepted[:update_split]
            self.cache_accepted = self.cache_accepted[update_split:]
            self._update_subroutine(send_to_update, batch_size)
    
    def _update_rejected(self, answers):
        """
        Train the active learning model with rejected annotations.
        """
        rejected = [_d for _d in answers if _d["answer"] == "reject"]
        rej_converted = self._convert_rejected_for_training(rejected)
        self.cache_rejected.extend(rej_converted)
        
        # if enough samples are present, update parameters
        update_threshold = self.base_update_threshold * (self.num_classes - 1)
        batch_size = self.base_batch_size * (self.num_classes - 1)
        
        num_ready_updates = len(self.cache_rejected) // update_threshold
        if num_ready_updates >= 1:
            update_split = update_threshold * num_ready_updates
            send_to_update = self.cache_rejected[:update_split]
            self.cache_rejected = self.cache_rejected[update_split:]
            self._update_subroutine(send_to_update, batch_size)
        
    def _convert_rejected_for_training(self, rejected):
        '''
        Subroutine for _update_rejected() to utilize rejected annotations for training.
        '''
        converted = []
        for _rej_dict in rejected:
            _label = _rej_dict["label"]
            for _class in self.label_encoder.keys():
                # skip the rejected class
                if _class == _label:
                    continue
                # update to un-rejected class and append
                _acc_dict = deepcopy(_rej_dict)
                _acc_dict["label"] = _class
                converted.append(_acc_dict)
        return converted
