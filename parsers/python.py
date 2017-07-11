from ast import parse as py_parse


def parse(code):
    """
    Just a default parse function invocation from ast module, nothing
    special. Give simple and easy to walk & use tree.
    """
    return py_parse(code)
