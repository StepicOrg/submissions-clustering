"""Module for stuff related with language bases."""

from subsclu.exceptions import InvalidValue

__all__ = ["Language"]


class Language:
    """Base class for languages, acting like a bunch of fields and methods."""

    def __init__(self, methods=None):
        """Make a language from a set of methods.

        Args:
            methods: Dict of mapping name to method func.
            version: Current language version. May be an int or a tuple of
            ints, floats, strs.
        """
        methods = methods or {}
        for name, method in methods.items():
            setattr(self, name, method)

    def __contains__(self, item):
        """Check if instance contains item as a field or as a method."""
        return item in self.__dict__

    def __getitem__(self, item):
        """Try to get field or method as a key, or raises an Exception."""
        if item in self:
            return self.__dict__[item]
        else:
            raise InvalidValue("no {} field or method in language"
                               .format(item))

    @property
    def attrs(self):
        """List currect language fields and methods."""
        return list(name for name in self.__dict__
                    if not name.startswith("_"))

    @staticmethod
    def outof(*args, **kwargs):
        """See :func:`subsclu.languages.spec.language_from_spec`."""
        from subsclu.languages.spec import language_from_spec
        return language_from_spec(*args, **kwargs)
