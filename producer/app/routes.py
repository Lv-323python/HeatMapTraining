"""
Module for creating a producer on Sanic which sends JSON to RabbitMQ
"""
import os
import json
from app import app
from sanic import response
from sanic.response import html
from sanic_wtf import SanicForm
from wtforms import SubmitField, TextField
from jinja2 import Template
from rabbitmq_helpers.request_sender_client import RequestSenderClient
from rabbitmq_helpers.request_sender_client_config import HOST, PORT


class FeedbackForm(SanicForm):
    """Provides basic form for input receiving from user"""
    git_client = TextField('git_client')
    version = TextField('version')
    token = TextField('token')
    repo = TextField('repo')
    owner = TextField('owner')
    hash = TextField('hash')
    branch = TextField('branch')
    action = TextField('action')
    submit = SubmitField('Submit')


def render_template(html_name, **args):
    """
    Function which starts working with templates
    :param html_name:
    :param args:
    :return: html template
    """
    with open(os.path.join(os.path.dirname(__file__), 'templates', html_name), 'r') as file:
        html_text = file.read()
    template = Template(html_text)
    return html(template.render(args))


@app.route('/', methods=['GET', 'POST'])
async def index(request):
    """Routing function for main page"""
    form = FeedbackForm(request)
    if request.method == 'POST':
        git_client = form.git_client.data
        token = form.token.data
        version = form.version.data
        repo = form.repo.data
        owner = form.owner.data
        hash = form.hash.data
        branch = form.branch.data
        action = form.action.data
        git_info = {
            'git_client': git_client,
            'token': token,
            'version': version,
            'repo': repo,
            'owner': owner,
            'hash': hash,
            'branch': branch,
            'action': action}

        request_sender_rpc = RequestSenderClient(host=HOST, port=PORT)
        data = request_sender_rpc.call(json.dumps(git_info))

        return response.json(json.loads(data))
    return render_template('index.html')

