"""Ration metric from difflib."""

import heapq as hp
import logging
from collections import namedtuple, Sized
from difflib import SequenceMatcher
from functools import lru_cache

from subsclu.scorers.base import Metric

__all__ = ["RatioMetric"]

logger = logging.getLogger(__name__)


def _ratio_list(source, dests):
    max_ratio = 0.
    for dest in dests:
        seq_matcher = SequenceMatcher(None, source, dest)
        if seq_matcher.real_quick_ratio() <= max_ratio \
                or seq_matcher.quick_ratio() <= max_ratio:
            continue
        max_ratio = max(max_ratio, seq_matcher.ratio())
    return max_ratio


class _HeapObj(namedtuple("HeapObj", ["est", "lvl", "sm"])):
    def __lt__(self, other):
        return self.est < other.est or (self.est == other.est
                                        and self.lvl < other.lvl)

    def __le__(self, other):
        return self.est < other.est or (self.est == other.est
                                        and self.lvl <= other.lvl)

    def __eq__(self, other):
        return self.est == other.est and self.lvl == other.lvl

    def __ne__(self, other):
        return self.est != other.est or self.lvl != other.lvl

    def __gt__(self, other):
        return self.est > other.est or (self.est == other.est
                                        and self.lvl > other.lvl)

    def __ge__(self, other):
        return self.est > other.est or (self.est == other.est
                                        and self.lvl >= other.lvl)


def _init_tuple(source, dest):
    seq_matcher = SequenceMatcher(None, source, dest)
    return _HeapObj(seq_matcher.real_quick_ratio(), True, seq_matcher)


def _ratio_heap(source, dests):
    # pylint: disable=protected-access, no-member
    heap = [_init_tuple(source, s) for s in dests]
    hp._heapify_max(heap)
    push_elem = None
    max_ratio = 0.
    while heap:
        if push_elem:
            est, lvl, seq_matcher = hp._heapreplace_max(heap, push_elem)
        else:
            est, lvl, seq_matcher = hp._heappop_max(heap)
        if est > max_ratio:
            if lvl:
                push_elem = _HeapObj(
                    seq_matcher.quick_ratio(), False, seq_matcher
                )
            else:
                push_elem = None
                max_ratio = max(max_ratio, seq_matcher.ratio())
        else:
            break
    return max_ratio


_USE_HEAP = False
_HEAP_THRESHOLD = 50


def _ratio(src, dst):
    if _USE_HEAP and isinstance(dst, Sized) and len(dst) >= _HEAP_THRESHOLD:
        logger.info("using heap method to calc ratio")
        return _ratio_heap(src, dst)
    return _ratio_list(src, dst)


class RatioMetric(Metric):
    """Implementation of ratio metric."""

    def __init__(self, method):
        """Create instance of ratio metric.

        Args:
            method: method to preprocess str with.
        """
        self.method = method

    @lru_cache(maxsize=None)
    def _method(self, source):
        return self.method(source)

    def metric(self, source, dest):
        """See :func:`subsclu.scorers.base.Metric.metric`."""
        return self.best_metric(source, (dest,))

    def best_metric(self, source, dests):
        """See :func:`subsclu.scorers.base.Metric.best_metric`."""
        return _ratio(
            self._method(source),
            (self._method(dest) for dest in dests)
        )
