from sklearn.base import BaseEstimator, TransformerMixin


class BagOfWords(BaseEstimator, TransformerMixin):
    def __init__(self):
        pass

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        return X
