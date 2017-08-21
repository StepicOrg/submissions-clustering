import subsclu
from subsclu import scorers
from subsclu.utils import read as read_utils


def main():
    model = subsclu.from_spec("python", "test")
    submissions = read_utils.from_sl3("data/subs.sl3", nrows=1000)
    submissions = list(read_utils.filter_out_invalid(submissions, "python"))
    model.fit(submissions)

    scorer = scorers.from_spec("python", "diff")
    score = scorer.score(
        model, submissions,
        presaved_path="data/python_diff_1000.dump"
    )
    print(score)


if __name__ == '__main__':
    main()
