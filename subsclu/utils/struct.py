import numpy as np


def find_centers(X, y):
    if y.max() != -1:
        return np.stack([X[y == label].mean(axis=0) for label in range(y.max() + 1)])
    else:
        return np.array([])


def fill_gaps(indicies, elems, size, gap=lambda: np.array([])):
    full = [None] * size
    for ind, elem in zip(indicies, elems):
        full[ind] = elem
    for ind in range(size):
        if full[ind] is None:
            full[ind] = gap()
    return full
