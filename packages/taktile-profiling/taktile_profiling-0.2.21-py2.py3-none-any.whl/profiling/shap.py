import math
from abc import ABC, abstractmethod
from functools import lru_cache, partial
from itertools import combinations

import numpy as np
import pandas as pd


@lru_cache(maxsize=256)
def n_choose_k(n, k):
    """Calculate binomial coefficient

    Numerical stable calculation with caching. Equivalent to:

    factorial(n) / factorial(k) / factorial(n - k)

    which has very large numerators and denominators.
    """
    coef = 1
    k = min(k, n - k)
    for x in range(1, k + 1):
        coef = coef * (n - k + x) // x
    return coef


comb = np.vectorize(
    n_choose_k,
    otypes=[int],
    doc="Vectorized version of 'n choose k', mimics scipy.special.comb",
)


def fast_object_mode(s):
    """Calculate mode of Series through intermediate string representation instead of hash table

    Parameters
    ----------
    s : pd.Series
        Pandas Series

    Returns
    -------
    Modal value
    """
    s_string = s.astype(str)
    _, indices, counts = np.unique(s_string, return_index=True, return_counts=True)
    index_max = indices[counts.argmax()]
    return s[index_max]


class Explainer(ABC):
    @abstractmethod
    def explain(self, X):
        raise NotImplementedError


def update_columns(base, update):
    """Update a base dataframe column-wise with a replacement dataframe

    Parameters
    ----------
    base : pd.DataFrame
        Base dataframe that will be updated
    update : pd.DataFrame
        Values to use when updating

    Returns
    -------
    pd.DataFrame
        Updated DataFrame where base-columns have been replaced with update-columns
    """
    base_columns = base.columns
    base = base.drop(columns=update.columns)
    if (len(base) == 1) & (len(update) > 1):  # numpy-style broadcasting
        base = pd.concat([base] * len(update), axis=0, ignore_index=True)
    base.index = update.index.copy()
    combined = pd.concat([base, update], axis=1)
    return combined.reindex(columns=base_columns)


def reduce_func(func, X):
    """Reduce a function to accept an arbitrary subset of X as input

    Parameters
    ----------
    func : function
        Original function, must accept X as input
    X : pd.DataFrame
        Original dataframe, used for filling in missing columns

    Returns
    -------
    function
        Reduced function that takes an arbitrary subset of X's columns as input
    """

    def func_subset(X_subset, X, original_func):
        X_updated = update_columns(base=X, update=X_subset)
        return original_func(X_updated)

    reduced_func = partial(func_subset, X=X, original_func=func)
    return reduced_func


