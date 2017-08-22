class _FrozenBunch:
    def __init__(self, *methods):
        for method in methods:
            names = []
            if isinstance(method, tuple):
                names, method = method
            names.append(method.__name__)
            for name in names:
                self.__dict__[name] = method

    def __contains__(self, item):
        return item in self.__dict__

    def __getitem__(self, item):
        if item in self.__dict__:
            return self.__dict__[item]
        else:
            raise ValueError("no such method in bunch")

    def __setattr__(self, key, value):
        raise TypeError("bunch does not support item assignment")


class BunchOfMethods:
    def __new__(cls, *methods):
        return lambda: _FrozenBunch(*methods)
