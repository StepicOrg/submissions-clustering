import ast

"""
Node description for Python 3.4.3
WARNING: Implementation relies on fields order. Do NOT change NODE_DESC in runtime
"""

NODE_DESC = {
    ast.Module: {
        'props': (),
        'children': ('body',)
    },

    # Literals
    ast.Num: {
        'props': ('n',),
        'children': ()
    },
    ast.Str: {
        'props': ('s',),
        'children': ()
    },

    # ast.FormattedValue: {
    #     'props': ('conversion',),
    #     'children': ('value', 'format_spec')
    # },
    # ast.JoinedStr: {
    #     'props': (),
    #     'children': ('values',)
    # },

    ast.Bytes: {
        'props': ('s',),
        'children': ()
    },
    ast.List: {
        'props': (),
        'children': ('elts', 'ctx')
    },
    ast.Tuple: {
        'props': (),
        'children': ('elts', 'ctx')
    },
    ast.Set: {
        'props': (),
        'children': ('elts',)
    },
    ast.Dict: {
        'props': (),
        'children': ('keys', 'values')
    },

    ast.Ellipsis: {
        'props': (),
        'children': ()
    },
    ast.NameConstant: {
        'props': ('value',),
        'children': ()
    },

    # Variables
    ast.Name: {
        'props': ('id',),
        'children': ('ctx',)
    },

    ast.Load: {
        'props': (),
        'children': ()
    },
    ast.Store: {
        'props': (),
        'children': ()
    },
    ast.Del: {
        'props': (),
        'children': ()
    },

    ast.Starred: {
        'props': (),
        'children': ('value', 'ctx')
    },

    # Expressions
    ast.Expr: {
        'props': (),
        'children': ('value',)
    },

    ast.UnaryOp: {
        'props': (),
        'children': ('op', 'operand')
    },
    ast.UAdd: {
        'props': (),
        'children': ()
    },
    ast.USub: {
        'props': (),
        'children': ()
    },
    ast.Not: {
        'props': (),
        'children': ()
    },
    ast.Invert: {
        'props': (),
        'children': ()
    },

    ast.BinOp: {
        'props': (),
        'children': ('left', 'op', 'right')
    },
    ast.Add: {
        'props': (),
        'children': ()
    },
    ast.Sub: {
        'props': (),
        'children': ()
    },
    ast.Mult: {
        'props': (),
        'children': ()
    },
    ast.Div: {
        'props': (),
        'children': ()
    },
    ast.FloorDiv: {
        'props': (),
        'children': ()
    },
    ast.Mod: {
        'props': (),
        'children': ()
    },
    ast.Pow: {
        'props': (),
        'children': ()
    },
    ast.LShift: {
        'props': (),
        'children': ()
    },
    ast.RShift: {
        'props': (),
        'children': ()
    },
    ast.BitOr: {
        'props': (),
        'children': ()
    },
    ast.BitXor: {
        'props': (),
        'children': ()
    },
    ast.BitAnd: {
        'props': (),
        'children': ()
    },
    # ast.MatMult: {
    #     'props': (),
    #     'children': ()
    # },

    ast.BoolOp: {
        'props': (),
        'children': ('op', 'values')
    },
    ast.And: {
        'props': (),
        'children': ()
    },
    ast.Or: {
        'props': (),
        'children': ()
    },

    ast.Compare: {
        'props': (),
        'children': ('left', 'ops', 'comparators')
    },
    ast.Eq: {
        'props': (),
        'children': ()
    },
    ast.NotEq: {
        'props': (),
        'children': ()
    },
    ast.Lt: {
        'props': (),
        'children': ()
    },
    ast.LtE: {
        'props': (),
        'children': ()
    },
    ast.Gt: {
        'props': (),
        'children': ()
    },
    ast.GtE: {
        'props': (),
        'children': ()
    },
    ast.Is: {
        'props': (),
        'children': ()
    },
    ast.IsNot: {
        'props': (),
        'children': ()
    },
    ast.In: {
        'props': (),
        'children': ()
    },
    ast.NotIn: {
        'props': (),
        'children': ()
    },

    ast.Call: {
        'props': (),
        'children': ('func', 'args', 'keywords', 'starargs', 'kwargs')
    },
    ast.keyword: {
        'props': ('arg',),
        'children': ('value',)
    },

    ast.IfExp: {
        'props': (),
        'children': ('test', 'body', 'orelse')
    },

    ast.Attribute: {
        'props': ('attr',),
        'children': ('value', 'ctx')
    },

    # Subscripting
    ast.Subscript: {
        'props': (),
        'children': ('value', 'slice', 'ctx')
    },
    ast.Index: {
        'props': (),
        'children': ('value',)
    },
    ast.Slice: {
        'props': (),
        'children': ('lower', 'upper', 'step')
    },
    ast.ExtSlice: {
        'props': (),
        'children': ('dims',)
    },

    # Comprehensions
    ast.ListComp: {
        'props': (),
        'children': ('elt', 'generators')
    },
    ast.SetComp: {
        'props': (),
        'children': ('elt', 'generators')
    },
    ast.GeneratorExp: {
        'props': (),
        'children': ('elt', 'generators')
    },
    ast.DictComp: {
        'props': (),
        'children': ('key', 'value', 'generators')
    },
    ast.comprehension: {
        'props': (),  # + 'is_async',
        'children': ('target', 'iter', 'ifs')
    },

    # Statements
    ast.Assign: {
        'props': (),
        'children': ('targets', 'value')
    },
    # ast.AnnAssign: {
    #     'props': ('simple',),
    #     'children': ('target', 'annotation', 'value')
    # },
    ast.AugAssign: {
        'props': (),
        'children': ('target', 'op', 'value')
    },

    # ast.Print: {
    #     'props': ('nl',),
    #     'children': ('dest', 'value')
    # },

    ast.Raise: {
        'props': (),
        'children': ('exc', 'cause')
    },
    ast.Assert: {
        'props': (),
        'children': ('test', 'msg')
    },

    ast.Delete: {
        'props': (),
        'children': ('targets',)
    },

    ast.Pass: {
        'props': (),
        'children': ()
    },

    # Imports
    ast.Import: {
        'props': (),
        'children': ('names',)
    },
    ast.ImportFrom: {
        'props': ('module', 'level'),
        'children': ('names',)
    },
    ast.alias: {
        'props': ('name', 'asname'),
        'children': ()
    },

    # Control flow
    ast.If: {
        'props': (),
        'children': ('test', 'body', 'orelse')
    },

    ast.For: {
        'props': (),
        'children': ('target', 'iter', 'body', 'orelse')
    },

    ast.While: {
        'props': (),
        'children': ('test', 'body', 'orelse')
    },

    ast.Break: {
        'props': (),
        'children': ()
    },
    ast.Continue: {
        'props': (),
        'children': ()
    },

    ast.Try: {
        'props': (),
        'children': ('body', 'handlers', 'orelse', 'finalbody')
    },
    # ast.TryFinally: {
    #     'props': (),
    #     'children': ('body', 'finalbody')
    # },
    # ast.TryExcept: {
    #     'props': (),
    #     'children': ('body', 'handlers', 'orelse')
    # },
    ast.ExceptHandler: {
        'props': ('name',),
        'children': ('type', 'body')
    },

    ast.With: {
        'props': (),
        'children': ('items', 'body')
    },
    ast.withitem: {
        'props': (),
        'children': ('context_expr', 'optional_vars')
    },

    # Functions and class definitions
    ast.FunctionDef: {
        'props': ('name',),
        'children': ('args', 'body', 'decorator_list', 'returns')
    },
    ast.Lambda: {
        'props': (),
        'children': ('args', 'body')
    },
    ast.arguments: {
        'props': (),
        'children': ('args', 'kwonlyargs', 'vararg', 'kwarg', 'defaults', 'kw_defaults')
    },
    ast.arg: {
        'props': ('arg',),
        'children': ('annotation',)
    },

    ast.Return: {
        'props': (),
        'children': ('value',)
    },
    ast.Yield: {
        'props': (),
        'children': ('value',)
    },
    ast.YieldFrom: {
        'props': (),
        'children': ('value',)
    },

    ast.Global: {
        'props': ('names',),
        'children': ()
    },
    ast.Nonlocal: {
        'props': ('names', ),
        'children': ()
    },

    ast.ClassDef: {
        'props': ('name',),
        'children': ('bases', 'keywords', 'starargs', 'kwargs', 'body', 'decorator_list')
    },

    # Async and await
    # ast.AsyncFunctionDef: {
    #     'props': ('name',),
    #     'children': ('args', 'body', 'decorator_list', 'returns')
    # },
    # ast.Await: {
    #     'props': (),
    #     'children': ('value',)
    # },
    # ast.AsyncFor: {
    #     'props': (),
    #     'children': ('target', 'iter', 'body', 'orelse')
    # },
    # ast.AyncWith: {
    #     'props': (),
    #     'children': ('items', 'body')
    # }
}
