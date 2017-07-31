from collections import Iterable
from difflib import SequenceMatcher


def ratio(ps, ss):
    if not isinstance(ss, Iterable):
        ss = (ss,)
    max_ratio = 0.
    for s in ss:
        sm = SequenceMatcher(None, ps, s)
        if sm.real_quick_ratio() <= max_ratio or sm.quick_ratio() <= max_ratio:
            continue
        max_ratio = max(max_ratio, sm.ratio())
    return max_ratio
