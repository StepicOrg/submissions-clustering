from .pre import *
from .simple import *
from .sklearn import *
from .tovec import *

__all__ = pre.__all__ + simple.__all__ + sklearn.__all__ + tovec.__all__

VALID_NAMES = "bon", "bot", "hash", "dense", "suml", "meanl", "tfid", "norm", "t2v", "ts2v"


def from_spec(name, **kwargs):
    if name == "bon":
        return BagOfNgrams(**kwargs)
    elif name == "bot":
        return BagOfTrees(**kwargs)
    elif name == "hash":
        return Hasher(**kwargs)
    elif name == "dense":
        return DenseTransformer()
    elif name == "suml":
        return SumList()
    elif name == "meanl":
        return MeanList()
    elif name == "tfid":
        return TfidfTransformer(**kwargs)
    elif name == "norm":
        return Normalizer(**kwargs)
    elif name == "t2v":
        return Token2Vec(**kwargs)
    elif name == "ts2v":
        return Tokens2Vec(**kwargs)
    else:
        raise ValueError(f"name must be of the {VALID_NAMES}")
