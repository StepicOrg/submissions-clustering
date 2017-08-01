import heapq as hp
from collections import Iterable
from collections import namedtuple
from difflib import SequenceMatcher


def ratio_list(ps, ss):
    max_ratio = 0.
    for s in ss:
        sm = SequenceMatcher(None, ps, s)
        if sm.real_quick_ratio() <= max_ratio or sm.quick_ratio() <= max_ratio:
            continue
        max_ratio = max(max_ratio, sm.ratio())
    return max_ratio


class HeapObj(namedtuple("HeapObj", ["est", "lvl", "sm"])):
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


def init_tuple(ps, s):
    sm = SequenceMatcher(None, ps, s)
    return HeapObj(sm.real_quick_ratio(), True, sm)


def ratio_heap(ps, ss):
    heap = [init_tuple(ps, s) for s in ss]
    hp._heapify_max(heap)
    push_elem = None
    max_ratio = 0.
    while heap:
        est, lvl, sm = hp._heapreplace_max(heap, push_elem) if push_elem else hp._heappop_max(heap)
        if est > max_ratio:
            if lvl:
                push_elem = HeapObj(sm.quick_ratio(), False, sm)
            else:
                push_elem = None
                max_ratio = max(max_ratio, sm.ratio())
        else:
            break
    return max_ratio


THRESHOLD = 50


def ratio(ps, ss):
    if not isinstance(ss, Iterable):
        ss = (ss,)
    if hasattr(ss, "__len__") and len(ss) >= THRESHOLD:
        return ratio_heap(ps, ss)
    else:
        return ratio_list(ps, ss)
