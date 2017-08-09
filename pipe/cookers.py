from itertools import takewhile

import numpy as np
from more_itertools import flatten, windowed
from sklearn.base import TransformerMixin
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.neighbors import NearestNeighbors


class BagOfNgrams(CountVectorizer):
    def build_analyzer(self):
        left_bound, right_bound = self.ngram_range

        def analyzer(x):
            return flatten(windowed(x, i) for i in range(left_bound, min(len(x), right_bound) + 1))

        return analyzer


class BagOfTrees(CountVectorizer):
    def build_analyzer(self):
        left_bound, right_bound = self.ngram_range

        def analyzer(x):
            return flatten(x.subtrees(i) for i in range(left_bound, right_bound + 1))

        return analyzer


"""
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
"""


class KADNearestNeighbors(NearestNeighbors):
    def __init__(self, n_neighbors=5, radius=1.0,
                 algorithm='auto', leaf_size=30, metric='minkowski',
                 p=2, metric_params=None, n_jobs=1, **kwargs):
        super().__init__(n_neighbors=n_neighbors, radius=radius,
                         algorithm=algorithm, leaf_size=leaf_size, metric=metric,
                         p=p, metric_params=metric_params, n_jobs=n_jobs, **kwargs)

        self._i = None

    def fit(self, X, i=None):
        self._i = i if i is not None else np.arange(X.shape[0])
        return super().fit(X)

    def neighbors(self, X):
        dist, ind = self.kneighbors(X)
        new_ind = []
        for odist, oind in zip(dist, ind):
            rind = list(map(lambda x: x[1], takewhile(lambda x: x[0] <= self.radius, zip(odist, oind))))
            new_ind.append(self._i[rind].tolist())
        return new_ind


class DenseTransformer(TransformerMixin):
    def fit(self, X, y=None):
        return self

    def transform(self, X):
        return X.toarray()
