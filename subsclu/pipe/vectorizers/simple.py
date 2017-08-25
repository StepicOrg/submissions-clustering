"""Simple methods implementation."""

import numpy as np
from scipy.sparse import issparse

from subsclu.pipe.bases import BaseEstimator, TransformerMixin

__all__ = ["DenseTransformer", "SumList", "MeanList"]


class DenseTransformer(BaseEstimator, TransformerMixin):
    """Transform sparse matrix into dense."""

    def fit(self, vecs):
        # pylint: disable=unused-argument
        """Doing nothing."""
        return self

    def transform(self, vecs):
        # pylint: disable=no-self-use
        """Transform into dense if was sparse."""
        return vecs.toarray() if issparse(vecs) else vecs


class SumList(BaseEstimator, TransformerMixin):
    """Calculating sum."""

    def fit(self, vecs):
        # pylint: disable=unused-argument
        """Doing nothing."""
        return self

    def transform(self, vecs):
        # pylint: disable=no-self-use
        """Sum input vectors into one."""
        return np.stack([np.sum(vec, axis=0) for vec in vecs])


class MeanList(BaseEstimator, TransformerMixin):
    """Calculating mean."""

    def fit(self, vecs):
        # pylint: disable=unused-argument
        """Doing nothing."""
        return self

    def transform(self, vecs):
        # pylint: disable=no-self-use
        """Calculate mean of input vectors."""
        return np.stack([np.mean(vec, axis=0) for vec in vecs])
