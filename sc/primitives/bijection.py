from collections import Mapping

__all__ = ["DefaultIntBijection"]


class _Bijection(Mapping):
    def __init__(self):
        self._data = {}
        self._rev_data = {}

    def __getitem__(self, item):
        return self._data[item]

    def __iter__(self):
        yield from self._data.items()

    def __len__(self):
        return len(self._data)

    def __repr__(self):
        return str(list(self._data.items()))

    @property
    def rev(self):
        self._data, self._rev_data = self._rev_data, self._data
        return self


class DefaultIntBijection(_Bijection):
    def __init__(self, zero_value=None):
        super().__init__()
        if zero_value is not None:
            self.__getitem__(zero_value)

    def __getitem__(self, item):
        if item not in self._data:
            next_int = len(self)
            self._data[item] = next_int
            self._rev_data[next_int] = item
        return super().__getitem__(item)

    def __iter__(self):
        yield from ((i, self._rev_data[i]) for i in range(len(self)))
