import numpy as np

from subsclu.pipe.bases import BaseEstimator, ClusterMixin

__all__ = ["StupidClusterizer"]


class StupidClusterizer(BaseEstimator, ClusterMixin):
    def __init__(self):
        self.labels_ = None

    def _stupid_labels(self, size):
        return -np.ones(size, dtype=np.int32)

    def fit(self, vecs):
        self.labels_ = self._stupid_labels(vecs.shape[0])
        return self

    def predict(self, vecs):
        return self._stupid_labels(vecs.shape[0])
