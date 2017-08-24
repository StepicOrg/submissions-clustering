"""Stuff related to matricies ops."""

import numpy as np

__all__ = ["find_centers", "fill_gaps"]


def find_centers(vecs, labels):
    """Find cetres for input points and labels."""
    if labels.max() != -1:
        return np.stack([
            vecs[labels == label].mean(axis=0)
            for label in range(labels.max() + 1)
        ])
    return np.array([])


def fill_gaps(indicies, elems, size, gap=lambda: np.array([])):
    """Fill gaps of arrays with size with indicies and elems."""
    full = [None] * size
    for ind, elem in zip(indicies, elems):
        full[ind] = elem
    for ind in range(size):
        if full[ind] is None:
            full[ind] = gap()
    return full
