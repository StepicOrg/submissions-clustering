from itertools import chain

import numpy as np
import pandas as pd
from more_itertools import flatten
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.feature_extraction.text import CountVectorizer

from .primitives import DefaultIntBijection


def parse(s):
    t = tuple(map(int, s.split()))
    return t[0] if len(t) == 1 else t


class ForNodeEmbedding(BaseEstimator, TransformerMixin):
    def fit(self, X, y=None):
        return self

    def transform(self, X):
        return pd.DataFrame.from_records(chain.from_iterable(x.flatten(add_children_leaves_nums=True) for x in X))


class BagOfWords(CountVectorizer):
    def __init__(self, *args, **kwargs):
        kwargs["token_pattern"] = "[0-9]+"
        super().__init__(*args, **kwargs)

    # noinspection PyAttributeOutsideInit
    def fit_transform(self, X, y=None):
        X = list(map(lambda x: " ".join(str(i) for i in x), X))
        result = super().fit_transform(X, y)
        self.vocabulary_ = {parse(k): v for k, v in self.vocabulary_.items()}
        self.stop_words_ = set(map(parse, self.stop_words_))
        return result


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
