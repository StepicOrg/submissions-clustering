from sc import plotters
from sc import utils
from sc.sc import SubmissionsClustering


def test():
    sc = SubmissionsClustering.from_str("python", "diff")
    codes, statuses = utils.from_csv("data/step-12768-submissions.csv", nrows=1000)
    sc.fit(codes, statuses)

    plotter = plotters.from_spec("plotly2d")
    sc.plot_with(plotter)


def main():
    sc = SubmissionsClustering.from_str("python", "diff")
    codes, statuses = utils.from_csv("data/step-12768-submissions.csv", nrows=1000)
    print(len(sc.fit_neighbors(codes, statuses)[0]))


if __name__ == '__main__':
    test()
    # main()
