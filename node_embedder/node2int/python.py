import ast
from enum import Flag, auto
from .node_coding import NodeCoding
from ..tree import Tree


class SimpleVisitor(ast.NodeVisitor):
    def __init__(self, node_coding):
        """Creates a simple visitor object.

        :param node_coding:
        """
        self.node_coding = node_coding

    def generic_visit(self, node):
        """Simple visit func for all nodes. Return a tree with same structure."""
        kind = node.__class__.__name__
        value = self.node_coding[kind]
        children = [self.visit(child) for child in ast.iter_child_nodes(node)]
        return Tree(value, children)


class EmbeddingFeature(Flag):
    """
    Different features of embedding. CONSIDER_LITERALS make different
    codes for different literals, CONSIDER_NAMES make different codes for
    different names.
    """

    SIMPLE = 0
    CONSIDER_LITERALS = auto()
    CONSIDER_NAMES = auto()


def node_embedding(py_ast, embedding_features=EmbeddingFeature.SIMPLE, node_coding=None):
    """Given as ast tree, map each node to a particular int code."""
    node_coding = node_coding or NodeCoding()
    if EmbeddingFeature.CONSIDER_LITERALS | EmbeddingFeature.CONSIDER_NAMES in embedding_features:
        # TODO: To be implemented...
        raise Exception("Not implemented yet!")
    else:
        visitor = SimpleVisitor(node_coding)
    return visitor.visit(py_ast), node_coding
