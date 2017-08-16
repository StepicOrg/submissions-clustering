from .nn import *

__all__ = nn.__all__

VALID_NAMES = "nn",


def from_spec(name, **kwargs):
    if name == "nn":
        return NNSeeker(**kwargs)
    else:
        raise ValueError(f"name must be of the {VALID_NAMES}")
