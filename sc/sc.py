import pandas as pd

from sc.pipe import *
from sc.utils import find_centers


class SubmissionsClustering(BaseEstimator):
    def __init__(self, preprocessor, vectorizer, clusterizer, seeker):
        self.preprocessor = preprocessor
        self.vectorizer = vectorizer
        self.clusterizer = clusterizer
        self.seeker = seeker

        self._submissions = None

    @staticmethod
    def from_str(language, approach):
        if language == "python" and approach == "diff":
            return SubmissionsClustering(
                preprocessor=SimplePreprocessor(
                    language="python", method="tokenize"
                ),
                vectorizer=make_pipeline(
                    BagOfNgrams(ngram_range=(1, 2)),
                    TfidfTransformer(),
                    DenseTransformer()
                ),
                clusterizer=StupidClusterizer(),
                seeker=NNSeeker()
            )
        else:
            raise ValueError("No such language and approach supported yet")

    @staticmethod
    def norm_submission(submission):
        if isinstance(submission, tuple) and len(submission) == 2:
            return submission
        elif isinstance(submission, str):
            return submission, "correct"
        else:
            try:
                return str(submission), "correct"
            except Exception as e:
                raise ValueError("Wrong submission form") from e

    def _add_submissions(self, submissions):
        self._submissions = pd.DataFrame(columns=["code", "status"]) if self._submissions is None else self._submissions
        submissions = (self.norm_submission(submission) for submission in submissions)
        self._submissions = self._submissions.append(
            pd.DataFrame.from_records(submissions, columns=list(self._submissions.columns)),
            ignore_index=True
        )

    def _del_submissions(self):
        self._submissions.drop(self._submissions.index, inplace=True)

    def fit(self, submissions):
        self._add_submissions(submissions)
        data = self._submissions
        ci, s = self.preprocessor.fit_sanitize(data["code"].tolist())
        X = self.vectorizer.fit_transform(s)
        y = self.clusterizer.fit_predict(X)
        mask = data.loc[ci].status == "correct"
        self.seeker.fit(X[mask], y[mask], find_centers(X, y), ci[mask])

    def refit(self, submissions):
        self._del_submissions()
        self.fit(submissions)

    def _gather_neighbors(self, n, ci, nci):
        codes = self._submissions.code.values
        ans = [[]] * n
        for i, n in zip(ci, nci):
            ans[i] = codes[n].tolist()
        return ans

    def neighbors(self, codes):
        """Give neighbors for each code sample in the input.

        :param codes: code samples
        :type codes: list[str]
        
        :return: neighbors for each code sample
        :rtype: list[list[str]]
        """
        ci, s = self.preprocessor.sanitize(codes)
        X = self.vectorizer.transform(s)
        y = self.clusterizer.predict(X)
        I = self.seeker.neighbors(X, y)
        return self._gather_neighbors(len(codes), ci, I)
