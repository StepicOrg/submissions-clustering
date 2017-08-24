"""Module consist of languages specifications."""

import logging

from subsclu.exceptions import InvalidSpec
from subsclu.languages.python import Python

__all__ = ["VALID_NAMES", "language_from_spec"]

logger = logging.getLogger(__name__)

VALID_NAMES = ("python",)
"""Tuple of valid names."""


def language_from_spec(name):
    """Make language from str name.

    Args:
        name (str): Name of a language to make.

    Returns:
        An instance of :class:`subsclu.languages.base.Language`.

    """
    logger.info("creating a language from name %s", name)
    if name == "python":
        return Python()
    else:
        raise InvalidSpec("name must be one of the {}".format(VALID_NAMES))
