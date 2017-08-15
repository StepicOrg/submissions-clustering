from .count import *
from .hash import *
from .simple import *
from .sklearn import *
from .tovec import *

__all__ = count.__all__ + hash.__all__ + simple.__all__ + sklearn.__all__ + tovec.__all__

VALID_NAMES = "bon", "bot", "hash", "dense", "tfid"


def from_spec(name, **kwargs):
    if name == "bon":
        return BagOfNgrams(**kwargs)
    elif name == "bot":
        return BagOfTrees(**kwargs)
    elif name == "hash":
        return Hash(**kwargs)
    elif name == "dense":
        return DenseTransformer()
    elif name == "tfid":
        return TfidfTransformer(**kwargs)
    else:
        raise ValueError(f"name must be of the {VALID_NAMES}")
