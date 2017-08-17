import pandas as pd

from subsclu import utils
from subsclu.pipe.bases import BaseEstimator, NeighborsMixin
from subsclu.utils import LoadSaveMixin

__all__ = ["SubmissionsClustering"]


class SubmissionsClustering(BaseEstimator, NeighborsMixin, LoadSaveMixin):
    def __init__(self, preprocessor, vectorizer, clusterizer, seeker):
        self.preprocessor = preprocessor
        self.vectorizer = vectorizer
        self.clusterizer = clusterizer
        self.seeker = seeker

    def fit(self, submissions):
        """Fit model with new submissions.

        :param submissions: code samples
        :type submissions: list[(str, str)]

        :return: self
        :rtype: SubmissionsClustering
        """
        codes, statuses = utils.split_into_lists(submissions)
        correct_indicies, structs = self.preprocessor.fit_sanitize(codes)
        del codes
        vecs = self.vectorizer.fit_transform(structs)
        del structs
        labels = self.clusterizer.fit_predict(vecs)
        statuses = pd.Series(statuses).iloc[correct_indicies]
        train_ind = statuses.reset_index(drop=True)
        train_ind = train_ind[train_ind == "correct"].index.values
        indicies = statuses[statuses == "correct"].index.values
        del statuses
        del correct_indicies
        self.seeker.fit(vecs=vecs[train_ind], labels=labels[train_ind],
                        indicies=indicies, centers=utils.find_centers(vecs, labels))
        return self

    def neighbors(self, codes):
        """Give neighbors indicies for each code sample in the input.

        :param codes: code samples
        :type codes: list[str]

        :return: array of neighbors for each code sample
        :rtype: list[ndarray]
        """
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
        return utils.fill_gaps(correct_indicies, neighbors_ind, size)
