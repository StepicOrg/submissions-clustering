import logging.config

from subsclu.utils import dump as dump_utils
from subsclu.utils import read as read_utils


def make_model_path(language, approach, nrows):
    return "data/model_{}_{}_{}.dump".format(language, approach, nrows or "all")


def run():
    language, approach = "python", "ast"
    data_path, nrows = "data/subs.sl3", 3000

    submissions = list(read_utils.from_sl3(data_path, nrows=nrows))

    # model = sc.SubmissionsClustering.outof(language, approach)
    # model.fit(submissions)

    presaved_model_path = make_model_path(language, approach, nrows)
    model = dump_utils.pickle_load(presaved_model_path)

    """
    scorer = scorers.from_spec(language, test_approach)
    presaved_score_path = "data/score_{}_{}_{}.dump".format(language, test_approach, nrows or "all")
    score = scorer.score(model, submissions, presaved_score_path)
    print("score={}".format(score))
    """


def main():
    logging.basicConfig(
        level=logging.ERROR,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    logger = logging.getLogger(__name__)
    logger.info("start running")
    run()
    logger.info("finishing running")


if __name__ == '__main__':
    main()
