# from sc.sc import SubmissionsClustering
# from sc import utils
# from sc.pipe.commons import reducers as rdc
from sc.pipe.commons import reducers


def test():
    reducer = reducers.from_spec("pca", 10)
    print(reducer)


def main():
    sc = SubmissionsClustering.from_str("python", "diff")
    codes, statuses = utils.from_csv("data/step-12768-submissions.csv", nrows=1000)
    print(len(sc.fit_neighbors(codes, statuses)[0]))


if __name__ == '__main__':
    test()
    # main()
