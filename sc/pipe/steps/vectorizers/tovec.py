import numpy as np
from gensim.models.doc2vec import TaggedDocument, Doc2Vec
from gensim.models.word2vec import Word2Vec

from sc.pipe.bases import BaseEstimator, TransformerMixin

__all__ = ["Token2Vec", "Tokens2Vec"]


class Token2Vec(BaseEstimator, TransformerMixin):
    def __make_model(self):
        return Word2Vec(size=self.size, min_count=self.min_count, iter=self.max_iter, workers=self.workers)

    def __init__(self, size=100, min_count=1, max_iter=20, workers=1):
        self.size = size
        self.min_count = min_count
        self.max_iter = max_iter
        self.workers = workers

        self.__model = self.__make_model()

    def fit(self, X, y=None):
        X = [[str(num) for num in x] for x in X]
        self.__model.build_vocab(X)
        self.__model.train(X, total_examples=self.__model.corpus_count, epochs=self.__model.iter)
        return self

    def transform(self, X):
        return [np.stack(
            [self.__model[str(num)] if str(num) in self.__model else np.zeros(self.size) for num in x]
        ) for x in X]


class Tokens2Vec(BaseEstimator, TransformerMixin):
    def __make_model(self):
        return Doc2Vec(size=self.size, min_count=self.min_count, iter=self.max_iter, workers=self.workers)

    def __init__(self, size=100, min_count=2, max_iter=20, workers=1):
        self.size = size
        self.min_count = min_count
        self.max_iter = max_iter
        self.workers = workers

        self.__model = self.__make_model()

    def fit(self, X, y=None):
        X = list(TaggedDocument(x, i) for i, x in enumerate(X))
        self.__model.build_vocab(X)
        self.__model.train(X, total_examples=self.__model.corpus_count, epochs=self.__model.iter)
        return self

    def transform(self, X):
        return np.stack([self.__model.infer_vector(x) for x in X])
