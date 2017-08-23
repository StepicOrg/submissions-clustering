"""Module for stuff related with language bases."""

import logging

from subsclu.exceptions import InvalidSpec, InvalidValue

__all__ = ["Language"]

logger = logging.getLogger(__name__)


class Language:
    """Base class for languages, acting like a bunch of fields and methods."""

    def __init__(self, methods=None, version=None):
        """Make a language from a set of methods.

        Args:
            methods: Iterable of methods as a tuple of possible names and the
            method itself.
            version: Current language version. May be an int or a tuple of
            ints, floats, strs.
        """
        methods = methods or ()
        for names, method in methods:
            if not isinstance(names, tuple):
                names = (names,)
            for name in names:
                setattr(self, name, method)
        self._version = version

    def __contains__(self, item):
        """Check if instance contains item as a field or as a method."""
        return item in self.__dict__

    def _get(self, item):
        if item in self:
            return self.__dict__[item]
        else:
            raise InvalidValue("no {} field or method in language"
                               .format(item))

    def __getitem__(self, item):
        """Try to get field or method as a key, or raises an Exception."""
        return self._get(item)

    def __getattr__(self, item):
        """Try to get field or method as an attr, or raises an Exception."""
        return self._get(item)

    @property
    def version(self):
        """Try to get language version."""
        return self._version

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
