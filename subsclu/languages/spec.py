from .python import Python

_PYTHON = Python()


def Python():
    return _PYTHON


VALID_NAMES = "python",


def from_spec(name):
    if name == "python":
        return Python()
    else:
        raise ValueError("name must be of the {}".format(VALID_NAMES))
