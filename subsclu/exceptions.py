class InvalidSpecError(Exception):
    """Raise an error when meet wrong specification for some factory."""
    pass


class PipeCompoundError(Exception):
    """Raise an error when pipe parts give incompatible output."""
    pass
