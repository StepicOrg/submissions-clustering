from itertools import chain

import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.feature_extraction.text import CountVectorizer

from .primitives import DefaultIntBijection


def parse(s):
    t = tuple(map(int, s.split()))
    return t[0] if len(t) == 1 else t


class BagOfWords(CountVectorizer):
    # noinspection PyAttributeOutsideInit
    def fit_transform(self, X, y=None):
        X = list(map(lambda x: " ".join(str(i) for i in x), X))
        result = super().fit_transform(X, y)
        self.vocabulary_ = {parse(k): v for k, v in self.vocabulary_.items()}
        self.stop_words_ = set(map(parse, self.stop_words_))
        return result


class BagOfTrees(BaseEstimator, TransformerMixin):
    def __init__(self, height=2):
        self.height = height

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        n = len(X)
        X = list(list(x.subtrees(self.height)) for x in X)
        dib = DefaultIntBijection(type2=tuple)
        for subtree in chain.from_iterable(X):
            _ = dib[subtree]
        m = len(dib)
        enc_X = np.zeros((n, m))
        for i in range(n):
            for subtree in X[i]:
                enc_X[i, dib[subtree]] += 1
        return enc_X
