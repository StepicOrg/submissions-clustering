from sc.sc import SubmissionsClustering
from sc.utils.code_gens import from_csv


def main():
    sc = SubmissionsClustering.from_str("python", "diff")
    df = list(from_csv("data/step-12768-submissions.csv", columns=["code", "status"], nrows=100))
    sc.fit(df)
    # codes = list(map(lambda x: x[0], df))
    # n = sc.neighbors(codes)
    # print(list(map(lambda x: len(x), n)))
    # print(list(map(len, codes)))


if __name__ == '__main__':
    main()
