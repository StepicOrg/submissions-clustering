import pandas as pd

from subsclu.pipe.bases import BaseEstimator, NeighborsMixin
from subsclu.utils.dump import LoadSaveMixin
from subsclu.utils.matrix import find_centers
from subsclu.utils.read import split_into_lists


class SubmissionsClustering(BaseEstimator, NeighborsMixin, LoadSaveMixin):
    def __init__(self, preprocessor, vectorizer, clusterizer, seeker):
        self.preprocessor = preprocessor
        self.vectorizer = vectorizer
        self.clusterizer = clusterizer
        self.seeker = seeker

        self._train_ind = None

    def fit(self, submissions):
        """Fit model with new submissions.

        :param submissions: tuple of (code, status), where status either "correct" or something
        else
        :type submissions: list[(str, str)]

        :return: self
        :rtype: SubmissionsClustering
        """
        codes, statuses = split_into_lists(submissions)
        structs = self.preprocessor.fit_sanitize(codes)
        vecs = self.vectorizer.fit_transform(structs)
        labels = self.clusterizer.fit_predict(vecs)
        statuses = pd.Series(statuses)
        self._train_ind = statuses[statuses == "correct"].index.values
        self.seeker.fit(vecs=vecs[self._train_ind], labels=labels[self._train_ind],
                        centers=find_centers(vecs, labels))
        return self

    def neighbors(self, codes):
        """Give correct neighbors indicies for each code sample in the input.

        :param codes: code samples
        :type codes: list[str]

        :return: array of neighbors inds for each code sample
        :rtype: list[ndarray]
        """
        structs = self.preprocessor.sanitize(codes)
        vecs = self.vectorizer.transform(structs)
        labels = self.clusterizer.predict(vecs)
        neighbors_inds = self.seeker.neighbors(vecs, labels)
        answer = []
        for neighbors_ind in neighbors_inds:
            if neighbors_ind.size:
                answer.append(self._train_ind[neighbors_ind])
            else:
                answer.append([])
        return answer
