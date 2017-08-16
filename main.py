from timeit import timeit

from sc import sc_from_spec
from sc.scorers import scorer_from_spec
from sc.utils import pickler
from sc.utils import read_subs


def score():
    sc = sc_from_spec("python", "diff")
    sc.fit(*read_subs.from_sl3("data/subs.sl3", nrows=1000))

    scorer = scorer_from_spec("python", "diff")
    sc.score_with(scorer)


def time():
    print(timeit(lambda: read_subs.from_sl3("data/subs.sl3"), number=3))
    print(timeit(lambda: read_subs.from_csv("data/step-12768-submissions.csv"), number=3))


def main():
    sc = sc_from_spec("python", "diff")
    codes, statuses = read_subs.from_sl3("data/subs.sl3", nrows=10000)
    sc.fit(codes, statuses)
    print("BEGIN")
    print(timeit(lambda: pickler.pickle(sc, "data/sc.dump"), number=1))

    del sc
    sc = pickler.unpickle("data/sc.dump")
    print(len(sc.neighbors([codes[0]])[0]))

    # plotter = plotter_from_spec("plotly")
    # sc.plot_with(plotter, title="Test plot", path="plots/temp_plot.html")


if __name__ == '__main__':
    # score()
    # time()
    main()
