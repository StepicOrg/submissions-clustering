"""Module consist of languages specifications."""

from subsclu.languages.python import Python

__all__ = ["NAME_TO_LANGUAGE"]

NAME_TO_LANGUAGE = {
    "python": Python
}
"""Map name to language class."""
