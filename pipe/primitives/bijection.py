from abc import ABC
from collections import Mapping

__all__ = ["DefaultIntBijection"]


class Bijection(ABC, Mapping):
    def __init__(self, type1=int, type2=str):
        assert not issubclass(type1, type2) and not issubclass(type2, type1)
        assert issubclass(type1, Hashable) and issubclass(type2, Hashable)
        self.type1, self.type2 = type1, type2
        self.one2two, self.two2one = {}, {}

    def __getitem__(self, item):
        return self.one2two[item] if isinstance(item, self.type1) else self.two2one[item]

    def __iter__(self):
        yield from self.one2two.items()

    def __len__(self):
        return len(self.one2two)

    def __repr__(self):
        return str(list(self))


class DefaultIntBijection(Bijection):
    def __init__(self, type2=str, zero_value=None):
        super().__init__(type2=type2)
        assert zero_value is None or isinstance(zero_value, type2)
        if zero_value is not None:
            _ = self[zero_value]

    def __getitem__(self, item):
        if isinstance(item, self.type2) and item not in self.two2one:
            next_int = len(self)
            self.one2two[next_int] = item
            self.two2one[item] = next_int
        return super().__getitem__(item)

    def __iter__(self):
        yield from ((i, self[i]) for i in range(len(self)))
