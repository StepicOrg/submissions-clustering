"""Stuff related with serializing and deserializing."""

import _pickle as cPickle
import gzip
import logging

from sklearn.externals import joblib

__all__ = ["pickle_save", "pickle_load", "joblib_save", "joblib_load",
           "default_save", "default_load", "LoadSaveMixin"]

logger = logging.getLogger(__name__)


def pickle_save(object_, path, **kwargs):
    """Pickle serializing with gzip."""
    logger.info("pickle object %s to %s", object_, path)
    with gzip.open(path, "wb") as file:
        cPickle.dump(object_, file, **kwargs)


def pickle_load(path, **kwargs):
    """Pickle deserializing with gzip."""
    logger.info("unpickle object from %s", path)
    with gzip.open(path, "rb") as file:
        return cPickle.load(file, **kwargs)


def joblib_save(object_, path, **kwargs):
    """Joblib serializing with compress."""
    logger.info("joblib serialize object %s to %s", object_, path)
    joblib.dump(object_, path, **kwargs)


def joblib_load(path, **kwargs):
    """Joblib deselializing with compress."""
    logger.info("joblib deserialize object from %s", path)
    return joblib.load(path, **kwargs)


_JOBLIB = joblib_save, joblib_load

_DEFAULT = _JOBLIB

_DEFAULT_SAVE, _DEFAULT_LOAD = _DEFAULT


def default_save(*args, **kwargs):
    """Do default serialize."""
    _DEFAULT_SAVE(*args, **kwargs)


def default_load(*args, **kwargs):
    """Do default deserialize."""
    return _DEFAULT_LOAD(*args, **kwargs)


class LoadSaveMixin:
    """Mixin for easy save and load any pickable object."""

    def save(self, path, **kwargs):
        """Serialize object and save it at path."""
        logger.info("save object of type %s", self.__class__.__name__)
        default_save(self, path, **kwargs)

    @classmethod
    def load(cls, path, **kwargs):
        """Deserialize object from path."""
        logger.info("load object of type %s", cls.__name__)
        return default_load(path, **kwargs)
