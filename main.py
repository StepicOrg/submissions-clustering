from timeit import timeit

from sc import sc_from_spec
from sc.plotters import plotter_from_spec
from sc.scorers import scorer_from_spec
from sc.utils import read_subs


def score():
    diff_scorer = scorer_from_spec("python", "diff")
    token_scorer = scorer_from_spec("python", "token")
    ast_scorer = scorer_from_spec("python", "ast")

    src = "a=3"
    dst = "g=4"
    print(diff_scorer.score(src, dst))
    print(token_scorer.score(src, dst))
    print(ast_scorer.score(src, dst))


def time():
    print(timeit(lambda: read_subs.from_sl3("data/subs.sl3"), number=3))
    print(timeit(lambda: read_subs.from_csv("data/step-12768-submissions.csv"), number=3))


def main():
    sc = sc_from_spec("python", "test")
    codes, statuses = read_subs.from_csv("data/step-12768-submissions.csv", nrows=1000)
    print(len(sc.fit_neighbors(codes, statuses)[0]))

    plotter = plotter_from_spec("plotly")
    sc.plot_with(plotter, title="Test plot", path="plots/temp_plot.html")


if __name__ == '__main__':
    score()
    # time()
    # main()
