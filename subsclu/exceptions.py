class Error(Exception):
    """Base class for all custom exceptions within module."""
    pass


class InvalidSpec(Error):
    """Raise an error when meet wrong specification for some factory."""
    pass


class InvalidPipeCompound(Error):
    """Raise an error when pipe parts give incompatible output or/and input."""
    pass


class InvalidValue(Error):
    """Raise an error when invalid value occurs."""
    pass


class InvalidStructUsage(Error):
    """Raise an error when invalid struct usage orrurs."""
    pass
