from collections import namedtuple

import redbaron

from plissken.documents.function import FunctionDoc
from plissken.documents.helpers import (
    get_documented_variables,
    get_init,
    is_docstring,
    method_is_class_method,
    method_is_dunder,
    method_is_private,
    method_is_semi_private,
)
from plissken.documents.variable import VariableDoc

ClassDocument = namedtuple(
    "ClassDocument",
    [
        "name",
        "docstring",
        "init_method",
        "dunder_methods",
        "semi_private_methods",
        "private_methods",
        "class_methods",
        "variables",
    ],
)


def ClassDoc(node: redbaron.nodes.ClassNode):

    name = node.name

    docstring = ""

    try:
        if isinstance(node[0], redbaron.nodes.StringNode):
            docstring = node[0]
    except IndexError:
        docstring = ""
        pass

    docstring = is_docstring(docstring)

    methods = [FunctionDoc(n) for n in node if isinstance(n, redbaron.nodes.DefNode)]

    init_method = get_init(methods)
    dunder_methods = [n for n in methods if method_is_dunder(n.name)]
    semi_private_methods = [n for n in methods if method_is_semi_private(n.name)]
    private_methods = [n for n in methods if method_is_private(n.name)]
    class_methods = [n for n in methods if method_is_class_method(n.name)]
    class_attributes = [VariableDoc(x[0], x[1]) for x in get_documented_variables(node)]
    variables = [VariableDoc(n[0], n[1]) for n in get_documented_variables(node)]

    return ClassDocument(
        name=name,
        docstring=docstring,
        init_method=init_method,
        dunder_methods=dunder_methods,
        semi_private_methods=semi_private_methods,
        private_methods=private_methods,
        class_methods=class_methods,
        variables=variables,
    )
