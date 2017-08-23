import ast
import logging
import parser
import symbol
import sys
import token as token_
import tokenize as tokenize_
from io import BytesIO
from keyword import iskeyword

from asttokens import ASTTokens

from subsclu.languages.base import Language
from subsclu.primitives import Tree

__all__ = ["check_valid", "parse_asttokens", "parse_ast", "Python"]

logger = logging.getLogger(__name__)

_IGNORED_TOKENS = {
    token_.ENDMARKER, token_.NEWLINE, token_.DEDENT, token_.ERRORTOKEN,
    tokenize_.COMMENT, tokenize_.NL, tokenize_.ENCODING
}
_TOKEN_MAP = dict(
    list(symbol.sym_name.items()) + list(token_.tok_name.items())
)


def _code2ast(code):
    return ast.parse(code)


def check_valid(code):
    """Check if input object is a valid python code.

    Args:
        code ():

    Returns:

    """
    try:
        if isinstance(code, str) and _code2ast(code) is not None:
            return True
    except SyntaxError:
        pass
    logger.debug("invalid python code: {}".format(code))
    return False


def _parse_tokens(code):
    result = []
    for token in tokenize_.tokenize(BytesIO(code.encode('utf-8')).readline):
        num, val, exact_type = token.type, token.string, token.exact_type
        if num in _IGNORED_TOKENS:
            logger.debug("ignored token val: {}".format(val))
            continue
        elif num == tokenize_.NAME and not iskeyword(val):
            val = "<name>"
        elif num == tokenize_.NUMBER:
            val = "<number>"
        elif num == tokenize_.STRING:
            val = "<string>"
        elif num == tokenize_.OP:
            val = _TOKEN_MAP[exact_type]
        result.append(val)
    return result


def _not_junk(token):
    return token.type not in _IGNORED_TOKENS


def _tok_to_str(token):
    return str((token.type, token.string))


def parse_asttokens(code):
    return list(map(_tok_to_str, filter(_not_junk, ASTTokens(code).tokens)))


class _SimpleVisitor(ast.NodeVisitor):
    def generic_visit(self, node):
        return Tree(node.__class__.__name__, map(self.visit, ast.iter_child_nodes(node)))


def parse_ast(code):
    return _SimpleVisitor().visit(_code2ast(code))


def _grammar2tree(node):
    value = _TOKEN_MAP[node[0]]
    children = map(_grammar2tree, filter(lambda x: isinstance(x, list), node[1:]))
    return Tree(value, children)


def _parse_grammar(code):
    return _grammar2tree(parser.suite(code).tolist())


class Python(Language):
    def __init__(self):
        super().__init__(
            methods=(
                ("check", check_valid),
                ("tokenize", parse_asttokens),
                ("astize", parse_ast)
            )
        )

    @property
    def version(self):
        version = sys.version_info
        return version.major, version.minor, version.micro
