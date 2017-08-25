"""Importing clusterizers from sklearn."""

from sklearn.cluster import MiniBatchKMeans, AffinityPropagation, DBSCAN

__all__ = ["MiniBatchKMeans", "AffinityPropagation", "MyDBSCAN"]


class MyDBSCAN(DBSCAN):
    """DBSCAN + predict method."""

    def predict(self, vecs):
        """Predict labels for vecs."""
        return self.fit_predict(vecs)
