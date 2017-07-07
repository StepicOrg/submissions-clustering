class CASTNode:
    def __init__(self, kind, value=None, children=None):
        self.kind = kind
        self.value = value
        self.children = children or []
