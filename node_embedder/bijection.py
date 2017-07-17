from collections import Mapping, Hashable, MutableMapping


class Bijection(Mapping):
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


class MutableBijection(MutableMapping, Bijection):
    def __setitem__(self, key, value):
        key, value = (key, value) if isinstance(key, self.type1) else (value, key)
        if key in self:
            del self[key]
        if value in self:
            del self[value]
        self.one2two[key], self.two2one[value] = value, key

    def __delitem__(self, key):
        key, value = (key, self[key]) if isinstance(key, self.type1) else (self[key], key)
        del self.one2two[key]
        del self.two2one[value]
