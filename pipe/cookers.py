from itertools import chain

import numpy as np
from more_itertools import flatten, windowed
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.feature_extraction.text import CountVectorizer

from .primitives import DefaultIntBijection


class BagOfNgrams(CountVectorizer):
    def build_analyzer(self):
        left_bound, right_bound = self.ngram_range

        def analyzer(x):
            n = len(x)
            return flatten(windowed(x, i) for i in range(left_bound, min(n, right_bound) + 1))

        return analyzer


# TODO: same as above
class BagOfTrees(BaseEstimator, TransformerMixin):
    def __init__(self, ngram_range=(2, 2)):
        self.ngram_range = ngram_range

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        n = len(X)
        left_ngr, right_ngr = self.ngram_range
        X = list(list(chain.from_iterable(x.subtrees(height) for height in range(left_ngr, right_ngr + 1))) for x in X)
        dib = DefaultIntBijection(type2=tuple)
        for subtree in chain.from_iterable(X):
            _ = dib[subtree]
        m = len(dib)
        enc_X = np.zeros((n, m))
        for i in range(n):
            for subtree in X[i]:
                enc_X[i, dib[subtree]] += 1
        return enc_X
