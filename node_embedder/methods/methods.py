from abc import ABC


class Method(ABC):
    pass


class ASTize(Method):
    pass


class Tokenize(Method):
    pass


class Grammarize(Method):
    pass


class UnsupportedMethod(Exception):
    pass
