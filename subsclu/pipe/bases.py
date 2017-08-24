"""Base classes and mixins for pipe ops."""

from sklearn.base import BaseEstimator, TransformerMixin, ClusterMixin

__all__ = ["BaseEstimator", "TransformerMixin", "ClusterMixin",
           "SanitizerMixin", "NeighborsMixin"]


class SanitizerMixin:
    # pylint: disable=too-few-public-methods
    """Default mixin for sanitizier."""

    def fit_sanitize(self, codes, **fit_params):
        """Fit model with given data, then sanitize it."""
        return self.fit(codes, **fit_params).sanitize(codes)


class NeighborsMixin:
    # pylint: disable=too-few-public-methods
    """Default mixin for neighbors."""

    def fit_neighbors(self, vecs, labels, **fit_params):
        """Fit model with given data, then neighbors it."""
        return self.fit(vecs, labels, **fit_params).neighbors(vecs)
