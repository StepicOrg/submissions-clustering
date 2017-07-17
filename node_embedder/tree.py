class Tree:
    """A simple tree to store value at each node."""

    def __init__(self, value=None, children=None):
        """Init method for tree.

        :param value: Value to store at root node.
        :param children: List of children, Tree objects.
        """
        self.value = value
        self.children = children or []
        self._leaves_num = None

    def map(self, mapping):
        """
        Map each value at each node using mapping dict/func. Not inplace,
        returning new tree object with same structure.
        """
        _mapping = (lambda x: mapping[x]) if hasattr(mapping, "__getitem__") else mapping
        return Tree(_mapping(self.value), [child.map(_mapping) for child in self.children])

    def pretty_print(self, level=0, indent="  "):
        """
        A simple func to print out tree with values and structure using
        indent.
        """
        pfx = level * indent
        print("{}{}".format(pfx, self.value))
        for child in self.children:
            child.pretty_print(level + 1)

    def flatten(self, add_children_leaves_nums=False):
        """Flatten tree into a list of (parent value, children values) tuples."""
        if len(self.children):
            result = [[self.value, [child.value for child in self.children]]]
            if add_children_leaves_nums:
                result[0].append([child.leaves_num for child in self.children])
            for child in self.children:
                result.extend(child.flatten(add_children_leaves_nums))
            return result
        else:
            return []

    @property
    def leaves_num(self):
        """Return number of leaves in tree. Lazy-evaluated."""
        self._leaves_num = self._leaves_num \
                           or int(len(self.children) == 0) \
                           or sum(child.leaves_num for child in self.children)
        return self._leaves_num
