"""Package for implementing stuff related with languages.

This module implementing bunch of classes, each for each language we gonna use.
See :class:`subsclu.languages.base.Language` for more info.

Attributes:
    Language: :class:`subsclu.languages.base.Language`.
    Python: :class:`subsclu.languages.python.Python`.

"""

from subsclu.languages.base import Language
from subsclu.languages.python import Python

__all__ = ["Language", "Python"]
