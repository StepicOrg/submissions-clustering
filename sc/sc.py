import pandas as pd

from sc import utils
from sc.pipe.bases import BaseEstimator, NeighborsMixin

__all__ = ["SubmissionsClustering"]


def _fill_gaps(indicies, elems, size, gap=lambda: []):
    full = [None] * size
    for ind, elem in zip(indicies, elems):
        full[ind] = elem
    for ind in range(size):
        if full[ind] is None:
            full[ind] = gap()
    return full


class SubmissionsClustering(BaseEstimator, NeighborsMixin, utils.LoadSaveMixin):
    def __init__(self, preprocessor, vectorizer, clusterizer, seeker):
        self.preprocessor = preprocessor
        self.vectorizer = vectorizer
        self.clusterizer = clusterizer
        self.seeker = seeker

    def fit(self, submissions):
        codes, statuses = utils.split_into_lists(submissions)
        correct_indicies, structs = self.preprocessor.fit_sanitize(codes)
        del codes
        vecs = self.vectorizer.fit_transform(structs)
        del structs
        labels = self.clusterizer.fit_predict(vecs)
        train_ind = (pd.Series(statuses).iloc[correct_indicies] == "correct").index.values
        del statuses
        del correct_indicies
        self.seeker.fit(vecs=vecs[train_ind], labels=labels[train_ind],
                        indicies=train_ind, centers=utils.find_centers(vecs, labels))
        return self

    def neighbors(self, codes):
        codes = list(codes)
        size = len(codes)
        correct_indicies, structs = self.preprocessor.sanitize(codes)
        del codes
        vecs = self.vectorizer.transform(structs)
        del structs
        labels = self.clusterizer.predict(vecs)
        neighbors_ind = self.seeker.neighbors(vecs, labels)
        del vecs
        del labels
        return _fill_gaps(correct_indicies, neighbors_ind, size)
