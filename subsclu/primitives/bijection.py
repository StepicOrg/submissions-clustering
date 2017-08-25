"""Implementation of bijection mapping."""

import logging
from collections import Mapping

__all__ = ["DefaultIntBijection"]

logger = logging.getLogger(__name__)


class _Bijection(Mapping):
    def __init__(self, data=None, rev_data=None):
        self._data = data or {}
        self._rev_data = rev_data or {}

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
        """Do a bijection reversing."""
        logger.info("reversing a bijection")
        return _Bijection(self._rev_data, self._data)


class DefaultIntBijection(_Bijection):
    """Default increasing int bijection for convinience."""

    def __init__(self, zero_value=None):
        """Create an instance of bijection.

        Args:
            zero_value: Value for map 0 to.
        """
        super().__init__()
        if zero_value is not None:
            self.__getitem__(zero_value)

    def __getitem__(self, item):
        """Get int mapping, or new one if no such item was met previosly."""
        if item not in self._data:
            logging.debug("new item %s", item)
            next_int = len(self)
            self._data[item] = next_int
            self._rev_data[next_int] = item
        return super().__getitem__(item)

    def __iter__(self):
        """Yileding a tuple of mappings (int, obj) in ascending order."""
        yield from ((i, self._rev_data[i]) for i in range(len(self)))
