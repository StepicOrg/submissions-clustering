import sc
from sc import plotters
from sc import utils


def main():
    snn = sc.from_spec("python", "diff")
    codes, statuses = utils.from_csv("data/step-12768-submissions.csv", nrows=1000)
    snn.fit(codes, statuses)

    plotter = plotters.from_spec("plotly2d")
    snn.plot_with(plotter, title="Test plot", path="plots/temp_plot.html")


if __name__ == '__main__':
    main()
