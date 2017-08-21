import heapq as hp
from collections import namedtuple, Sized
from difflib import SequenceMatcher
from functools import lru_cache
from .base import BaseMetric


def _ratio_list(src, dst):
    max_ratio = 0.
    for s in dst:
        sm = SequenceMatcher(None, src, s)
        if sm.real_quick_ratio() <= max_ratio or sm.quick_ratio() <= max_ratio:
            continue
        max_ratio = max(max_ratio, sm.ratio())
    return max_ratio


class _HeapObj(namedtuple("HeapObj", ["est", "lvl", "sm"])):
    def __lt__(self, other):
        return self.est < other.est or (self.est == other.est and self.lvl < other.lvl)

    def __le__(self, other):
        return self.est < other.est or (self.est == other.est and self.lvl <= other.lvl)

    def __eq__(self, other):
        return self.est == other.est and self.lvl == other.lvl

    def __ne__(self, other):
        return self.est != other.est or self.lvl != other.lvl

    def __gt__(self, other):
        return self.est > other.est or (self.est == other.est and self.lvl > other.lvl)

    def __ge__(self, other):
        return self.est > other.est or (self.est == other.est and self.lvl >= other.lvl)


def _init_tuple(ps, s):
    sm = SequenceMatcher(None, ps, s)
    return _HeapObj(sm.real_quick_ratio(), True, sm)


def _ratio_heap(ps, ss):
    heap = [_init_tuple(ps, s) for s in ss]
    hp._heapify_max(heap)
    push_elem = None
    max_ratio = 0.
    while heap:
        est, lvl, sm = hp._heapreplace_max(heap, push_elem) if push_elem else hp._heappop_max(heap)
        if est > max_ratio:
            if lvl:
                push_elem = _HeapObj(sm.quick_ratio(), False, sm)
            else:
                push_elem = None
                max_ratio = max(max_ratio, sm.ratio())
        else:
            break
    return max_ratio


_THRESHOLD = 50


def _ratio(src, dst):
    if isinstance(dst, Sized) and len(dst) >= _THRESHOLD:
        return _ratio_heap(src, dst)
    else:
        return _ratio_list(src, dst)


class RatioMetric(BaseMetric):
    def __init__(self, method):
        self.method = method

    @lru_cache(maxsize=None)
    def _method(self, source):
        return self.method(source)

    def best_score(self, source, destinations):
        return _ratio(self._method(source), (self._method(destination) for destination in destinations))

    def score(self, source, destination):
        return self.best_score(source, (destination,))
