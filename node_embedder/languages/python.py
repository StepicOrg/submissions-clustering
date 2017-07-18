import ast
from io import BytesIO
from keyword import iskeyword
from tokenize import tokenize, NAME, NUMBER, STRING, COMMENT, ERRORTOKEN, NL, ENCODING

from node_embedder.tree import Tree
from .language import Language
from ..methods import Tokenize, Treeize


class SimpleVisitor(ast.NodeVisitor):
    def __init__(self, encoding):
        self.encoding = encoding

    def generic_visit(self, node):
        code = self.encoding[node.__class__.__name__]
        children = [self.visit(child) for child in ast.iter_child_nodes(node)]
        return Tree(code, children)


class Python(Language):
    def check(self, code):
        try:
            if isinstance(code, str) and self.parse(code) is not None:
                return True
        except SyntaxError:
            pass
        return False

    def parse(self, code):
        return ast.parse(code)

    # TODO: почитать про парсинг https://docs.python.org/3/library/parser.html
    def process(self, method, code, encoding):
        if isinstance(method, Tokenize):
            result = []
            for output in tokenize(BytesIO(code.encode('utf-8')).readline):
                tok_num, tok_val, ex_type = output.type, output.string, output.exact_type
                if tok_num in {COMMENT, ERRORTOKEN, NL, ENCODING}:
                    continue
                elif tok_num == NAME and not iskeyword(tok_val):
                    print(tok_val)
                    tok_val = "<name>"
                elif tok_num == NUMBER:
                    tok_val = "<number>"
                elif tok_num == STRING:
                    tok_val = "<string>"
                result.append(encoding[tok_val])
            return result
        elif isinstance(method, Treeize):
            return SimpleVisitor(encoding).visit(self.parse(code))
