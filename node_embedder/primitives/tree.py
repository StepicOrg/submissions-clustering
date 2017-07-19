from collections import Collection
from itertools import chain


class Tree(Collection):
    def __init__(self, value, children=None):
        assert value is not None
        self.value = value
        self.children = children or []
        self._len = None
        self._leaves_num = None

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
        return Tree(_mapping(self.value), [child.map(_mapping) for child in self.children])

    def flatten(self, add_leaves=False, add_children_leaves_num=False):
        if len(self.children) or add_leaves:
            d = {"value": self.value, "children": [child.value for child in self.children]}
            if add_children_leaves_num:
                d["children_leaves_num"] = [child.leaves_num for child in self.children]
            yield from chain((d,), *(child.flatten(add_leaves, add_children_leaves_num) for child in self.children))

    @property
    def leaves_num(self):
        self._leaves_num = self._leaves_num \
                           or int(len(self.children) == 0) \
                           or sum(child.leaves_num for child in self.children)
        return self._leaves_num
