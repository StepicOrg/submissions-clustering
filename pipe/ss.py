from collections import namedtuple
from itertools import takewhile

import pandas as pd
from sklearn.cluster import MiniBatchKMeans
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.neighbors import NearestNeighbors
from sklearn.pipeline import make_pipeline
from sklearn.neighbors.base import NeighborsBase

from .cookers import *
from .preprocessor import Preprocessor


class Seeker:
    def __init__(self, *, insider_cluster=False, start_from_center=False, only_centroids=True,
                 max_c=200, dist_c=1., cmax_c=20, cdist_c=.1):
        self.inside_cluster = insider_cluster
        self.start_from_center = start_from_center
        self.only_centroids = only_centroids
        self.max_c = max_c
        self.dist_c = dist_c
        self.cmax_c = cmax_c
        self.cdist_c = cdist_c


class Method(namedtuple("Method", ["vectorizer", "clusterizer", "seeker"])):
    @staticmethod
    def from_predefined(language, approach):
        if language == "python" and approach == "diff":
            return Method(vectorizer=make_pipeline(Preprocessor(language="python", method="tokenize"),
                                                   BagOfNgrams(ngram_range=(1, 2)),
                                                   TfidfTransformer()),
                          clusterizer=MiniBatchKMeans(n_clusters=20),
                          seeker=Seeker())
        else:
            raise ValueError("No such method supported yet")


class SubmissionsSimilarity(BaseEstimator):
    def __init__(self, *, method, parralel=False):
        self.method = method
        self.parralel = parralel

        self.submissions = pd.DataFrame(columns=["code", "status"])

    def _del_submissions(self):
        self.submissions.drop(self.submissions.index, inplace=True)

    @staticmethod
    def _norm_submission(submission):
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

    def _add_submissions(self, submissions):
        submissions = (self._norm_submission(submission) for submission in submissions)
        self.submissions = self.submissions.append(
            pd.DataFrame.from_records(submissions, columns=list(self.submissions.columns)),
            ignore_index=True
        )

    @staticmethod
    def _find_centers(X, y):
        c = []
        for label in range(y.max() + 1):
            c.append(X[y == label].mean(axis=0).tolist())
        return np.array(c)

    def fit(self, submissions):
        # pre stage
        self._add_submissions(submissions)
        data = self.submissions
        vectorizer, clusterizer, seeker = self.method

        # vectoring and remove redundant (incorrect) data
        X = vectorizer.fit_transform(data["code"]).toarray()
        if "preprocessor" in vectorizer.named_steps:
            data = data.iloc[vectorizer.named_steps["preprocessor"].correct_index].reset_index(drop=True)

        # clustering
        if clusterizer is not None:
            y = clusterizer.fit_predict(X).astype(int)
        else:
            y = -np.ones(len(data), dtype=int)

        # find centers
        c = self._find_centers(X, y)

        # leave only correct
        correct = data["status"] == "correct"
        data = data.loc[correct, "code"].values
        X, y = X[correct], y[correct]

        # drop non centroids
        n_jobs = -1 if self.parralel else 1
        if seeker.only_centroids:
            no_cluster = y == -1
            new_data, new_X, new_y = list(data[no_cluster]), list(X[no_cluster]), list(y[no_cluster])
            cmax_c, cdist_c = seeker.cmax_c, seeker.cdist_c
            for label in range(len(c)):
                train = y == label
                if sum(train) != 0:
                    data_train, X_train, y_train = data[train], X[train], y[train]
                    nn = NearestNeighbors(n_neighbors=min(sum(train), cmax_c), n_jobs=n_jobs)
                    nn.fit(X_train)
                    dist, ind = nn.kneighbors(c[label][np.newaxis, :])
                    ind = list(map(lambda x: x[1], takewhile(lambda x: x[0] <= cdist_c, zip(dist[0], ind[0]))))
                    new_data.extend(data_train[ind])
                    new_X.extend(X_train[ind])
                    new_y.extend(y_train[ind])
            data, X, y = np.array(new_data), np.array(new_X), np.array(new_y)

        # TODO: ...

        pass

    def refit(self, submissions):
        self._del_submissions()
        self.fit(submissions)
