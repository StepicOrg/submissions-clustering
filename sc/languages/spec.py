from .python import *

__all__ = ["language_from_spec"]

VALID_NAMES = "python",


def language_from_spec(name):
    if name == "python":
        return Python()
    else:
        raise ValueError(f"name must be of the {VALID_NAMES}")
