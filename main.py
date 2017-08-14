def test():
    def f():
        pass

    a = BunchOfMethods(f)
    print("kek" in a)


def plot():
    sc = SubmissionsClustering.from_str("python", "diff")
    codes, statuses = utils.from_csv("data/step-12768-submissions.csv", nrows=1000)
    sc.fit(codes, statuses)

    plotter = plotters.from_spec("plotly")
    sc.plot_with(plotter, title="Test plotting", path="plots/temp_plot.html")


def main():
    sc = SubmissionsClustering.from_str("python", "diff")
    codes, statuses = utils.from_csv("data/step-12768-submissions.csv", nrows=1000)
    print(len(sc.fit_neighbors(codes, statuses)[0]))


if __name__ == '__main__':
    test()
    # plot()
    # main()
