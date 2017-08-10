import numpy as np

__all__ = ["find_centers"]


def find_centers(X, y):
    c = []
    for label in range(y.max() + 1):
        c.append(X[y == label].mean(axis=0).tolist())
    return np.array(c)
