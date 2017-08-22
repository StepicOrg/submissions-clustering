import logging

import pandas as pd

from subsclu.pipe.bases import BaseEstimator, NeighborsMixin
from subsclu.utils.dump import LoadSaveMixin
from subsclu.utils.matrix import find_centers
from subsclu.utils.read import split_into_lists

logger = logging.getLogger(__name__)


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
        logger.info("fitting preprocessor step")
        structs = self.preprocessor.fit_sanitize(codes)
        logger.info("fitting vectorizer step")
        vecs = self.vectorizer.fit_transform(structs)
        logger.info("fitting clusterizer step")
        labels = self.clusterizer.fit_predict(vecs)
        statuses = pd.Series(statuses)
        self._train_ind = statuses[statuses == "correct"].index.values
        logger.debug("num of correct codes={}".len(self._train_ind))
        logger.info("fitting seeker step")
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
        logger.info("doing preprocessor step")
        structs = self.preprocessor.sanitize(codes)
        logger.info("doing vectorizer step")
        vecs = self.vectorizer.transform(structs)
        logger.info("doing clusterizer step")
        labels = self.clusterizer.predict(vecs)
        logger.info("doing seeker step")
        neighbors_inds = self.seeker.neighbors(vecs, labels)
        answer = []
        for i, neighbors_ind in enumerate(neighbors_inds):
            if neighbors_ind.size:
                answer.append(self._train_ind[neighbors_ind])
            else:
                logger.debug("empty set of neighbors for {}".format(codes[i]))
                answer.append([])
        return answer
