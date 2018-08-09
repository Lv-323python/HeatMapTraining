"""
    sanic app

    ! start to use user interface
"""
import os

import json
from jinja2 import Template
from sanic import Sanic, response
from sanic.response import html
from sanic_wtf import SanicForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

from consumer.sender import sender

APP = Sanic()


def render_template(html_name, **args):
    """

    :param html_name:
    :param args:
    :return:
    """
    with open(os.path.join(os.path.dirname(__file__), 'templates', html_name), 'r') as f_f:
        html_text = f_f.read()
    template = Template(html_text)
    return html(template.render(args))


class IndexPage(SanicForm):
    """
        Index page
    """
    git_client = StringField('Git Client', validators=[DataRequired])
    version = StringField('Version')
    token = StringField('Token')
    repository = StringField('Repository', validators=[DataRequired])
    owner = StringField('Owner', validators=[DataRequired])
    hash = StringField('Hash')
    branch = StringField('Branch')
    action = StringField('Action', validators=[DataRequired])
    submit = SubmitField('Submit')


@APP.route("/", methods=["GET", "POST"])
async def index(request):
    """

    :param request:
    :return:
    """
    form = IndexPage(request)
    if request.method == 'POST':
        git_client = form.git_client.data
        version = form.version.data
        token = form.token.data
        repository = form.repository.data
        owner = form.owner.data
        c_hash = form.hash.data
        branch = form.branch.data
        action = form.action.data
        request_dict = {'git_client': git_client,
                        'version': version,
                        'token': token,
                        'repo': repository,
                        'owner': owner,
                        'hash': c_hash,
                        'branch': branch,
                        'action': action}

        return response.json(sender(json.dumps(request_dict)))
    return render_template('index.html')


if __name__ == "__main__":
    APP.run(host="0.0.0.0", port=8000)
