"""Itertools funcs."""

__all__ = ["select_at"]


def select_at(values, indicies):
    """Yield values at given indicies."""
    choose_index_it = iter(indicies)
    choosen_index = next(choose_index_it)
    for index, value in enumerate(values):
        if index == choosen_index:
            yield value
            choosen_index = next(choose_index_it)
