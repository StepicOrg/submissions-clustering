import _pickle as cPickle
import gzip

from sklearn.externals import joblib


def pickle_save(object_, path, **kwargs):
    with gzip.open(path, "wb") as file:
        cPickle.dump(object_, file, **kwargs)


def pickle_load(path, **kwargs):
    with gzip.open(path, "rb") as file:
        return cPickle.load(file, **kwargs)


_PICKLE = pickle_save, pickle_load


def joblib_save(object_, path, **kwargs):
    joblib.dump(object_, path, **kwargs)


def joblib_load(path, **kwargs):
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
