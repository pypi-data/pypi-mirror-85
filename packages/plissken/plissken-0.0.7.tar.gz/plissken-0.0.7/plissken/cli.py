"""
    plissken.cli
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~

    plissken's command line interface

"""

import os

import click


@click.group()
def main():
    """
    The main entry point for plissken
    :return:
    """
    pass


@main.command()
@click.argument("module_root")
@click.option("--out", type=str, default="docs")
@click.option("--format", type=str, default="md")
@click.option("--template_dir", type=str, default="")
@click.option("--template", type=str, default="")
def generate(module_root, out, format, template_dir, template):
    """
    This is a sub command on the main entry point group
    :return:
    """
    from plissken.documents.helpers import prettyDoc
    from plissken.documents.module import ModuleDocument
    from plissken.documents.package import PackageDoc, PackageDocument
    from plissken.file_operators import render_template

    def save_file(text, export_file_path):

        out_file = os.path.join(out, f"{export_file_path}.{format}")
        os.makedirs(os.path.dirname(out_file), exist_ok=True)
        with open(out_file, "w") as f:
            print(text, file=f)
        return

    def recursive_render(document):

        if isinstance(document, PackageDocument):
            render = render_template(f"{format}.template", data=prettyDoc(document))
            save_file(render, document.export_file_path)
            for package in document.sub_packages:
                recursive_render(package)
            for module in document.modules:
                recursive_render(module)
            return
        if isinstance(document, plissken.documents.module.ModuleDocument):
            render = render_template(f"{format}.template", data=prettyDoc(document))
            save_file(render, document.export_file_path)
            return

    package_docs = PackageDoc(module_root, package_root=os.path.basename(module_root))

    recursive_render(package_docs)

    pass
