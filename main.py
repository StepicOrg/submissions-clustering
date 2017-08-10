from sc.sc import SubmissionsClustering
from sc.utils import from_csv


def main():
    sc = SubmissionsClustering.from_str("python", "diff")
    codes, statuses = from_csv("data/step-12768-submissions.csv", nrows=1000)
    print(len(sc.fit_neighbors(codes, statuses)[0]))


if __name__ == '__main__':
    main()
