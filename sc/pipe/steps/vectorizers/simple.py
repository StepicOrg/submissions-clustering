from sklearn.base import TransformerMixin

__all__ = ["DenseTransformer"]


class DenseTransformer(TransformerMixin):
    def fit(self, X, y=None):
        return self

    def transform(self, X):
        return X.toarray()
