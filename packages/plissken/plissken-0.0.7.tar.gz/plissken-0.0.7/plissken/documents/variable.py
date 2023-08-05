import typing
from collections import namedtuple

import redbaron

from plissken.documents.helpers import is_docstring

VariableDocument = namedtuple("VariableDocument", ["name", "annotation", "docstring"])


def VariableDoc(
    node: typing.Union[
        redbaron.nodes.NameNode,
        redbaron.nodes.AssignmentNode,
        redbaron.nodes.StandaloneAnnotationNode,
    ],
    doc: redbaron.nodes.StringNode,
):

    name = ""
    annotation = ""
    docstring = ""

    if isinstance(node, redbaron.nodes.NameNode):
        name = node.value
        try:
            annotation = node.annotation.value
        except:
            annotation = ""

    elif isinstance(node, redbaron.nodes.AssignmentNode):
        name = node.target.value
        try:
            annotation = node.annotation.value
        except:
            annotation = ""

    elif isinstance(node, redbaron.nodes.StandaloneAnnotationNode):
        name = node.target.value
        try:
            annotation = node.annotation.value
        except:
            annotation = ""
    else:
        raise ValueError(Node)

    docstring = is_docstring(doc)

    if not docstring:
        raise ValueError(
            f"The docstring for {name} doesn't appear valid. Got: {doc.value}"
        )
    return VariableDocument(name=name, annotation=annotation, docstring=docstring)
