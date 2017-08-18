from abc import ABC, abstractmethod


class Plotter(NamedABC):
    @property
    @abstractmethod
    def NAMES(self):
        pass

    @abstractmethod
    def plot(self, X, y):
        pass

    def from_spec(self):
        pass


__all__ = ["abstractmethod", "NamedABC"]


class NamedABC(ABC):
    @property
    @abstractmethod
    def NAMES(self):
        pass

    @classmethod
    def __get_names(cls):
        names = cls.NAMES
        if isinstance(names, str):
            return names,
        elif isinstance(names, tuple) and all(isinstance(name, str) for name in names):
            return names
        else:
            raise ValueError("NAMES attribute should be str ot tuple or strs")

    @classmethod
    def __get_named_derives(cls):
        ans = {}
        for sc in cls.__subclasses__():
            for name in sc.__get_names():
                if name in ans:
                    raise ValueError("same names for two or more classes")
                else:
                    ans[name] = sc
        return ans

    @classmethod
    def from_name(cls, name, **kwargs):
        named_derives = cls.__get_named_derives()
        if not len(named_derives):
            raise ValueError(f"no derives classes")
        for sc_name, sc in named_derives.items():
            if name == sc_name:
                return sc(**kwargs)
        else:
            raise ValueError(f"name should be one of the {tuple(named_derives.keys())}")
