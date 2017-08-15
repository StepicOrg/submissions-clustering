from itertools import takewhile

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from sklearn.neighbors import NearestNeighbors
from tqdm import tqdm

from .__metrics import ratio


def find_centers(X, y):
    c = []
    for label in range(y.max() + 1):
        c.append(X[y == label].mean(axis=0).tolist())
    return np.array(c)


def prune_mask(mask, ind):
    new_mask = []
    k, i = 0, 0
    for bit in mask:
        if bit:
            if k == ind[i]:
                i += 1
                new_mask.append(True)
            else:
                new_mask.append(False)
            k += 1
        else:
            new_mask.append(True)
    return np.array(new_mask)


def score_ratio(transform, *, cluster=None,
                inside_cluster=False, start_from_center=False, only_centroids=False,
                max_c=100, dist_c=1., centroid_cap=10, leaf_size=30,
                dataset="data/step-12768-submissions-with-ratio.csv", nrows=None,
                show_dist_plot=True):
    data = pd.read_csv(dataset, nrows=nrows)
    X = transform.fit_transform(data["code"]).toarray()
    data = data.iloc[transform.named_steps["pre"].icorrect]

    if cluster is not None:
        y = cluster.fit_predict(X).astype(int)
    else:
        y = -np.ones(X.shape[0], dtype=int)

    centers = find_centers(X, y)

    if only_centroids:
        for label in range(y.max() + 1):
            train = (data["status"] == "correct") & (y == label)
            if sum(train) != 0:
                nn = NearestNeighbors(n_neighbors=min(centroid_cap, sum(train)), n_jobs=-1, leaf_size=leaf_size)
                nn.fit(X[train])
                ind = nn.kneighbors(centers[label][np.newaxis, :], return_distance=False)
                mask = prune_mask(train, ind[0])
                data, X, y = data[mask], X[mask], y[mask]

    if not inside_cluster:
        y = -np.ones(X.shape[0], dtype=int)

    diff_ratios = []
    for label in tqdm(range(y.min(), y.max() + 1)):
        train = (data["status"] == "correct")
        if label != -1:
            train &= (y == label)
        test = (data["status"] != "correct") & (y == label)
        if sum(train) == 0 or sum(test) == 0:
            est_ratios = np.zeros(sum(test))
        else:
            nn = NearestNeighbors(n_neighbors=min(max_c, sum(train)), n_jobs=-1, leaf_size=leaf_size)
            nn.fit(X[train])
            est_ratios = []
            train_codes = data[train]["code"].values
            test_codes = tqdm(data[test]["code"].values)
            if start_from_center and label != -1:
                dist, ind = nn.kneighbors(centers[label][np.newaxis, :])
                dist, ind = dist[0], ind[0]
                est_codes = list(map(lambda t: train_codes[t[1]],
                                     takewhile(lambda t: t[0] <= dist_c, zip(dist, ind))))
                for code in test_codes:
                    est_ratios.append(ratio(code, est_codes))
            else:
                dist, ind = nn.kneighbors(X[test])
                for code, est_dist, est_ind in zip(test_codes, dist, ind):
                    est_codes = map(lambda t: train_codes[t[1]],
                                    takewhile(lambda t: t[0] <= dist_c, zip(est_dist, est_ind)))
                    est_ratios.append(ratio(code, est_codes))
        diff_ratios.extend(data[test]["best_ratio"] - est_ratios)

    diff_ratios = np.array(diff_ratios)
    if show_dist_plot:
        sns.distplot(diff_ratios)
        plt.show()
    return diff_ratios.mean(), diff_ratios.var()
