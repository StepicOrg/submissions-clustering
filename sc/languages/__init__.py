from .python import Python

__all__ = ["Python"]

VALID_NAMES = "python",


def from_spec(name):
    if name == "python":
        return Python()
    else:
        raise ValueError("name must be of the {}".format(VALID_NAMES))
