import numpy as np
import pandas as pd

from sc.pipe.bases import BaseEstimator, NeighborsMixin
from sc.pipe.commons import KADNearestNeighbors

__all__ = ["NNSeeker"]


class NNSeeker(BaseEstimator, NeighborsMixin):
    def __init__(self, insider_cluster=False, start_from_center=False, only_centroids=False,
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

        self.__c = None
        self.__nns = None

    @property
    def __n_jobs(self):
        return -1 if self.parralel else 1

    def fit(self, X, y, c, i=None):
        y = pd.Series.from_array(y)
        i = i if i is not None else np.arange(X.shape[0])

        if self.only_centroids:
            new_y_list = [y[y == -1]]
            for label in range(len(c)):
                train = y == label
                if sum(train):
                    nn = KADNearestNeighbors(n_neighbors=min(sum(train), self.cmax_c),
                                             radius=self.cdist_c,
                                             leaf_size=self.leaf_size,
                                             n_jobs=self.__n_jobs)
                    ii = y[train].index.values
                    nn.fit(X[ii], i[ii])
                    ind = nn.neighbors(c[label][np.newaxis, :])
                    new_y_list.append(y.iloc[ind[0]])
            y = pd.concat(new_y_list)

        nns = {}
        for label in range(-1, len(c)):
            if not self.inside_cluster and label != -1:
                nns[label] = nns[-1]
            else:
                train = (y == y) if label == -1 else (y == label)
                if sum(train):
                    nn = KADNearestNeighbors(n_neighbors=min(sum(train), self.max_c),
                                             radius=self.dist_c,
                                             leaf_size=self.leaf_size,
                                             n_jobs=self.__n_jobs)
                    ii = y[train].index.values
                    nn.fit(X[ii], i[ii])
                    nns[label] = nn

        self.__c = c
        self.__nns = nns
        return self

    def neighbors(self, X, y):
        ans = [[]] * X.shape[0]

        for label in np.unique(y):
            test = y == label
            if label in self.__nns:
                nn = self.__nns[label]
                if self.start_from_center and label != -1:
                    ind = np.repeat(nn.neighbors(self.__c[label][np.newaxis, :]), sum(test), axis=0)
                else:
                    ind = nn.neighbors(X[test])
            else:
                ind = [[]] * sum(test)
            for i, v in zip(np.where(test)[0], ind):
                ans[i] = v

        return ans
