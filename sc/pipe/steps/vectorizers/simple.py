from sc.pipe.bases import BaseEstimator, TransformerMixin
import numpy as np

__all__ = ["DenseTransformer", "SumList", "MeanList"]


class DenseTransformer(BaseEstimator, TransformerMixin):
    def fit(self, X, y=None):
        return self

    def transform(self, X):
        return X.toarray()


class SumList(BaseEstimator, TransformerMixin):
    def fit(self, X, y=None):
        return self

    def transform(self, X):
        return np.stack([np.sum(x, axis=0) for x in X])


class MeanList(BaseEstimator, TransformerMixin):
    def fit(self, X, y=None):
        return self

    def transform(self, X):
        return np.stack([np.mean(x, axis=0) for x in X])
