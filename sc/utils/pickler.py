import _pickle
import gzip

__all__ = ["pickle", "unpickle"]


def pickle(obj, path):
    with gzip.open(path, "wb") as f:
        _pickle.dump(obj, f, -1)


def unpickle(path):
    with gzip.open(path, "rb") as f:
        return _pickle.load(f)
