import ast
import parser
import symbol as _symbol
import token as _token
import tokenize as _tokenize
from io import BytesIO
from keyword import iskeyword

from bunch import Bunch

from ..primitives import tree


def code2ast(code):
    return ast.parse(code)


# import sys
# sys.setrecursionlimit(10 * sys.getrecursionlimit())


class SimpleVisitor(ast.NodeVisitor):
    def generic_visit(self, node):
        return tree(node.__class__.__name__, map(self.visit, ast.iter_child_nodes(node)))


IGNORED_TOKENS = {_tokenize.COMMENT, _tokenize.NL, _tokenize.ENCODING, _tokenize.ERRORTOKEN}
TOKEN_MAP = {**_symbol.sym_name, **_token.tok_name}


def grammar2tree(node):
    return tree(TOKEN_MAP[node[0]], map(grammar2tree, filter(lambda x: isinstance(x, list), node[1:])))


def check(code):
    try:
        if isinstance(code, str) and code2ast(code) is not None:
            return True
    except SyntaxError:
        pass
    return False


def tokenize(code):
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
        result.append(val)
    return result


def grammarize(code):
    return grammar2tree(parser.suite(code).tolist())


def astize(code):
    return SimpleVisitor().visit(code2ast(code))


python = Bunch({
    "check": check,
    "tokenize": tokenize,
    "grammarize": grammarize,
    "astize": astize
})
