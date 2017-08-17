import numpy as np
from gensim.models.doc2vec import TaggedDocument, Doc2Vec
from gensim.models.word2vec import Word2Vec

from sc.pipe.bases import BaseEstimator, TransformerMixin

__all__ = ["Token2Vec", "Tokens2Vec"]


class Token2Vec(BaseEstimator, TransformerMixin):
    def _make_model(self):
        return Word2Vec(size=self.size, min_count=self.min_count, iter=self.max_iter,
                        workers=self.workers)

    def __init__(self, size=100, min_count=1, max_iter=20, workers=1):
        self.size = size
        self.min_count = min_count
        self.max_iter = max_iter
        self.workers = workers

        self._model = self._make_model()

    def fit(self, vecs):
        vecs = [[str(num) for num in vec] for vec in vecs]
        self._model.build_vocab(vecs)
        self._model.train(vecs, total_examples=self._model.corpus_count, epochs=self._model.iter)
        return self

    def transform(self, vecs):
        return [np.stack([self._model[str(num)] if str(num) in self._model
                          else np.zeros(self.size) for num in vec]) for vec in vecs]


class Tokens2Vec(BaseEstimator, TransformerMixin):
    def _make_model(self):
        return Doc2Vec(size=self.size, min_count=self.min_count, iter=self.max_iter,
                       workers=self.workers)

    def __init__(self, size=100, min_count=2, max_iter=20, workers=1):
        self.size = size
        self.min_count = min_count
        self.max_iter = max_iter
        self.workers = workers

        self._model = self._make_model()

    def fit(self, vecs):
        vecs = list(TaggedDocument(vec, ind) for ind, vec in enumerate(vecs))
        self._model.build_vocab(vecs)
        self._model.train(vecs, total_examples=self._model.corpus_count, epochs=self._model.iter)
        return self

    def transform(self, vecs):
        return np.stack([self._model.infer_vector(vec) for vec in vecs])
