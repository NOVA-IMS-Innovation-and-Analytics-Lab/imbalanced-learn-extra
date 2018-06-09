"""
The :mod:`sklearnext.utils.validation` includes utilities
for input validation.
"""

# Author: Georgios Douzas <gdouzas@icloud.com>
# License: BSD 3 clause

from itertools import product
from sklearn.base import BaseEstimator
from sklearn.utils import check_random_state
from sklearn.model_selection._search import _check_param_grid


def _normalize_param_grid(param_grid):
    """Normalize the parameter grid to use with
    parametrized estimators."""
    _check_param_grid(param_grid)
    normalized_param_grid = param_grid.copy()
    est_name = list(set([param.split('__')[0] for param in param_grid.keys()]))
    normalized_param_grid.update({'est_name': est_name})
    return normalized_param_grid


def check_param_grids(param_grids, estimators):
    """Normalize the parameter grid to use with
    parametrized estimators."""
    if isinstance(param_grids, list):
        normalized_param_grids = []
        for param_grid in param_grids:
            normalized_param_grids.append(_normalize_param_grid(param_grid))
    else:
        normalized_param_grids = [_normalize_param_grid(param_grids)]
    est_names, _ = zip(*estimators)
    est_names = set(est_names)
    try:
        generated_est_names = set([param_grid['est_name'][0] for param_grid in normalized_param_grids])
    except IndexError:
        generated_est_names = set()
        normalized_param_grids = []
    for est_name in est_names.difference(generated_est_names):
        normalized_param_grids += [{'est_name': [est_name]}]
    return normalized_param_grids


def add_dataset_id(param_grids, num_datasets):
    """Add the dataset ids to param_grids."""
    products = product(param_grids, range(num_datasets))
    added_id_param_grids = []
    for param_grid, dataset_id in products:
        added_id_param_grid = param_grid.copy()
        added_id_param_grid.update({'dataset_id': [dataset_id]})
        added_id_param_grids.append(added_id_param_grid)
    return added_id_param_grids


def check_datasets(datasets):
    """Check that datasets is a list of (X,y) pairs or a dictionary of dataset-name:(X,y) pairs."""
    try:
        datasets_names = [dataset_name for dataset_name, _ in datasets]
        are_all_strings = all([isinstance(dataset_name, str) for dataset_name in datasets_names])
        are_unique = len(list(datasets_names)) == len(set(datasets_names))
        if are_all_strings and are_unique:
            return datasets
        else:
            raise ValueError("The datasets' names should be unique strings.")
    except:
        raise ValueError("The datasets should be a list of (dataset name:(X,y)) pairs.")


def check_random_states(random_state, repetitions):
    """Create random states for experiments."""
    random_state = check_random_state(random_state)
    return [random_state.randint(0, 2 ** 32 - 1, dtype='uint32') for _ in range(repetitions)]


def check_estimators(estimators):
    """Check estimators correct input."""
    error_msg = 'Invalid `estimators` attribute, `estimators` should be a list of (string, estimator) tuples.'
    try:
        if not all([all([isinstance(name, str), isinstance(est, BaseEstimator)]) for name, est in estimators]) or len(estimators) == 0:
            raise AttributeError(error_msg)
    except:
        raise AttributeError(error_msg)



