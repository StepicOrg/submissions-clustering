import subsclu
from subsclu.utils import read as read_utils


def main():
    sc = subsclu.from_spec("python", "diff")
    subs = list(read_utils.from_sl3("data/subs.sl3", nrows=1000))
    sc.fit(subs)
    print(len(sc.neighbors([subs[0][0]])[0]))


if __name__ == '__main__':
    main()
