import numpy as np
from sklearn.base import BaseEstimator, ClusterMixin

__all__ = ["StupidClusterizer"]


class StupidClusterizer(BaseEstimator, ClusterMixin):
    def __init__(self):
        self.labels_ = None

    def _stupid_labels(self, n):
        return -np.ones(n, dtype=np.int32)

    def fit(self, X):
        self.labels_ = self._stupid_labels(X.shape[0])
        return self

    def predict(self, X):
        return self._stupid_labels(X.shape[0])
