import numpy as np
from sklearn.base import BaseEstimator, ClusterMixin

__all__ = ["StupidClusterizer"]


class StupidClusterizer(BaseEstimator, ClusterMixin):
    def fit(self, X):
        return self

    def predict(self, X):
        return -np.ones(X.shape[0], dtype=np.int32)
