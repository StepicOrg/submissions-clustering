import logging

from subsclu.exceptions import InvalidSpecError
from .python import Python

logger = logging.getLogger(__name__)

_PYTHON = Python()


def Python():
    return _PYTHON


VALID_NAMES = "python",


def from_spec(name):
    logger.info("start creating language from spec with name = {}".format(name))
    if name == "python":
        return Python()
    else:
        raise InvalidSpecError("name must be of the {}".format(VALID_NAMES))
