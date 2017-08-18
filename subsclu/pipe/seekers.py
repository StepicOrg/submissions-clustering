from itertools import takewhile

import numpy as np
import pandas as pd
from sklearn.neighbors import NearestNeighbors

from subsclu.pipe.bases import BaseEstimator, NeighborsMixin
from subsclu.utils.matrix import find_centers

__all__ = ["NNSeeker"]


class _KADNearestNeighbors(NearestNeighbors, NeighborsMixin):
    def __init__(self, n_neighbors=5, radius=1.0,
                 algorithm='auto', leaf_size=30, metric='minkowski',
                 p=2, metric_params=None, n_jobs=1, **kwargs):
        super().__init__(n_neighbors=n_neighbors, radius=radius,
                         algorithm=algorithm, leaf_size=leaf_size, metric=metric,
                         p=p, metric_params=metric_params, n_jobs=n_jobs, **kwargs)

        self._indicies = None

    def fit(self, vecs, indicies=None):
        self._indicies = indicies if indicies is not None else np.arange(vecs.shape[0])
        return super().fit(vecs)

    def neighbors(self, vecs):
        dist, ind = self.kneighbors(vecs)
        new_ind = []
        for odist, oind in zip(dist, ind):
            rind = list(map(lambda x: x[1],
                            takewhile(lambda x: x[0] <= self.radius, zip(odist, oind))
                            ))
            new_ind.append(self._indicies[rind].tolist())
        return new_ind


class NNSeeker(BaseEstimator, NeighborsMixin):
    def __init__(self, insider_cluster=False, start_from_center=False, only_centroids=False,
                 max_c=300, dist_c=1., cmax_c=20, cdist_c=.1,
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

        self._centers = None
        self._nns = None

    @property
    def _n_jobs(self):
        return -1 if self.parralel else 1

    def fit(self, vecs, labels, indicies=None, centers=None):
        labels = pd.Series.from_array(labels)
        indicies = indicies if indicies is not None else np.arange(vecs.shape[0])
        centers = centers if centers is not None else find_centers(vecs, labels)

        if self.only_centroids:
            new_labels_list = [labels[labels == -1]]
            for label in range(len(centers)):
                train = labels == label
                if sum(train):
                    nn = _KADNearestNeighbors(n_neighbors=min(sum(train), self.cmax_c),
                                              radius=self.cdist_c,
                                              leaf_size=self.leaf_size,
                                              n_jobs=self._n_jobs)
                    train_ind = labels[train].index.values
                    nn.fit(vecs[train_ind], indicies[train_ind])
                    ind = nn.neighbors(centers[label][np.newaxis, :])[0]
                    new_labels_list.append(labels.iloc[ind])
            labels = pd.concat(new_labels_list)

        nns = {}
        for label in range(-1, len(centers)):
            if not self.inside_cluster and label != -1:
                nns[label] = nns[-1]
            else:
                train = (labels == labels) if label == -1 else (labels == label)
                if sum(train):
                    nn = _KADNearestNeighbors(n_neighbors=min(sum(train), self.max_c),
                                              radius=self.dist_c,
                                              leaf_size=self.leaf_size,
                                              n_jobs=self._n_jobs)
                    train_ind = labels[train].index.values
                    nn.fit(vecs[train_ind], indicies[train_ind])
                    nns[label] = nn

        self._centers = centers
        self._nns = nns
        return self

    def neighbors(self, vecs, labels):
        ans = [[]] * vecs.shape[0]
        for label in np.unique(labels):
            test = labels == label
            if label in self._nns:
                nn = self._nns[label]
                if self.start_from_center and label != -1:
                    indicies = np.repeat(
                        nn.neighbors(self._centers[label][np.newaxis, :]), sum(test), axis=0
                    )
                else:
                    indicies = nn.neighbors(vecs[test])
            else:
                indicies = [[]] * sum(test)
            for ind, elem in zip(np.where(test)[0], indicies):
                ans[ind] = elem
        for ind, elem in enumerate(ans):
            ans[ind] = np.array(elem)
        return ans
