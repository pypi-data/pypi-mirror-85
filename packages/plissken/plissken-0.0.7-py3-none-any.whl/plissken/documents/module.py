import os
import sys
from collections import namedtuple

import redbaron

from plissken.documents.function import FunctionDoc
from plissken.documents.helpers import get_documented_variables, is_docstring
from plissken.documents.klass import ClassDoc
from plissken.documents.variable import VariableDoc
from plissken.file_operators import code2red

ModuleDocument = namedtuple(
    "ModuleDocument",
    ["name", "docstring", "variables", "classes", "functions", "export_file_path"],
)


def get_qualified_name_from_path(file: str) -> str:

    base_name = os.path.basename(file)
    if base_name == "__init__.py":
        base_name = os.path.dirname(file)

    else:
        base_name = base_name[:-3]

    base_name = ".".join(os.path.split(base_name))

    if base_name.startswith("."):
        base_name = base_name[1:]

    return base_name


def split_all(path):
    allparts = []
    while 1:
        parts = os.path.split(path)
        if parts[0] == path:  # sentinel for absolute paths
            allparts.insert(0, parts[0])
            break
        elif parts[1] == path:  # sentinel for relative paths
            allparts.insert(0, parts[1])
            break
        else:
            path = parts[0]
            allparts.insert(0, parts[1])
    return allparts


def trim_prefix(path, package_root):
    rv = []
    path = split_all(path)
    while path:
        x = path.pop(0)
        if x == package_root:
            path.insert(0, x)
            return os.path.join(*path)


def ModuleDoc(file: str, package_root=None):
    # A Module is a python file that isn't an __init__.py file
    # It can have Variables, Classes, Methods, and/or a doc string

    node = code2red(file)

    if package_root:
        file = trim_prefix(file, package_root)

    export_file_path = os.path.splitext(file)[0]
    name = get_qualified_name_from_path(file)

    docstring = ""

    try:
        if isinstance(node[0], redbaron.nodes.StringNode):
            docstring = node[0]
    except IndexError:
        docstring = ""

    docstring = is_docstring(docstring)

    variables = [VariableDoc(n[0], n[1]) for n in get_documented_variables(node)]
    classes = [ClassDoc(n) for n in node if isinstance(n, redbaron.nodes.ClassNode)]
    functions = [FunctionDoc(n) for n in node if isinstance(n, redbaron.nodes.DefNode)]

    return ModuleDocument(
        name=name,
        docstring=docstring,
        variables=variables,
        classes=classes,
        functions=functions,
        export_file_path=export_file_path,
    )
