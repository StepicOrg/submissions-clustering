"""Module for custom exceptions."""

__all__ = ["InvalidSpec", "InvalidPipeCompound",
           "InvalidValue", "InvalidStructUsage"]


class _Error(Exception):
    """Base class for all custom exceptions within module."""


class InvalidSpec(_Error):
    """Raise an error when meet wrong specification for some factory."""


class InvalidPipeCompound(_Error):
    """Raise an error when pipe parts give incompatible output or/and input."""


class InvalidValue(_Error):
    """Raise an error when invalid value occurs."""


class InvalidStructUsage(_Error):
    """Raise an error when invalid struct usage orrurs."""
