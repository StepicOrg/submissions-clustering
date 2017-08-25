"""Stuff related to matricies ops."""

import numpy as np

__all__ = ["find_centers", "shift_indicies", "fill_gaps"]


def find_centers(vecs, labels):
    """Find cetres for input points and labels."""
    if labels.max() != -1:
        return np.stack([
            vecs[labels == label].mean(axis=0)
            for label in range(labels.max() + 1)
        ])
    return np.array([])


def shift_indicies(arrays, shift):
    """Shift values in arrays using shift array."""
    shifted_arrays = []
    for array in arrays:
        if array.size:
            shifted_arrays.append(shift[array])
        else:
            shifted_arrays.append(np.empty(0))
    return shifted_arrays


def fill_gaps(indicies, elementss, size, gap):
    """Fill gaps of arrays with size with indicies and elems."""
    full = [None] * size
    for ind, elem in zip(indicies, elementss):
        full[ind] = elem
    for ind in range(size):
        if full[ind] is None:
            full[ind] = gap()
    return full
