from itertools import repeat

import pandas as pd

from sc.pipe.bases import BaseEstimator, NeighborsMixin
from sc.utils.matrix import find_centers

__all__ = ["SubmissionsClustering"]


class SubmissionsClustering(BaseEstimator, NeighborsMixin):
    def __init__(self, preprocessor, vectorizer, clusterizer, seeker):
        self.preprocessor = preprocessor
        self.vectorizer = vectorizer
        self.clusterizer = clusterizer
        self.seeker = seeker

        self.__submissions = None

    def __add_submissions(self, codes, statuses):
        submissions = zip(codes, statuses or repeat("correct"))
        self.__submissions = pd.DataFrame(
            columns=["code", "status"]) if self.__submissions is None else self.__submissions
        self.__submissions = self.__submissions.append(
            pd.DataFrame.from_records(submissions, columns=list(self.__submissions.columns)),
            ignore_index=True
        )

    def __del_submissions(self):
        self.__submissions.drop(self.__submissions.index, inplace=True)

    def fit(self, codes, statuses=None):
        """Fit model with past submissions plus new codes and statuses.

        :param codes: code samples
        :type codes: list[str]
        :param statuses: submissions status of samples, either "correct" or something else
        :type statuses: None | list[str]

        :return: self
        :rtype: SubmissionsClustering
        """
        self.__add_submissions(codes, statuses)
        data = self.__submissions
        ci, s = self.preprocessor.fit_sanitize(data["code"].tolist())
        X = self.vectorizer.fit_transform(s)
        y = self.clusterizer.fit_predict(X)
        mask = data.loc[ci].status == "correct"
        self.seeker.fit(X[mask], y[mask], find_centers(X, y), ci[mask])
        return self

    def refit(self, codes, statuses=None):
        """Same as .fit, just deleting previosly submissions.

        :param codes: code samples
        :type codes: list[str]
        :param statuses: submissions status of samples, either "correct" either something else
        :type statuses: None | list[str]

        :return: self
        :rtype: SubmissionsClustering
        """
        self.__del_submissions()
        return self.fit(codes, statuses)

    def __gather_neighbors(self, n, ci, nci):
        codes = self.__submissions.code.values
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
        return self.__gather_neighbors(len(codes), ci, I)

    def plot_with(self, plotter, title, path):
        data = self.__submissions
        ci, s = self.preprocessor.sanitize(data["code"].tolist())
        X = self.vectorizer.transform(s)
        y = self.clusterizer.predict(X)
        centers = self.clusterizer.centers_ if hasattr(self.clusterizer, "centers_") else find_centers(X, y)
        centroids = self.clusterizer.centroids_ if hasattr(self.clusterizer, "centroids_") else None
        codes = data.loc[ci].code
        statuses = data.loc[ci].status
        plotter.plot(X, y, centers=centers, centroids=centroids,
                     codes=codes, statuses=statuses, title=title, path=path)
