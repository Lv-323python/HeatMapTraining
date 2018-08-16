"""
Module for creating a producer on Sanic which sends JSON to RabbitMQ
"""
import os
import json
from app import app
from sanic import response
from sanic.response import html
from jinja2 import Template
from rabbitmq_helpers.request_sender_client import RequestSenderClient
from rabbitmq_helpers.request_sender_client_config import HOST, PORT


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
    return render_template('index.html')


@app.route("/getinfo")
async def getinfo(request):

    git_info = {
        'git_client': request.raw_args.get('git_client', ""),
        'token': request.raw_args.get('token', ""),
        'version': request.raw_args.get('version', ""),
        'repo': request.raw_args.get('repo', ""),
        'owner': request.raw_args.get('owner', ""),
        'hash': request.raw_args.get('hash', ""),
        'branch': request.raw_args.get('branch', ""),
        'action': request.raw_args.get('action', "")
    }
    request_sender_rpc = RequestSenderClient(host=HOST, port=PORT)
    data = request_sender_rpc.call(json.dumps(git_info))

    return response.json(json.loads(data))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
