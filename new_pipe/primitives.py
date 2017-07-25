from abc import ABC
from collections import Collection, Mapping, Hashable
from itertools import chain


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


class tree(Collection):
    def __init__(self, value, children=None):
        assert value is not None
        self.value = value
        self.children = [] if children is None else list(children)
        self._len = None
        self._leaves_num = None
        self._height = None
        self._depth = None

    def __contains__(self, item):
        return item in self.__iter__()

    def __iter__(self):
        yield from chain((self.value,), *(child for child in self.children))

    def __len__(self):
        self._len = self._len \
                    or 1 + sum(len(child) for child in self.children)
        return self._len

    def map(self, mapping):
        _mapping = (lambda x: mapping[x]) if hasattr(mapping, "__getitem__") else mapping
        return tree(_mapping(self.value), [child.map(_mapping) for child in self.children])

    def flatten(self, add_leaves=False, add_children_leaves_num=False):
        if len(self.children) or add_leaves:
            d = {"parent": self.value, "children": [child.value for child in self.children]}
            if add_children_leaves_num:
                d["children_leaves_num"] = [child.leaves_num for child in self.children]
            yield from chain((d,), *(child.flatten(add_leaves, add_children_leaves_num) for child in self.children))

    def subtree(self, height=2):
        if height:
            if height == 1:
                return self.value,
            else:
                return tuple(chain((self.value,), (child.subtree(height - 1) for child in self.children)))

    def subtrees(self, height=2):
        if self.height >= height:
            yield from chain((self.subtree(height),), *(child.subtrees(height) for child in self.children))

    @property
    def leaves_num(self):
        self._leaves_num = self._leaves_num \
                           or int(len(self.children) == 0) \
                           or sum(child.leaves_num for child in self.children)
        return self._leaves_num

    @property
    def height(self):
        self._height = self._height \
                       or int(len(self.children) == 0) \
                       or min(child.height for child in self.children) + 1
        return self._height

    @property
    def depth(self):
        self._depth = self._depth \
                      or int(len(self.children) == 0) \
                      or max(child.height for child in self.children) + 1
        return self._depth
