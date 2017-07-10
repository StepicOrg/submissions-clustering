class NodeCoding:
    """
    Simple implementation of bijection (code : int <-> kind : str) map. Not
    very effective from memory perspective, still fast through.
    """

    def __init__(self):
        """Creates an empty bijection object."""
        self.c2k = {}
        self.k2c = {}

    def _get_kind(self, code):
        return self.c2k[code]

    def _get_code(self, kind):
        if kind not in self.k2c:
            new_code = len(self.c2k)
            self.c2k[new_code] = kind
            self.k2c[kind] = new_code
        return self.k2c[kind]

    def __getitem__(self, item):
        """
        Apply the bijection to input, output the second element in pair.
        Note, that int input give your str and str input give int.
        """
        if isinstance(item, int):
            return self._get_kind(item)
        else:
            return self._get_code(item)

    @property
    def total_size(self):
        """Return number of elements in dict."""
        return len(self.c2k)
