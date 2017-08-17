from timeit import timeit

import sc
from sc import utils


def main():
    snn = sc.from_spec("python", "diff")
    subs = list(utils.from_sl3("data/subs.sl3", nrows=1000))
    snn.fit(subs)
    print("BEGIN")
    print(timeit(lambda: snn.save("data/snn.dump"), number=1))
    del snn

    print("END")
    print(timeit(lambda: sc.SubmissionsClustering.load("data/snn.dump"), number=1))

    """
    snn = SubmissionsClustering.load("data/snn.dump")
    single = subs[0][0]
    neighbors = snn.neighbors([single])[0]
    print(neighbors[:5])
    """


if __name__ == '__main__':
    main()
