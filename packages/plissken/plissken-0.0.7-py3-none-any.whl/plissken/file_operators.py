import os

from jinja2 import ChoiceLoader, Environment, FileSystemLoader, select_autoescape
from redbaron import RedBaron


def code2red(filename: str) -> RedBaron:
    with open(filename) as sc:
        red = RedBaron(sc.read())
    return red


def render_template(template, data, directory=None) -> str:

    loader_list = [
        os.path.join(os.path.abspath(os.path.dirname(__file__)), "templates")
    ]
    if directory:
        if not isinstance(directory, list):
            directory = [directory]
        directory = [os.path.abspath(d) for d in directory]
        loader_list = directory + loader_list

    loader_list = [FileSystemLoader(d) for d in loader_list]

    env = Environment(
        loader=ChoiceLoader(loader_list),
        autoescape=select_autoescape(),
        extensions=["jinja2.ext.do"],
    )
    template = env.get_template(template)
    return template.render(data=data)
