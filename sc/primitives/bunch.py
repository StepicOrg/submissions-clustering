__all__ = ["BunchOfMethods"]


class _FrozenBunch:
    def __init__(self, *methods):
        for method in methods:
            self.__dict__[method.__name__] = method

    def __contains__(self, item):
        return item in self.__dict__

    def __getitem__(self, item):
        return self.__dict__[item]

    def __setattr__(self, key, value):
        raise TypeError("'FrozenBunch' object does not support item assignment")


class BunchOfMethods:
    def __new__(cls, *methods):
        return lambda: _FrozenBunch(*methods)
