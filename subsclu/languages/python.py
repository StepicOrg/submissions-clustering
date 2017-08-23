"""Implementation of stuff related to python language."""

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
    """Check if input code is a valid python code."""
    try:
        if isinstance(code, str) and _code2ast(code) is not None:
            return True
    except SyntaxError:
        pass
    logger.debug("invalid python code %s", code)
    return False


def _parse_tokens(code):
    result = []
    for token in tokenize_.tokenize(BytesIO(code.encode('utf-8')).readline):
        num, val, exact_type = token.type, token.string, token.exact_type
        if num in _IGNORED_TOKENS:
            logger.debug("ignored token val %s", val)
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
    """Parse given code into tokens using :mod:`asttokens` + deleting junk."""
    return list(map(_tok_to_str, filter(_not_junk, ASTTokens(code).tokens)))


class _SimpleVisitor(ast.NodeVisitor):
    def generic_visit(self, node):
        return Tree(node.__class__.__name__,
                    map(self.visit, ast.iter_child_nodes(node)))


_SIMPLE_VISITOR = _SimpleVisitor()


def parse_ast(code):
    """Parse given code into ast tree using :mod:`ast`."""
    return _SIMPLE_VISITOR.visit(_code2ast(code))


def _grammar2tree(node):
    value = _TOKEN_MAP[node[0]]
    children = map(_grammar2tree,
                   filter(lambda x: isinstance(x, list), node[1:]))
    return Tree(value, children)


def _parse_grammar(code):
    return _grammar2tree(parser.suite(code).tolist())


class Python(Language):
    """Python language."""

    _APPROACHES_TO_METHOD = (
        ("check", check_valid),
        ("tokenize", parse_asttokens),
        ("astize", parse_ast)
    )
    """Map from well-known approach to existing method func."""

    def __init__(self):
        """Init method with no args."""
        super().__init__(self._APPROACHES_TO_METHOD)

    @property
    def version(self):
        """:func:`subsclu.languages.base.Language.version`."""
        return sys.version_info[:3]
