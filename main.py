import logging.config
import os

import subsclu as sc
from subsclu.scorers import Scorer
from subsclu.utils import dump as dump_utils
from subsclu.utils import read as read_utils


def make_model_path(language, approach, nrows):
    return "data/model_{}_{}_{}.dump" \
        .format(language, approach, nrows or "all")


def make_score_path(language, approach, nrows):
    return "data/score_{}_{}_{}.dump" \
        .format(language, approach, nrows or "all")


def run():
    # params
    language, approach = "python", "test"
    data_path, nrows = "data/subs.sl3", 1000
    test_approach = "diff"
    model_seek_path, model_save_path = False, False

    # make fitted model
    submissions = list(read_utils.from_sl3(data_path, nrows=nrows))
    presaved_model_path = make_model_path(language, approach, nrows)
    if model_seek_path and os.path.exists(presaved_model_path):
        model = dump_utils.pickle_load(presaved_model_path)
    else:
        model = sc.SubmissionsClustering.outof(language, approach)
        model.fit(submissions)
        if model_save_path:
            dump_utils.pickle_save(model, presaved_model_path)

    # score
    presaved_score_path = make_score_path(language, test_approach, nrows)
    scorer = Scorer.outof(language, test_approach)
    score = scorer.score(model, submissions, presaved_score_path)
    print("score {}".format(score))


def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    logger = logging.getLogger(__name__)
    logger.info("start running")
    run()
    logger.info("finishing running")


if __name__ == '__main__':
    main()
