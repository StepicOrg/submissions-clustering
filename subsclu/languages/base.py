"""Module for stuff related with language bases."""

import logging

from subsclu.exceptions import InvalidSpec, InvalidValue

__all__ = ["Language"]

logger = logging.getLogger(__name__)


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
    def outof(name, **kwargs):
        """Make language from str name.

        Args:
            name (str): Name of a language to make.
            **kwargs: Params to pass in language creation.

        Returns:
            An instance of :class:`subsclu.languages.base.Language`.

        """
        logger.info("creating a language from name %s", name)
        from subsclu.languages.spec import NAME_TO_LANGUAGE
        if name in NAME_TO_LANGUAGE:
            return NAME_TO_LANGUAGE[name](**kwargs)
        else:
            raise InvalidSpec("name must be one of the {}"
                              .format(NAME_TO_LANGUAGE.keys()))
