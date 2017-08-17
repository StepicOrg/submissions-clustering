import _pickle as cPickle
import gzip

from sklearn.externals import joblib

__all__ = ["save_object", "load_object", "LoadSaveMixin"]


def pickle_save(object_, path):
    with gzip.open(path, "wb") as file:
        cPickle.dump(object_, file, -1)


def pickle_load(path):
    with gzip.open(path, "rb") as file:
        return cPickle.load(file)


_PICKLE = pickle_save, pickle_load


def joblib_save(object_, path):
    joblib.dump(object_, path, True, -1)


def joblib_load(path):
    return joblib.load(path)


_JOBLIB = joblib_save, joblib_load

_DEFAULT = _JOBLIB

save_object, load_object = _DEFAULT


class LoadSaveMixin:
    def save(self, path):
        save_object(self, path)

    @classmethod
    def load(cls, path):
        return load_object(path)
