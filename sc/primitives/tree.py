from collections import Collection
from itertools import chain

__all__ = ["Tree"]


class Tree(Collection):
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
        yield from chain((self.value,), chain.from_iterable(child for child in self.children))

    def __len__(self):
        self._len = self._len \
                    or 1 + sum(len(child) for child in self.children)
        return self._len

    def map(self, mapping):
        _mapping = (lambda x: mapping[x]) if hasattr(mapping, "__getitem__") else mapping
        return Tree(_mapping(self.value), [child.map(_mapping) for child in self.children])

    def flatten(self, add_leaves=False, add_children_leaves_nums=False):
        if len(self.children) or add_leaves:
            d = {"parent": self.value, "children": [child.value for child in self.children]}
            if add_children_leaves_nums:
                d["children_leaves_nums"] = [child.leaves_num for child in self.children]
            yield from chain((d,), chain.from_iterable(
                child.flatten(add_leaves, add_children_leaves_nums) for child in self.children
            ))

    def subtree(self, height=2):
        if height:
            if height == 1:
                return self.value,
            else:
                return tuple(chain((self.value,), (child.subtree(height - 1) for child in self.children)))

    def subtrees(self, height=2):
        if self.depth >= height:
            yield from chain((self.subtree(height),),
                             chain.from_iterable(child.subtrees(height) for child in self.children))

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
