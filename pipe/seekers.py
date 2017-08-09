import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator

from .cookers import KADNearestNeighbors
from .utils.preprocessing import find_centers


class Seeker(BaseEstimator):
    def __init__(self, *, insider_cluster=False, start_from_center=False, only_centroids=False,
                 max_c=200, dist_c=1., cmax_c=20, cdist_c=.1,
                 leaf_size=30, parralel=False):
        self.inside_cluster = insider_cluster
        self.start_from_center = start_from_center
        self.only_centroids = only_centroids
        self.max_c = max_c
        self.dist_c = dist_c
        self.cmax_c = cmax_c
        self.cdist_c = cdist_c
        self.leaf_size = leaf_size
        self.parralel = parralel

        self._c = None
        self._nns = None

    @staticmethod
    def from_predefined(seeker):
        if seeker == "nn":
            return Seeker()
        else:
            raise ValueError("No such seeker supported yet")

    @property
    def _n_jobs(self):
        return -1 if self.parralel else 1

    def fit(self, X, y=None, c=None):
        if y is None:
            y = -np.ones(X.shape[0], dtype=int)
        y = pd.Series.from_array(y)

        if c is None:
            c = find_centers(X, y)

        if self.only_centroids:
            new_y_list = [y[y == -1]]
            for label in range(len(c)):
                train = y == label
                if sum(train):
                    nn = KADNearestNeighbors(n_neighbors=min(sum(train), self.cmax_c),
                                             radius=self.cdist_c,
                                             leaf_size=self.leaf_size,
                                             n_jobs=self._n_jobs)
                    i = y[train].index.values
                    nn.fit(X[i], i)
                    ind = nn.neighbors(c[label][np.newaxis, :])
                    new_y_list.append(y.iloc[ind[0]])
            y = pd.concat(new_y_list)

        nns = {}
        for label in range(-1, len(c)):
            if not self.inside_cluster and label != -1:
                nns[label] = nns[-1]
            else:
                train = y == y if label == -1 else y == label
                if sum(train):
                    nn = KADNearestNeighbors(n_neighbors=min(sum(train), self.max_c),
                                             radius=self.dist_c,
                                             leaf_size=self.leaf_size,
                                             n_jobs=self._n_jobs)
                    i = y[train].index.values
                    nn.fit(X[i], i)
                    nns[label] = nn

        self._c = c
        self._nns = nns

    def neighbors(self, X, y=None):
        if y is None:
            y = -np.ones(X.shape[0], dtype=int)

        ans = [[]] * X.shape[0]

        for label in np.unique(y):
            test = y == label
            if label in self._nns:
                nn = self._nns[label]
                if self.start_from_center and label != -1:
                    ind = np.repeat(nn.neighbors(self._c[label][np.newaxis, :]), sum(test), axis=0)
                else:
                    ind = nn.neighbors(X[test])
            else:
                ind = [[]] * sum(test)
            for i, v in zip(np.where(test)[0], ind):
                ans[i] = v

        return ans
