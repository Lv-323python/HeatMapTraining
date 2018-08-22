"""
Module contains helper functions for rendering templates
"""

import os
from sanic.response import html
from jinja2 import Template


def render_template(html_name, **args):
    """
    Function which starts working with templates
    :param html_name:
    :param args:
    :return: html template
    """
    with open(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'templates', html_name), 'r') as file:
        html_text = file.read()
    template = Template(html_text)
    return html(template.render(args))
