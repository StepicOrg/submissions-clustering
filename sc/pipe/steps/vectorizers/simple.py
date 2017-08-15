from sc.pipe.bases import BaseEstimator, TransformerMixin

__all__ = ["DenseTransformer"]


class DenseTransformer(BaseEstimator, TransformerMixin):
    def fit(self, X, y=None):
        return self

    def transform(self, X):
        return X.toarray()
