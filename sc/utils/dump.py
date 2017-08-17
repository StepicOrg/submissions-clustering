import _pickle as cPickle
import gzip

from sklearn.externals import joblib

__all__ = ["save", "load", "LoadSaveMixin"]


def _pickle_save(object_, path):
    with gzip.open(path, "wb") as file:
        cPickle.dump(object_, file, -1)


def _pickle_load(path):
    with gzip.open(path, "rb") as file:
        return cPickle.load(file)


_PICKLE = _pickle_save, _pickle_load


def _joblib_save(object_, path):
    joblib.dump(object_, path, True, -1)


def _joblib_load(path):
    return joblib.load(path)


_JOBLIB = _joblib_save, _joblib_load

_DEFAULT = _JOBLIB


class LoadSaveMixin:
    _save, _load = _DEFAULT

    def save(self, path):
        self._save(self, path)

    @classmethod
    def load(cls, path):
        return cls._load(path)
