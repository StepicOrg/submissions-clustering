import sc
from sc import plotters
from sc import utils
from timeit import timeit


def time():
    print(timeit(lambda: utils.from_sl3("data/subs.sl3"), number=3))
    print(timeit(lambda: utils.from_csv("data/step-12768-submissions.csv"), number=3))


def main():
    snn = sc.from_spec("python", "test")
    codes, statuses = utils.from_csv("data/step-12768-submissions.csv", nrows=1000)
    print(len(snn.fit_neighbors(codes, statuses)[0]))

    # plotter = plotters.from_spec("plotly2d")
    # snn.plot_with(plotter, title="Test plot", path="plots/temp_plot.html")


if __name__ == '__main__':
    time()
    # main()
