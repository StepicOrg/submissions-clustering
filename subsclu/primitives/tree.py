"""Implementation of simple tree."""

from collections.abc import Set
from itertools import chain

__all__ = ["Tree"]


class Tree(Set):
    """The tree class itself, nothing special."""

    def __init__(self, value, children=None):
        """Create tree node (i.e, tree) with value and children.

        Args:
            value (object): Value to store in node.
            children (list[Tree]): List of childrens.
        """
        self.value = value
        self.children = [] if children is None else list(children)

        self._len = None
        self._leaves_num = None
        self._height = None
        self._depth = None

    def __contains__(self, item):
        """Check if tree contains item."""
        return item in self.__iter__()

    def __iter__(self):
        """Yield all tree values starting from root."""
        yield from chain((self.value,),
                         chain.from_iterable(child for child in self.children))

    def __len__(self):
        """Get currecnt tree size."""
        self._len = self._len or 1 + sum(len(child) for child in self.children)
        return self._len

    def map(self, mapping):
        """Construct new tree with same struct, but all values mapped."""
        if hasattr(mapping, "__getitem__"):
            def mapping_(value):
                """Transform dict into a function."""
                return mapping[value]
        else:
            mapping_ = mapping
        return Tree(mapping_(self.value),
                    [child.map(mapping_) for child in self.children])

    def flatten(self, add_leaves=False, add_children_leaves_nums=False):
        """Make tree flattening, yielding dict for each node."""
        if self.children or add_leaves:
            describe = {"parent": self.value,
                        "children": [child.value for child in self.children]}
            if add_children_leaves_nums:
                describe["children_leaves_nums"] = [
                    child.leaves_num for child in self.children
                ]
            yield from chain(
                (describe,),
                chain.from_iterable(
                    child.flatten(
                        add_leaves, add_children_leaves_nums
                    ) for child in self.children
                )
            )

    def subtree(self, height=2):
        """Get subtree of height starting from root as a tuple of values."""
        if height:
            if height == 1:
                return self.value,
            return tuple(chain(
                (self.value,),
                (child.subtree(height - 1) for child in self.children)
            ))
        return None

    def subtrees(self, height=2):
        """Yield all subtress of height starting from root."""
        if self.depth >= height:
            yield from chain(
                (self.subtree(height),),
                chain.from_iterable(
                    child.subtrees(height) for child in self.children
                )
            )

    @property
    def leaves_num(self):
        """Get tree num of leaves."""
        self._leaves_num = self._leaves_num or int(len(self.children) == 0)
        if not self._leaves_num:
            self._leaves_num = sum(child.leaves_num for child in self.children)
        return self._leaves_num

    @property
    def height(self):
        """Get tree height."""
        self._height = self._height or int(len(self.children) == 0)
        if not self._height:
            self._height = min(child.height for child in self.children) + 1
        return self._height

    @property
    def depth(self):
        """Get tree depth."""
        self._depth = self._depth or int(len(self.children) == 0)
        if not self._depth:
            self._depth = max(child.height for child in self.children) + 1
        return self._depth
