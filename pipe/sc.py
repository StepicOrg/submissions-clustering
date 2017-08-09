import pandas as pd
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.pipeline import make_pipeline

from .clusterizers import *
from .cookers import *
from .preprocessor import Preprocessor
from .seekers import Seeker
from .utils.preprocessing import find_centers


def norm_submission(submission):
    if isinstance(submission, tuple) and len(submission) == 2:
        return submission
    elif isinstance(submission, str):
        return submission, "correct"
    elif hasattr(submission, "code"):
        return submission.code, submission.status if hasattr(submission, "status") else "correct"
    elif hasattr(submission, "__getitem__") and "code" in submission:
        return submission["code"], submission["status"] if "status" in submission else "correct"
    else:
        try:
            return str(submission), "correct"
        except Exception as e:
            raise ValueError("Wrong submission form") from e


class SubmissionsClustering(BaseEstimator):
    def __init__(self, *, vectorizer, clusterizer, seeker):
        self.vectorizer = vectorizer
        self.clusterizer = clusterizer
        self.seeker = seeker

        self._submissions = pd.DataFrame(columns=["code", "status"])

    def _del_submissions(self):
        self._submissions.drop(self._submissions.index, inplace=True)

    @staticmethod
    def from_predefined(language, approach):
        if language == "python" and approach == "diff":
            return SubmissionsClustering(
                vectorizer=make_pipeline(
                    Preprocessor(language="python", method="tokenize"),
                    BagOfNgrams(ngram_range=(1, 2)),
                    TfidfTransformer(),
                    DenseTransformer()
                ),
                clusterizer=StupidClusterizer(),
                seeker=Seeker.from_predefined("nn")
            )
        else:
            raise ValueError("No such language and approach supported yet")

    def _add_submissions(self, submissions):
        submissions = (norm_submission(submission) for submission in submissions)
        self._submissions = self._submissions.append(
            pd.DataFrame.from_records(submissions, columns=list(self._submissions.columns)),
            ignore_index=True
        )

    def fit(self, submissions):
        # pre stage
        self._add_submissions(submissions)
        data = self._submissions

        # vectorizer
        X = self.vectorizer.fit_transform(data["code"]).toarray()
        if "preprocessor" in self.vectorizer.named_steps:
            data = data.iloc[vectorizer.named_steps["preprocessor"].correct_index].reset_index(drop=True)

        # clusterizer
        if self.clusterizer is not None:
            y = self.clusterizer.fit_predict(X).astype(int)
        else:
            y = -np.ones(X.shape[0], dtype=int)

        # seeker
        self.seeker.fit(X[data.status == "correct"], y[data.status == "correct"], find_centers(X, y))

    def refit(self, submissions):
        self._del_submissions()
        self.fit(submissions)

    def _gather_correct(self, indices):
        correct_submissions = self._submissions[self._submissions.status == "correct", "codes"]
        codes = []
        for i in indices:
            codes.append(correct_submissions.iloc[i].tolist())
        return codes

    def neighbors(self, codes):
        """Give neighbors for each code sample in the input.

        :param codes: code samples
        :type codes: list[str]
        
        :return: neighbors for each code sample
        :rtype: list[list[str]]
        """
        X = self.vectorizer.transform(codes)
        y = self.clusterizer.predict(X)
        i = self.seeker.neighbors(X, y)
        return self._gather_correct(i)
