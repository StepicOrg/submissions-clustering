"""Implementation of simple clsuterizers."""

import numpy as np

from subsclu.pipe.bases import BaseEstimator, ClusterMixin

__all__ = ["SimpleClusterizer", "__all__"]


class SimpleClusterizer(BaseEstimator, ClusterMixin):
    """Stupid clusterizer."""

    def __init__(self):
        """Create default simple clusterizer."""
        self.labels_ = None

    @staticmethod
    def _stupid_labels(size):
        return -np.ones(size, dtype=np.int32)

    def fit(self, vecs):
        """Fit model with given vecs, assinging -1 label to each."""
        self.labels_ = self._stupid_labels(vecs.shape[0])
        return self

    def predict(self, vecs):
        """Predicting label, -1 for each."""
        return self._stupid_labels(vecs.shape[0])
