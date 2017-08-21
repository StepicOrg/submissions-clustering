import subsclu
from subsclu.utils import read as read_utils


def main():
    model = subsclu.from_spec("python", "diff")
    submissions = read_utils.from_sl3("data/subs.sl3", nrows=1000)
    submissions = list(read_utils.filter_out_invalid(submissions, "python"))
    model.fit(submissions)
    print(model.neighbors([submissions[0][0]])[0].shape)


if __name__ == '__main__':
    main()
