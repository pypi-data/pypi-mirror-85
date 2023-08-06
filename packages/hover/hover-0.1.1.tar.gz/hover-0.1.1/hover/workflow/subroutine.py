"""
Subroutines for the workflow module.
"""
from hover.evaluation import composite_accuracy, compute_on_df
from hover.proposal import metric_sort, fitness_diversity, entropy
import json


def get_composite_accuracy(analysis_result):
    burner_func = compute_on_df({"accuracy": "Emp. Acc.", "coverage": "Coverage"})(
        composite_accuracy
    )
    analysis_result["summary"]["Composite"] = burner_func(analysis_result["summary"])
    return analysis_result


def lf_string_representation(lf):
    """
    String representation of a labeling function using its bio.
    If a bio doesn't exist, use its UUID instead.
    """
    if hasattr(lf, 'bio'):
        return json.dumps(lf.bio, sort_keys=True, ensure_ascii=False)
    else:
        return str(lf.uuid)

def deduplicate_lfs(lfs, lookup_set=None):
    """
    Drop LF duplicates with optionally a specified lookup reference.
    :param lfs: labeling functions.
    :type lfs: list of Snorkel labeling functions
    :param lookup_set: set of string representation of LFs.
    :type lookup_set: set
    
    :returns: list -- LFs that are distinct according to the lookup set.
    """
    if lookup_set is None:
        lookup_set = set()

    unique_lfs = []
    for _lf in lfs:
        _rep = lf_string_representation(_lf)
        if not _rep in lookup_set:
            unique_lfs.append(_lf)
            lookup_set.add(_rep)
    return unique_lfs


def split_lfs_by_unique_target(lfs, seen_targets=None, threshold=1):
    """
    Pick out one LF (first in the list) for each unique target.
    :param lfs: labeling functions.
    :type lfs: list of Snorkel labeling functions
    :param seen_targets: {target: count} mapping.
    :type seen_targets: dict
    :param threshold: the number of LFs per target considered unique.
    :type threshold: int
    
    :returns: list, list -- LFs with unique targets, and LFs without.
    """
    from collections import Counter

    if seen_targets is None:
        seen_targets = Counter([])

    lfs_with_unique_target = []
    lfs_without_unique_target = []
    for _lf in lfs:
        selected = False
        for _target in _lf.targets:
            if seen_targets[_target] < threshold:
                selected = True
                break
        
        if selected:
            lfs_with_unique_target.append(_lf)
            for _target in _lf.targets:
                seen_targets[_target] += 1
        else:
            lfs_without_unique_target.append(_lf)
    return lfs_with_unique_target, lfs_without_unique_target


def default_candidate_ranking_function(lf_population):
    """
    Rank the candidates of a population of labeling functions.
    """
    lf_statistics = lf_population.statistics()
    num_candidates = lf_population.num_candidates()
    num_incumbents = lf_population.num_incumbents()

    # handle the no-candidate special case
    if num_candidates < 1:
        return []

    fitness_slice = lf_statistics["summary"]["Composite"].values[num_incumbents:]
    # if there are incumbents, use only them as agreement references
    if num_incumbents > 0:
        agreement_slice = lf_statistics["agreement"][num_incumbents:, :num_incumbents]
    else:
        agreement_slice = lf_statistics["agreement"][num_incumbents:, :]
    lf_candidates_with_metric = metric_sort(
        candidates=lf_population.candidates,
        objective_function=fitness_diversity,
        obj_args=(fitness_slice, agreement_slice),
        obj_kwargs={"offset_diagonal": False},
        reverse=True,
    )
    return lf_candidates_with_metric


def default_incumbent_ranking_function(lf_population):
    """
    Rank the incumbents of a population of labeling functions.
    """
    lf_statistics = lf_population.statistics()
    num_candidates = lf_population.num_candidates()
    num_incumbents = lf_population.num_incumbents()

    # handle the no-incumbent special case
    if num_incumbents < 1:
        return []

    fitness_slice = lf_statistics["summary"]["Composite"].values[:num_incumbents]
    agreement_slice = lf_statistics["agreement"][:num_incumbents, :num_incumbents]
    lf_incumbents_with_metric = metric_sort(
        candidates=lf_population.incumbents,
        objective_function=fitness_diversity,
        obj_args=(fitness_slice, agreement_slice),
        obj_kwargs={"offset_diagonal": True},
        reverse=True,
    )
    return lf_incumbents_with_metric
