import ast
from collections import namedtuple
from enum import Flag, auto
from .cast import CASTNode


class SimpleVisitor(ast.NodeVisitor):
    def visit(self, node):
        pass


class ParseFeature(Flag):
    SIMPLE = 0
    CONSIDER_LITERALS = auto()
    CONSIDER_NAMES = auto()


def parse(code, parse_features=ParseFeature.SIMPLE):
    py_ast = ast.parse(code)
    visitor = SimpleVisitor()
    return visitor.visit(py_ast)



    # TODO: 2 variants
    # TODO: 1) parse into common (for all languages) AST, then apply embedding
    # TODO: 1) parse into parse-specific AST, then apply embedding
    # TODO: Ok, let's use first one, but ignore node's literals
    # TODO: + data commit
