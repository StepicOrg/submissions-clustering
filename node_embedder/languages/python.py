import ast
import parser
import symbol as _symbol
import token as _token
import tokenize as _tokenize
from io import BytesIO
from keyword import iskeyword

from .language import Language
from ..methods import *
from ..primitives import Tree

SUPPORTED_METHODS = ASTize, Tokenize, Grammarize


def code2ast(code):
    return ast.parse(code)


class SimpleVisitor(ast.NodeVisitor):
    def __init__(self, encoding):
        self.encoding = encoding

    def generic_visit(self, node):
        code = self.encoding[node.__class__.__name__]
        children = [self.visit(child) for child in ast.iter_child_nodes(node)]
        return Tree(code, children)


def astize(method, code, encoding):
    return SimpleVisitor(encoding).visit(code2ast(code))


IGNORED_TOKENS = {_tokenize.COMMENT, _tokenize.NL, _tokenize.ENCODING, _tokenize.ERRORTOKEN}
TOKEN_MAP = dict(list(_symbol.sym_name.items()) + list(_token.tok_name.items()))


def tokenize(method, code, encoding):
    result = []
    for token in _tokenize.tokenize(BytesIO(code.encode('utf-8')).readline):
        num, val, exact_type = token.type, token.string, token.exact_type
        if num in IGNORED_TOKENS:
            continue
        elif num == _tokenize.NAME and not iskeyword(val):
            val = "<name>"
        elif num == _tokenize.NUMBER:
            val = "<number>"
        elif num == _tokenize.STRING:
            val = "<string>"
        elif num == _tokenize.OP:
            val = TOKEN_MAP[exact_type]
        result.append(encoding[val])
    return result


def grammar2tree(node, encoding):
    value = encoding[TOKEN_MAP[node[0]]]
    children = [grammar2tree(child, encoding) for child in filter(lambda x: isinstance(x, list), node[1:])]
    return Tree(value, children)


def grammarize(method, code, encoding):
    return grammar2tree(parser.suite(code).tolist(), encoding)


class Python(Language):
    def check(self, code):
        try:
            if isinstance(code, str) and code2ast(code) is not None:
                return True
        except SyntaxError:
            pass
        return False

    def process(self, method, code, encoding):
        if not isinstance(method, SUPPORTED_METHODS):
            raise UnsupportedMethod()

        return globals()[method.__class__.__name__.lower()](method, code, encoding)
