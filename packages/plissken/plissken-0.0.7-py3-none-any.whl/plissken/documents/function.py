from collections import namedtuple

import redbaron

from plissken.documents.helpers import is_docstring

ArgumentDocument = namedtuple("ArgumentDocument", ["name", "default", "annotation"])
DecoratorDocument = namedtuple("DecoratorDocument", ["name", "arguments"])
FunctionDocument = namedtuple(
    "FunctionDocument",
    [
        "name",
        "async_",
        "arguments",
        "docstring",
        "decorators",
        "code",
        "return_annotation",
    ],
)


def FunctionDoc(node: redbaron.nodes.DefNode) -> FunctionDocument:
    """
    A Function is a type of python construct within a Module.
    """
    doc_string = ""

    try:
        if isinstance(node[0], redbaron.nodes.StringNode):
            doc_string = node[0]
    except IndexError:
        doc_string = ""

    decorators = []
    if node.decorators:
        decorators = _generate_decorators(node.decorators)

    return FunctionDocument(
        name=node.name,
        async_=node.async_ or False,
        arguments=_generate_arguments(node.arguments),
        docstring=is_docstring(doc_string),
        decorators=decorators,
        return_annotation=node.return_annotation,
        code=node.dumps(),
    )


def _generate_decorators(
    node_list: redbaron.base_nodes.DecoratorsLineProxyList
) -> list:
    decorators = []
    for decorator in node_list:

        assert isinstance(decorator, redbaron.nodes.DecoratorNode)

        call_arguments = []
        if decorator.call:
            for call in decorator.call:
                name = call.value.value

                value = ""
                if call.target:
                    value = call.target.value

                annotation = ""
                call_arguments.append(
                    ArgumentDocument(name=name, default=value, annotation=annotation)
                )

        name_list = decorator.value.value
        decorator_name = "@" + ".".join(
            [x.value for x in name_list if isinstance(x, redbaron.nodes.NameNode)]
        )

        decorators.append(
            DecoratorDocument(name=decorator_name, arguments=call_arguments)
        )
    return decorators


def _generate_arguments(node_list: redbaron.base_nodes.CommaProxyList) -> list:
    args = []
    for arg in node_list:
        if isinstance(arg, redbaron.nodes.DefArgumentNode):

            name = arg.target.value
            default = ""
            annotation = ""
            if arg.value:
                default = arg.value.value
            if arg.annotation:
                annotation = arg.annotation.value
            args.append(
                ArgumentDocument(name=name, default=default, annotation=annotation)
            )

        if isinstance(arg, redbaron.nodes.ListArgumentNode):
            args.append(
                ArgumentDocument(name=f"*{arg.value.value}", default="", annotation="")
            )

        if isinstance(arg, redbaron.nodes.DictArgumentNode):
            args.append(
                ArgumentDocument(name=f"**{arg.value.value}", default="", annotation="")
            )

    return args
