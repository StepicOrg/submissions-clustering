import logging
import os

import numpy as np
import pandas as pd
from tqdm import tqdm

from subsclu.utils.dump import default_load, default_save
from subsclu.utils.read import split_into_lists
from .base import BaseScorer

logger = logging.getLogger(__name__)


def _distplot(dist):
    import matplotlib as mpl
    mpl.use('Agg')
    import matplotlib.pyplot as plt
    import seaborn as sns
    sns.distplot(dist)
    plt.show()


class ErrorScorer(BaseScorer):
    def __init__(self, metric):
        self.metric = metric

    def score(self, model, submissions, presaved_path=None, plot_errors=False):
        logger.info("start scoring")
        codes, statuses = split_into_lists(submissions)
        codes, statuses = pd.Series(codes), pd.Series(statuses)
        correct_codes, wrong_codes = codes[statuses == "correct"], codes[statuses != "correct"]
        ogger.debug("num of correct = {}, num of wrong = {}".format(len(correct_codes), len(wrong_codes)))

        def neighbors_codes(neighbors_ind):
            return codes.iloc[neighbors_ind].tolist()

        if presaved_path is not None and os.path.exists(presaved_path):
            logging.info("restoring best metrics from {}".format(presaved_path))
            best_metrics = default_load(presaved_path)
        else:
            logging.info("can't restore best metrics, start recalculating it")
            best_metrics = []
            for code in tqdm(wrong_codes):
                best_metrics.append(self.metric.best_metric(code, correct_codes))
            best_metrics = np.array(best_metrics)
            logging.info("finishing calculating best metrics")
            logging.debug("mean = {}".format(best_metrics.mean()))
            if presaved_path is not None:
                logging.info("saving best metrics to {}".format(presaved_path))
                default_save(best_metrics, presaved_path)

        logging.info("start calculating local best metrics")
        local_best_metrics = []
        for code, neighbors_ind in zip(tqdm(wrong_codes), model.neighbors(wrong_codes)):
            local_best_metrics.append(
                self.metric.best_metric(code, neighbors_codes(neighbors_ind))
            )
        local_best_metrics = np.array(local_best_metrics)
        logging.info("finishing calculating local best metrics")

        errors = best_metrics - local_best_metrics
        if plot_errors:
            logger.info("plot error distribution plot")
            _distplot(errors)
        return errors.mean()
