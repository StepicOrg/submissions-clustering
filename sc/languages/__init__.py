from .python import *

__all__ = ["from_spec"] + python.__all__

VALID_NAMES = "python",


def from_spec(name, **kwargs):
    if name == "python":
        return Python(**kwargs)
    else:
        raise ValueError(f"name must be of the {VALID_NAMES}")
