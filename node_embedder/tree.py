class Tree:
    """A simple tree to store value at each node."""

    def __init__(self, value=None, children=None):
        """Init method for tree.

        :param value: Value to store at root node.
        :param children: List of children, Tree objects.
        """
        self.value = value
        self.children = children or []

    def map(self, mapping):
        """
        Map each value at each node using mapping dict. Not inplace,
        returning new tree object with same structure.
        """
        return Tree(mapping[self.value], [child.map(mapping) for child in self.children])

    def pretty_print(self, level=0, indent="  "):
        """
        A simple func to print out tree with values and structure using
        indent.
        """
        pfx = level * indent
        print("{}{}".format(pfx, self.value))
        for child in self.children:
            child.pretty_print(level + 1)
