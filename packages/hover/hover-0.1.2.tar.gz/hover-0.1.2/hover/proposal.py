"""
Submodule that handles the proposal of the next batch for annotation.
Specifically, given a list of candidates (which can be rules or instantiations),
their statistics, and an objective, choose a sublist accordingly.
"""
# consider as a diverse set of proposal schemes as one can.
# this helps diversity the rules and instantiations.

import numpy as np
import numba


def metric_sort(candidates, objective_function, obj_args, obj_kwargs={}, reverse=True):
    """
    To be deprecated because evaluating the objective function has nothing intrinsic to do with the candidates.
    """
    metrics = objective_function(*obj_args, **obj_kwargs)
    return multi_metric_sort(candidates, metrics, reverse=reverse)

def multi_metric_sort(candidates, *metrics, reverse=True):
    """
    Sort candidates (in descending order by default) based on one or more metrics in the order they are given.
    :param candidates: a list of candidates to be returned.
    :type candidates: list
    :param metrics: any sequence of lists containing calculated metric values.
    :type metrics: iterable of lists
    :param reverse: whether to sort in descending order.
    :type reverse: bool
    """
    ordered = sorted(
        list(zip(candidates, *metrics)),
        key=lambda t: tuple(t[i] for i in range(1, len(t))),
        reverse=reverse,
    )
    return ordered
    

def fitness_diversity(
    fitness, agreement, alpha=1.0, num_agreement_reference=5, offset_diagonal=True
):
    """
    score[i] = standard_fitness[i] - alpha * mean(subset_agreement[i, :])
    @param fitness: vector holding the 'fitness' score of N candidates.
    @param agreement: N by M array holding the agreement between N candidates and M references.
    @param alpha: weighting coefficient for diversity.
    @param num_agreement_reference: the number of highest agreement values to average over.
    @param offset_diagonal: set to True when the agreement array is symmetric, because a candidate's agreement with itself does not count.
    """
    from scipy.stats import zscore

    assert fitness.shape[0] == agreement.shape[0]
    if offset_diagonal:
        assert np.allclose(
            agreement, agreement.T
        ), "Instructed to offset diagonals on an asymmetric array."
        agreement = agreement[:] - 2.0 * np.identity(fitness.shape[0])
    num_agreement_reference = min(agreement.shape[1], num_agreement_reference)
    eff_agreement = np.sort(agreement, axis=1)[:, -num_agreement_reference:][:, ::-1]
    return zscore(fitness) - alpha * np.mean(eff_agreement, axis=1)


@numba.jit(nopython=True)
def entropy_arr(probability_array, normalize=True):
    """
    Subroutine called by entropy() that assumes a 2-D array.
    @param probability_array: N by K array holding N probability vectors of K outcomes.
    @param normalize: whether to enforce normalization in each vector.
    """
    if normalize:
        probability_array /= probability_array.sum(axis=1)
    contributions = -1.0 * np.multiply(
        probability_array, np.log2(probability_array + 1e-32)
    )
    return contributions.sum(axis=1)


def entropy(probability_array, normalize=True):
    """
    Calculates entropy using this formula:
        H(X) = -sum{x}{P(x)log_2[P(x)]}
    :param probability_array: NumPy array with 1 or 2 dimensions.
    :param normalize: whether to enforce normalization in each vector.
    """
    if probability_array.ndim == 1:
        return entropy_arr(
            probability_array[np.newaxis, :], normalize=normalize
        ).flatten()[0]
    elif probability_array.ndim == 2:
        return entropy_arr(probability_array, normalize=normalize)
    else:
        raise ValueError("Expected NumPy array with ndim 1 or 2")


def unit_scale_entropy(probability_array, normalize=True):
    """
    Calculate entropy and scale it linearly to between 0 and 1.
    This is achieved by scaling the max entropy possible to 1.
    """
    num_outcomes = probability_array.shape[-1]
    # the scale factor is computed from a uniform probability distribution
    scale_factor = entropy(np.array([1.0] * num_outcomes), normalize=True)
    return entropy(probability_array, normalize=normalize) / scale_factor
