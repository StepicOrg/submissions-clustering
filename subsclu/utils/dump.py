import _pickle as cPickle
import gzip
import logging

from sklearn.externals import joblib

logger = logging.getLogger(__name__)


def pickle_save(object_, path, **kwargs):
    logger.info("pickle object {} to {}".format(object_, path))
    with gzip.open(path, "wb") as file:
        cPickle.dump(object_, file, **kwargs)


def pickle_load(path, **kwargs):
    logger.info("unpickle object from {}".format(path))
    with gzip.open(path, "rb") as file:
        return cPickle.load(file, **kwargs)


_PICKLE = pickle_save, pickle_load


def joblib_save(object_, path, **kwargs):
    logger.info("joblib serialize object {} to {}".format(object_, path))
    joblib.dump(object_, path, **kwargs)


def joblib_load(path, **kwargs):
    logger.info("joblib deserialize object from {}".format(path))
    return joblib.load(path, **kwargs)


_JOBLIB = joblib_save, joblib_load

_DEFAULT = _JOBLIB

default_save, default_load = _DEFAULT


class LoadSaveMixin:
    def save(self, path, **kwargs):
        default_save(self, path, **kwargs)

    @classmethod
    def load(cls, path, **kwargs):
        return default_load(path, **kwargs)
