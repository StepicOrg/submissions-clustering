"""Module for implementation of seekers."""

from itertools import takewhile

import numpy as np
import pandas as pd
from sklearn.neighbors import NearestNeighbors

from subsclu.pipe.bases import BaseEstimator, NeighborsMixin
from subsclu.utils.matrix import find_centers

__all__ = ["NNSeeker"]


class _KADNearestNeighbors(NearestNeighbors):
    def neighbors(self, vecs):
        """Output neighbors inds for each vec, consider both constraints."""
        dist, ind = self.kneighbors(vecs)
        new_ind = []
        for odist, oind in zip(dist, ind):
            new_ind.append(list(
                map(
                    lambda x: x[1],
                    takewhile(lambda x: x[0] <= self.radius, zip(odist, oind))
                )
            ))
        return new_ind


class NNSeeker(BaseEstimator, NeighborsMixin):
    # pylint: disable=too-many-instance-attributes
    """Seeker based on nearese neighbors finding."""

    def __init__(self, insider_cluster=False, start_from_center=False,
                 only_centroids=False, max_c=200, dist_c=1., cmax_c=20,
                 cdist_c=.1, leaf_size=30, parralel=False):
        # pylint: disable=too-many-arguments
        """Make NNSeeker.

        Args:
            insider_cluster (bool): If find neighbors inside same cluster.
            start_from_center (bool): If start from center of cluster.
            only_centroids (bool): If consider obly centroids.
            max_c (int): Maximun number of neighbors.
            dist_c (float): Maximun distance to find.
            cmax_c (int): Maximun number of neighbors for centroids.
            cdist_c (float): Maximun distance to find for centroids.l
            leaf_size (int): Leaf size in structs for NN.
            parralel (bool): If do jobs in parralel.
        """
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

    def fit(self, vecs, labels, centers=None):
        """Fit model with given vecs and labels."""
        labels = pd.Series.from_array(labels)
        if centers is None:
            centers = find_centers(vecs, labels)

        if self.only_centroids:
            new_labels_list = [labels[labels == -1]]
            for cur_label, cur_center in enumerate(centers):
                train = labels == cur_label
                if sum(train):
                    nn_alg = _KADNearestNeighbors(
                        n_neighbors=min(sum(train), self.cmax_c),
                        radius=self.cdist_c,
                        leaf_size=self.leaf_size,
                        n_jobs=self._n_jobs
                    )
                    train_ind = labels[train].index.values
                    nn_alg.fit(vecs[train_ind])
                    ind = nn_alg.neighbors(cur_center[np.newaxis, :])[0]
                    new_labels_list.append(labels.iloc[ind])
            labels = pd.concat(new_labels_list)

        nns = {}
        for cur_label in range(-1, len(centers)):
            if not self.inside_cluster and cur_label != -1:
                nns[cur_label] = nns[-1]
            else:
                if cur_label == -1:
                    train = (labels == labels)
                else:
                    train = (labels == cur_label)
                if sum(train):
                    nn_alg = _KADNearestNeighbors(
                        n_neighbors=min(sum(train), self.max_c),
                        radius=self.dist_c,
                        leaf_size=self.leaf_size,
                        n_jobs=self._n_jobs
                    )
                    train_ind = labels[train].index.values
                    nn_alg.fit(vecs[train_ind])
                    nns[cur_label] = nn_alg

        self._centers = centers
        self._nns = nns
        return self

    def neighbors(self, vecs, labels):
        """Output neighbors inds for each vec."""
        ans = [[]] * vecs.shape[0]
        for label in np.unique(labels):
            test = labels == label
            if label in self._nns:
                nn_alg = self._nns[label]
                if self.start_from_center and label != -1:
                    indicies = np.repeat(
                        nn_alg.neighbors(self._centers[label][np.newaxis, :]),
                        sum(test),
                        axis=0
                    )
                else:
                    indicies = nn_alg.neighbors(vecs[test])
            else:
                indicies = [[]] * sum(test)
            for ind, elem in zip(np.where(test)[0], indicies):
                ans[ind] = elem
        for ind, elem in enumerate(ans):
            ans[ind] = np.array(elem)
        return ans
