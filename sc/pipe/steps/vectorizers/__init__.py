from .count import *
from .simple import *
from .sklearn import *

__all__ = count.__all__ + simple.__all__ + sklearn.__all__

VALID_NAMES = "bon", "bot", "dense", "tfid"


def from_spec(name, **kwargs):
    if name == "bon":
        return BagOfNgrams(**kwargs)
    elif name == "bot":
        return BagOfTrees(**kwargs)
    elif name == "dense":
        return DenseTransformer(**kwargs)
    elif name == "tfid":
        return TfidfTransformer(**kwargs)
    else:
        raise ValueError(f"name must be of the {VALID_NAMES}")
