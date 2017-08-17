import ast
import parser
import symbol
import token as token_
import tokenize as tokenize_
from io import BytesIO
from keyword import iskeyword

from asttokens import ASTTokens

from subsclu.primitives import Tree, BunchOfMethods

__all__ = ["Python"]

IGNORED_TOKENS = {token_.ENDMARKER, token_.NEWLINE, token_.DEDENT, token_.ERRORTOKEN,
                  tokenize_.COMMENT, tokenize_.NL, tokenize_.ENCODING}
TOKEN_MAP = dict(list(symbol.sym_name.items()) + list(token_.tok_name.items()))


def code2ast(code):
    return ast.parse(code)


def check(code):
    try:
        if isinstance(code, str) and code2ast(code) is not None:
            return True
    except SyntaxError:
        pass
    return False


def tokenize(code):
    result = []
    for token in tokenize_.tokenize(BytesIO(code.encode('utf-8')).readline):
        num, val, exact_type = token.type, token.string, token.exact_type
        if num in IGNORED_TOKENS:
            continue
        elif num == tokenize_.NAME and not iskeyword(val):
            val = "<name>"
        elif num == tokenize_.NUMBER:
            val = "<number>"
        elif num == tokenize_.STRING:
            val = "<string>"
        elif num == tokenize_.OP:
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


def astize(code):
    return SimpleVisitor().visit(code2ast(code))


def grammar2tree(node):
    value = TOKEN_MAP[node[0]]
    children = map(grammar2tree, filter(lambda x: isinstance(x, list), node[1:]))
    return Tree(value, children)


def grammarize(code):
    return grammar2tree(parser.suite(code).tolist())


Python = BunchOfMethods(check, tokenize, asttokenize, astize, grammarize)
