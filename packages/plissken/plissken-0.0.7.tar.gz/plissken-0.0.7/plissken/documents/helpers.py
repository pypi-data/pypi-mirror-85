import typing
from collections import namedtuple

import redbaron


def isnamedtupleinstance(x):
    t = type(x)
    b = t.__bases__
    if len(b) != 1 or b[0] != tuple:
        return False
    f = getattr(t, "_fields", None)
    if not isinstance(f, tuple):
        return False
    return all(type(n) == str for n in f)


def prettyDoc(document: namedtuple) -> str:

    rv = dict(document._asdict())
    for k, v in rv.items():
        if isnamedtupleinstance(v):
            rv[k] = prettyDoc(v)

        elif isinstance(v, list):
            rv[k] = [prettyDoc(x) for x in v]

        else:
            rv[k] = v
    return rv


def get_init(methods):
    init = [n for n in methods if method_is_init(n.name)]
    if len(init) > 1:
        raise ValueError("only one __init__ method allowed")

    rv_init = None
    if init:
        rv_init = init.pop()

    return rv_init


def get_documented_variables(node):
    rv = []
    for ix, n in enumerate(node):
        if isinstance(
            node[ix],
            (
                redbaron.nodes.StandaloneAnnotationNode,
                redbaron.nodes.AssignmentNode,
                redbaron.nodes.NameNode,
            ),
        ):
            try:
                if isinstance(node[ix + 1], redbaron.nodes.StringNode):
                    rv.append((node[ix], node[ix + 1]))
            except IndexError:
                pass

    return rv


def method_is_init(name):
    return name == "__init__"


def method_is_semi_private(name):
    return name.startswith("_") and not name.startswith("__")


def method_is_private(name):
    return name.startswith("_") and not name.endswith("__")


def method_is_dunder(name):
    return name.startswith("__") and name.endswith("__") and name is not "__init__"


def method_is_class_method(name):
    return (
        not method_is_init(name)
        and not method_is_semi_private(name)
        and not method_is_private(name)
        and not method_is_dunder(name)
    )


def is_docstring(string: typing.Union[redbaron.nodes.StringNode, str]) -> str:

    if isinstance(string, redbaron.nodes.StringNode):
        string = string.value

    if string.startswith("'''") and string.endswith("'''"):
        return string[3:][:-3]

    if string.startswith('"""') and string.endswith('"""'):
        return string[3:][:-3]

    return ""
