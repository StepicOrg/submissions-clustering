from gensim.models.doc2vec import LabeledSentence
from sc.pipe.bases import BaseEstimator, TransformerMixin

__all__ = []

# TODO: хотим:
# список токенов -> вектор
# список токенов -> список векторов


class Tokens2Vec(BaseEstimator, TransformerMixin):
    def __init__(self):
        pass

    def fit(self, X):
        pass

    def transform(self, X):
        pass
