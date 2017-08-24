"""Implementation of error scorer."""

import logging
import os

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from tqdm import tqdm

from subsclu.scorers.base import Scorer
from subsclu.utils.dump import default_load, default_save
from subsclu.utils.read import split_into_lists

__all__ = ["ErrorScorer"]

logger = logging.getLogger(__name__)


class ErrorScorer(Scorer):
    """Error scorer."""

    def __init__(self, metric):
        """Create instance of scorer with given metric.

        Args:
            metric: Metric to metric.
        """
        self.metric = metric

    @staticmethod
    def _split(submissions):
        # split submissions into correct and wrong
        logger.info("start scoring")
        codes, statuses = split_into_lists(submissions)
        codes, statuses = pd.Series(codes), pd.Series(statuses)
        correct_codes = codes[statuses == "correct"]
        wrong_codes = codes[statuses != "correct"]
        logger.debug("num of correct %s, num of wrong %s",
                     len(correct_codes), len(wrong_codes))

        # func for get neighbors codes from indicies
        def neighbors_codes(neighbor_indicies):
            """Give codes at indicies."""
            return codes.iloc[neighbor_indicies].tolist()

        return correct_codes, wrong_codes, neighbors_codes

    def _local_best_metrics(self, model, neighbors_codes, wrong_codes):
        # calculating local best metrics
        logging.info("calculating local best metrics")
        local_best_metrics = []
        for code, neighbor_indicies in zip(
                tqdm(wrong_codes),
                model.neighbors(wrong_codes)
        ):
            local_best_metrics.append(
                self.metric.best_metric(
                    code,
                    neighbors_codes(neighbor_indicies)
                )
            )
        local_best_metrics = np.array(local_best_metrics)
        logging.info("finishing calculating local best metrics")
        return local_best_metrics

    def _best_metrics(self, correct_codes, presaved_path, wrong_codes):
        # calculating best metrics
        logger.info("calculating best metrics")
        if presaved_path is not None and os.path.exists(presaved_path):
            logging.info("restoring best metrics from %s", presaved_path)
            best_metrics = default_load(presaved_path)
        else:
            logging.info("can't restore best metrics, start recalculating it")
            best_metrics = []
            for code in tqdm(wrong_codes):
                best_metrics.append(
                    self.metric.best_metric(code, correct_codes)
                )
            best_metrics = np.array(best_metrics)
            logging.info("finishing calculating best metrics")
            logging.debug("mean %s", best_metrics.mean())
            if presaved_path is not None:
                logging.info("saving best metrics to %s", presaved_path)
                default_save(best_metrics, presaved_path)
        return best_metrics

    @staticmethod
    def _errors(best_metrics, local_best_metrics, plot_errors):
        # calculating errors
        logger.info("calculating errors")
        errors = best_metrics - local_best_metrics
        if plot_errors:
            logger.info("plot error distribution plot")
            sns.distplot(errors)
            plt.show()
        return errors

    def score(self, model, submissions, presaved_path=None, plot_errors=False):
        # pylint: disable=arguments-differ
        """See :func:`subsclu.scorers.base.Scorer.score`."""
        # split
        correct_codes, wrong_codes, neighbors_codes = self._split(submissions)
        # best_metrics
        best_metrics = self._best_metrics(
            correct_codes, presaved_path, wrong_codes
        )
        # local_best_metrics
        local_best_metrics = self._local_best_metrics(
            model, neighbors_codes, wrong_codes
        )
        # errors
        errors = self._errors(best_metrics, local_best_metrics, plot_errors)
        # return
        return errors.mean()
