from subsclu.exceptions import InvalidSpecError
from .python import Python

_PYTHON = Python()


def Python():
    return _PYTHON


VALID_NAMES = "python",


def from_spec(name):
    if name == "python":
        return Python()
    else:
        raise InvalidSpecError("name must be of the {}".format(VALID_NAMES))