class ShapExplainer(Explainer):
    def __init__(self, func, X, profile_columns=None):
        """Create a Shap Explainer

        Parameters
        ----------
        func : function
            Function to be explained. Must map from X to array-like
        X : pd.DataFrame
            Background dataset for Shapley value calculation
        profile_columns : list, optional
            Calculate Shapley values only for a subset of columns, by default all columns will be included
        """
        if profile_columns is not None:
            func = reduce_func(func, X=self._create_background_data(X))
            X = X[profile_columns]

        self.func = func
        self.X = self._create_background_data(X)
        self.n_col = len(self.X.columns)

    @staticmethod
    def _create_background_data(X):
        """Create single-row background dataset"""
        background = {}
        for col in X.columns:
            if pd.api.types.is_numeric_dtype(X[col]):
                background[col] = [X[col].median()]
            elif pd.api.types.is_object_dtype(X[col]):
                background[col] = [fast_object_mode(X[col])]
            else:
                background[col] = [X[col].mode(dropna=False).values[0]]
        X_background = pd.DataFrame(background, columns=X.columns).astype(X.dtypes)
        return X_background

    def explain(self, X):
        """Calculate Shapley explanations for a dataframe"""
        baselines = []
        explanations = []
        for i in range(len(X)):  # loop over rows
            row = X.iloc[[i]]
            reference, explanation = self._explain_row(row)
            baselines.append(reference)
            explanations.append(explanation)
        baselines = pd.Series(baselines, name="Baseline")
        explanations = pd.DataFrame(explanations, columns=X.columns)
        return baselines, explanations

    def _explain_row(self, row):
        """Calculate Shapley explanations for a single-row dataframe

        We are following Lundberg & Lee (2017) for the Kernel SHAP methodology:

        - Sample possible coalitions (i.e. active/inactive features)
        - Map those coalitions to features and predict
        - Regress predictions on coalition indicators using the SHAP Kernel

        For the final regression, the goal is to minimize the objective

        ||y - phi0 - indicators @ phi||

        with weights w (see Theorem 2 in the paper).

        The SHAP Kernel weights are infinite for the empty and the full coalition.
        This creates two constraints on Shapley values phi0, phi:

        [I]  phi0 == y_empty
        [II] phi0 + np.sum(phi) == y_full

        We minimize the objective on the mixed coalitions (which have finite weights) subject to
        constraints [I] and [II]. This is done by reformulating the objective function.
        First, substitute out phi0 = y_empty using [I]. Second, substitute out the last element
        of phi, phi_k, using [II]. This yields an unconstrained problem that can be solved by
        weighted least squares using numpy only (see code for details).
        """
        empty_coalition = {tuple([0] * self.n_col)}
        full_coalition = {tuple([1] * self.n_col)}

        X_empty = self._map_features(empty_coalition, row)
        X_full = self._map_features(full_coalition, row)

        y_empty = np.float(self.func(X_empty))
        y_full = np.float(self.func(X_full))

        if self.n_col == 1:
            # We have two constraints and two unknowns
            phi0 = y_empty
            phi = y_full - phi0
            return phi0, phi

        else:
            # We actually need to sample coalitions and solve the WLS problem
            coalitions = self._sample_coalitions(self.n_col)
            X = self._map_features(coalitions, row)
            y = np.array(self.func(X))

            weights = np.diag(self._coalition_weights(coalitions))
            indicators = np.array(list(coalitions), dtype=int)

            # define phi_ as all thetas but the last and phi_k as the last (k'th) phi
            # define indicators_ and indicators_k as the corresponding coalition indicators
            # we substitute out phi_k using constraint [II], which implies that
            # phi_k == y_full - phi0 - np.sum(phi_)
            phi0 = y_empty  # from [1]
            indicators_ = indicators[:, 0:-1]  # all indicators but the last
            indicators_k = indicators[:, -1]  # last indicator
            lhs = indicators_ - np.expand_dims(indicators_k, 1)
            rhs = (y - phi0) - indicators_k * (y_full - phi0)
            optim = np.linalg.lstsq(a=weights @ lhs, b=weights @ rhs, rcond=None)
            phi_ = optim[0]  # all but last phi
            phi_k = y_full - phi0 - np.sum(phi_)  # recover last phi from constraint
            phi = np.append(phi_, phi_k)  # reconstruct final phi

            return phi0, phi

    def _sample_coalitions(self, n_col):
        """Sample coalition vectors given a maximum coalition size of n_col"""
        budget = 2 * n_col + 2 ** 11  # set sampling budget
        coalitions = set()  # container for collecting coalitions

        for n_out in range(1, math.floor(n_col / 2) + 1):
            # coalitions starting from all columns (but one)
            new_coalitions0 = set(self._unique_coalitions(n_col - n_out, n_out))

            # coalitions starting from no columns (but one)
            if n_out < n_col - n_out:
                new_coalitions1 = set(self._unique_coalitions(n_out, n_col - n_out))
                new_coalitions = new_coalitions0.union(new_coalitions1)
            else:
                new_coalitions = new_coalitions0

            budget -= len(new_coalitions)

            if budget >= 0:
                coalitions.update(new_coalitions)
            else:
                return coalitions

        return coalitions

    def _map_features(self, coalitions, row):
        """Map coalition vectors to original feature space"""
        X_mapped = row.copy().iloc[[0] * len(coalitions)]  # repeat row

        # for each row (coalition) replace values with value from  background dataset
        coalitions_array = np.array(list(coalitions), dtype=bool)
        for i, col in enumerate(X_mapped.columns):
            inside = coalitions_array[:, i]
            X_mapped[col].where(cond=inside, other=self.X[col].values, inplace=True)
        return X_mapped

    @staticmethod
    def _coalition_weights(coalitions):
        """Calculate the sampling weight of each coalition using the SHAP Kernel"""
        coalitions = np.array(list(coalitions), dtype=bool)
        n_active = np.sum(coalitions, axis=1)
        n_col = coalitions.shape[1]
        weights = (n_col - 1) / (comb(n_col, n_active) * n_active * (n_col - n_active))
        return weights

    @staticmethod
    def _unique_coalitions(n_true, n_false):
        """Calculate all coalitions of n_true "True" and n_false "False" values"""
        length = n_true + n_false
        for indices in combinations(range(length), n_false):
            coalitions = [True] * length  # base case
            for index in indices:
                coalitions[index] = False
            yield tuple(coalitions)
