import os

__all__ = ["file_exists"]


def file_exists(path):
    return os.path.exists(path)
