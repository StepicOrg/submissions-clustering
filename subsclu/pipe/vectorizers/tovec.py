"""DL model using gensim."""

import numpy as np
from gensim.models.doc2vec import TaggedDocument, Doc2Vec
from gensim.models.word2vec import Word2Vec

from subsclu.pipe.bases import BaseEstimator, TransformerMixin

__all__ = ["Token2Vec", "Tokens2Vec"]


class Token2Vec(BaseEstimator, TransformerMixin):
    """Token embeddings."""

    def _make_model(self):
        return Word2Vec(size=self.size, min_count=self.min_count,
                        iter=self.max_iter, workers=self.workers)

    def __init__(self, size=100, min_count=1, max_iter=20, workers=1):
        """Make initialization of t2v model.

        Args:
            size (int): Size of feature dim.
            min_count (int): Min count of token to be included in dict.
            max_iter (int): Max number of iterations untill covergence.
            workers (int): CPU to run in parralel.
        """
        self.size = size
        self.min_count = min_count
        self.max_iter = max_iter
        self.workers = workers

        self._model = self._make_model()

    def fit(self, tokens):
        """Doing model fit of given tokens."""
        tokens = [[str(num) for num in vec] for vec in tokens]
        self._model.build_vocab(tokens)
        self._model.train(tokens, total_examples=self._model.corpus_count,
                          epochs=self._model.iter)
        return self

    def transform(self, tokens):
        """Transform each token into vec."""
        return [np.stack([
            self._model[str(num)] if str(num) in self._model
            else np.zeros(self.size)
            for num in vec
        ]) for vec in tokens]


class Tokens2Vec(BaseEstimator, TransformerMixin):
    """Tokens embedding."""

    def _make_model(self):
        return Doc2Vec(size=self.size, min_count=self.min_count,
                       iter=self.max_iter, workers=self.workers)

    def __init__(self, size=100, min_count=2, max_iter=20, workers=1):
        """Make initialization of ts2v model.

        Args:
            size (int): Size of feature dim.
            min_count (int): Min count of token to be included in dict.
            max_iter (int): Max number of iterations untill covergence.
            workers (int): CPU to run in parralel.
        """
        self.size = size
        self.min_count = min_count
        self.max_iter = max_iter
        self.workers = workers

        self._model = self._make_model()

    @staticmethod
    def _to_strs(vec):
        return list(map(str, vec.tolist()))

    def fit(self, vecs):
        """Doing model fit of given vecs."""
        vecs = list(
            TaggedDocument(self._to_strs(vec), [ind])
            for ind, vec in enumerate(vecs)
        )
        self._model.build_vocab(vecs)
        self._model.train(vecs, total_examples=self._model.corpus_count,
                          epochs=self._model.iter)
        return self

    def transform(self, vecs):
        """Transform vec into vec."""
        return np.stack([
            self._model.infer_vector(self._to_strs(vec)) for vec in vecs
        ])
