import _pickle as pkl
import gzip
import os


def file_exists(path):
    return os.path.exists(path)


def pickle(obj, path):
    with gzip.open(path, "wb") as f:
        pkl.dump(obj, f, -1)


def unpickle(path):
    with gzip.open(path, "rb") as f:
        return pkl.load(f)
