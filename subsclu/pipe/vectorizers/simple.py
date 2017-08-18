import numpy as np

from subsclu.pipe.bases import BaseEstimator, TransformerMixin

__all__ = ["DenseTransformer", "SumList", "MeanList"]


class DenseTransformer(BaseEstimator, TransformerMixin):
    def fit(self, vecs):
        return self

    def transform(self, vecs):
        return vecs.toarray()


class SumList(BaseEstimator, TransformerMixin):
    def fit(self, vecs):
        return self

    def transform(self, vecs):
        return np.stack([np.sum(vec, axis=0) for vec in vecs])


class MeanList(BaseEstimator, TransformerMixin):
    def fit(self, vecs):
        return self

    def transform(self, vecs):
        return np.stack([np.mean(vec, axis=0) for vec in vecs])
