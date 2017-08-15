from .simple import *
from .sklearn import *

__all__ = simple.__all__ + sklearn.__all__

VALID_NAMES = "mbkmeans", "afprop", "stupid"


def from_spec(name, **kwargs):
    if name == "mbkmeans":
        return MiniBatchKMeans(**kwargs)
    elif name == "afprop":
        return AffinityPropagation(**kwargs)
    elif name == "stupid":
        return StupidClusterizer()
    else:
        raise ValueError(f"name must be of the {VALID_NAMES}")
