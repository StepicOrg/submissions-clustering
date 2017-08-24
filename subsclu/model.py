"""Main module implementation."""

import logging

import numpy as np
import pandas as pd

from subsclu.pipe.bases import BaseEstimator, NeighborsMixin
from subsclu.utils import iter as iter_utils
from subsclu.utils import matrix as matrix_utils
from subsclu.utils import read as read_utils
from subsclu.utils.dump import LoadSaveMixin

__all__ = ["SubmissionsClustering"]

logger = logging.getLogger(__name__)


class SubmissionsClustering(BaseEstimator, NeighborsMixin, LoadSaveMixin):
    """Main model, combining all 4 steps in one pipeline."""

    def __init__(self, preprocessor, vectorizer, clusterizer, seeker):
        """Create instance of model with 4 steps.

        Args:
            preprocessor: Preprocessor step.
            vectorizer: Vectorizer step.
            clusterizer: Clusterizer step.
            seeker: Seeker step.
        """
        self.preprocessor = preprocessor
        self.vectorizer = vectorizer
        self.clusterizer = clusterizer
        self.seeker = seeker

        self._correct_indicies = None

    def fit(self, submissions):
        """Fit model using input sumbissions data.

        Args:
            submissions (Iterable[(str, str)]): Submissions to fit. Each sample
                should be a 2-tuple of (code, status) strings.

        Returns:
            Returns self.

        """
        # split input submissions iterable into codes and statuses lists
        codes, statuses = read_utils.split_into_lists(submissions)

        # fit them into preprocessor step, getting correct indicies and
        # transformed structs at that indicies
        logger.info("fitting preprocessor step")
        checked_indicies, structs = self.preprocessor.fit_sanitize(codes)

        # we can now do vectorizing and labeling for structs, cause we loose
        # any info about language, we just have structs of int codes
        logger.info("fitting vectorizer step")
        vecs = self.vectorizer.fit_transform(structs)
        logger.info("fitting clusterizer step")
        labels = self.clusterizer.fit_predict(vecs)

        # filter out unchecked code, getting correct statuses
        checked_statuses = iter_utils.select_at(statuses, checked_indicies)
        checked_statuses = pd.Series(list(checked_statuses))
        train_statuses = checked_statuses[checked_statuses == "correct"]
        train_indicies = train_statuses.index.values
        logger.debug("num of correct codes %s", len(train_indicies))

        # saving correct code indicies to be able to get original indicies back
        self._correct_indicies = checked_indicies[train_indicies]

        # fit seecker model
        logger.info("fitting seeker step")
        self.seeker.fit(
            vecs=vecs[train_indicies],
            labels=labels[train_indicies],
            centers=matrix_utils.find_centers(vecs, labels)
        )

        # return self, as usual fit do
        return self

    def neighbors(self, codes):
        """Give neighbor indicies for each code sample.

        Args:
            codes (Iterable[str]): Code to find neighbors to.

        Returns:
            List of neighbor indicies for each code sample.

        """
        # feed given codes directly to preprocessor
        codes = list(codes)
        logger.info("doing preprocessor step")
        checked_indicies, structs = self.preprocessor.sanitize(codes)

        # struct are now be able to get vecs, labels and neighbors
        logger.info("doing vectorizer step")
        vecs = self.vectorizer.transform(structs)
        logger.info("doing clusterizer step")
        labels = self.clusterizer.predict(vecs)
        logger.info("doing seeker step")
        neighbors = self.seeker.neighbors(vecs, labels)

        # shift correct neighbors back to original indicies
        neighbors_indicies = matrix_utils.shift_indicies(
            arrays=neighbors,
            shift=self._correct_indicies
        )

        # construct answer, filling gaps with empty arrays
        answer = matrix_utils.fill_gaps(
            indicies=checked_indicies,
            elementss=neighbors_indicies,
            size=len(codes),
            gap=lambda: np.empty(0)
        )

        # return answer
        return answer

    @staticmethod
    def outof(*args, **kwargs):
        """See :func:`subsclu.spec.model_from_spec`."""
        from subsclu.spec import model_from_spec
        return model_from_spec(*args, **kwargs)
