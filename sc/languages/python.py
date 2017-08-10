import ast
import parser
import symbol
import token as _token
import tokenize as _tokenize
from io import BytesIO
from keyword import iskeyword

from asttokens import ASTTokens

from sc.primitives import Tree
from .language import Language

__all__ = ["Python"]


def code2ast(code):
    return ast.parse(code)


IGNORED_TOKENS = {_token.ENDMARKER, _token.NEWLINE, _token.DEDENT, _token.ERRORTOKEN,
                  _tokenize.COMMENT, _tokenize.NL, _tokenize.ENCODING}
TOKEN_MAP = {**symbol.sym_name, **_token.tok_name}


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


def not_junk(token):
    return token.type not in IGNORED_TOKENS


def tok_to_str(token):
    return str((token.type, token.string))


def asttokenize(code):
    return list(map(tok_to_str, filter(not_junk, ASTTokens(code).tokens)))


class SimpleVisitor(ast.NodeVisitor):
    def generic_visit(self, node):
        return Tree(node.__class__.__name__, map(self.visit, ast.iter_child_nodes(node)))


SIMPLE_VISITOR = SimpleVisitor()


def astize(code):
    return SIMPLE_VISITOR.visit(code2ast(code))


def grammar2tree(node):
    return Tree(TOKEN_MAP[node[0]], map(grammar2tree, filter(lambda x: isinstance(x, list), node[1:])))


def grammarize(code):
    return grammar2tree(parser.suite(code).tolist())


class Python(Language):
    def __init__(self):
        super().__init__(check, tokenize, asttokenize, astize, grammarize)
