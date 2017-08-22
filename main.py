import logging.config

from subsclu.utils import dump as dump_utils
from subsclu.utils import read as read_utils


def run():
    language, train_approach, test_approach = "python", "ast", "diff"
    train_data_path, nrows = "data/subs.sl3", 3000

    submissions = read_utils.from_sl3(train_data_path, nrows=nrows)
    submissions = list(read_utils.filter_out_invalid(submissions, language))

    presaved_model_path = "data/model_{}_{}_{}.dump".format(language, train_approach, nrows or "all")
    # model = subsclu.from_spec(language, train_approach)
    # model.fit(submissions)
    # dump_utils.pickle_save(model, presaved_model_path)
    model = dump_utils.pickle_load(presaved_model_path)

    """
    scorer = scorers.from_spec(language, test_approach)
    presaved_score_path = "data/score_{}_{}_{}.dump".format(language, test_approach, nrows or "all")
    score = scorer.score(model, submissions, presaved_score_path)
    print("score= {}".format(score))
    """


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
