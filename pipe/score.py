import numpy as np
import pandas as pd

from sklearn.neighbors import NearestNeighbors


def score_ratio(transform, *, cluster=None, method="nn", max_c=1000, dist_c=1.,
                dataset="data/step-12768-submissions-with-ratio.csv", nrows=None):
    X = pd.read_csv(dataset, nrows=nrows)
    vecs = transform.fit_transform(X["code"])
    X = X.iloc[transform.named_steps["pre"].icorrect]
    if cluster is not None and method != "nn":
        X["labels"] = cluster.fit_predict(vecs)
    else:
        X["labels"] = np.zeros(X.shape[0])
    # TODO: label can be -1 !!!

    nns = []
    for y in range(int(X["labels"].max()) + 1):
        y_vecs = vecs[(X["status"] == "correct") & (X["labels"] == y)]
        nn = NearestNeighbors(n_neighbors=max_c, radius=dist_c, n_jobs=-1)
        if min(y_vecs.shape) != 0:
            nn.fit(y_vecs)
        nns.append(nn)

    if method == "centers":
        # TODO: find centers for clustering?
        pass

    correct_ind = X["status"] == "correct"
    wrong_ind = ~correct_ind
    correct_X, correct_vecs = X[correct_ind], vecs[correct_ind]
    wrong_X, wrong_vecs = X[wrong_ind], vecs[wrong_ind]

    diff_ratios = []
    for vec, x in zip(wrong_vecs, wrong_X):
        pass
        estimate_ratio = 1.
        diff_ratios.append(best_ratio - estimate_ratio)

    for vec, label, status, best_ratio in zip(wrong_vecs, wrong_X["labels"], wrong_X["status"], wrong_X["best_ratio"]):
        if status != "correct":
            # TODO:
            if method == "nn":
                pass
            elif method == "cluster":
                pass
            elif method == "centers":
                pass
            else:
                raise ValueError("Such method is't supported yet")
            estimate_ratio = 1.
            diff_ratios.append(best_ratio - estimate_ratio)

    return np.array(diff_ratios).mean()
