import numpy as np

from sc.pipe.bases import BaseEstimator, ClusterMixin

__all__ = ["StupidClusterizer"]


class StupidClusterizer(BaseEstimator, ClusterMixin):
    def __init__(self):
        self.labels_ = None

    def __stupid_labels(self, n):
        return -np.ones(n, dtype=np.int32)

    def fit(self, X):
        self.labels_ = self.__stupid_labels(X.shape[0])
        return self

    def predict(self, X):
        return self.__stupid_labels(X.shape[0])
