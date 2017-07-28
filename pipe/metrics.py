from collections import Iterable
from difflib import SequenceMatcher
from itertools import chain


def _ratio(s1, s2):
    return SequenceMatcher(None, s1, s2).ratio()


def ratio(s1, s2):
    if not isinstance(s2, Iterable):
        s2 = (s2,)
    return max(chain((_ratio(s1, _s2) for _s2 in s2), (0,)))
