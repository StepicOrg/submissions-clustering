import numpy as np
import pandas as pd
from sklearn.neighbors import NearestNeighbors
from tqdm import tqdm

from .metrics import ratio


def find_centroids(X, y):
    c = []
    for label in range(0, y.max() + 1):
        c.append(X[y == label].mean(axis=0))
    return np.array(c)


def score_ratio(transform, *, cluster=None, method="nn", max_c=100, dist_c=1., leaf_size=10,
                dataset="data/step-12768-submissions-with-ratio.csv", nrows=None):
    X = pd.read_csv(dataset, nrows=nrows)
    vecs = transform.fit_transform(X["code"]).toarray()
    X = X.iloc[transform.named_steps["pre"].icorrect]
    if cluster is not None and method != "nn":
        X["labels"] = cluster.fit_predict(vecs).astype(np.int)
    else:
        X["labels"] = -np.ones(X.shape[0]).astype(np.int)

    if method == "centroid":
        for label, centroid in enumerate(find_centroids(vecs, X["labels"].values)):
            vecs[X["labels"] == label] = centroid

    diff_ratios = []
    for y in tqdm(range(X["labels"].min(), X["labels"].max() + 1)):
        train = X["status"] == "correct" if y == -1 else (X["status"] == "correct") & (X["labels"] == y)
        test = (X["status"] != "correct") & (X["labels"] == y)
        train_vecs, test_vecs = vecs[train], vecs[test]
        train_X, test_X = X[train], X[test]
        if sum(train) == 0 or sum(test) == 0:
            est_ratios = np.zeros(sum(test))
        else:
            nn = NearestNeighbors(n_neighbors=min(max_c, train_vecs.shape[0]), n_jobs=-1, leaf_size=leaf_size)
            nn.fit(train_vecs)
            dist, ind = nn.kneighbors(test_vecs)
            est_ratios = []
            for code, est_dist, est_ind in zip(tqdm(test_X["code"]), dist, ind):
                est_ind = [i for d, i in zip(est_dist, est_ind) if d <= dist_c]
                est_ratios.append(ratio(code, train_X.iloc[est_ind]["code"]))
            est_ratios = np.array(est_ratios)
        diff_ratios.extend((test_X["best_ratio"] - est_ratios).tolist())

    return np.array(diff_ratios).mean()
