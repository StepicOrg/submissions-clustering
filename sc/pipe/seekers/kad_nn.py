from itertools import takewhile

import numpy as np
from sklearn.neighbors import NearestNeighbors

from sc.pipe.base import NeighborsMixin


class KADNearestNeighbors(NearestNeighbors, NeighborsMixin):
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
