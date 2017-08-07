from sklearn.base import BaseEstimator

METHODS = {
    "diff": None
}


class SubmissionsSimilarity(BaseEstimator):
    def __init__(self, *, language="python", method="diff"):
        self.language = language
        self.method = method

    def fit(self, X):
        # X is either gen or iterable of strs
        pass
