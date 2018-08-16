"""
Module for creating a producer on Sanic which sends JSON to RabbitMQ
"""
import os
import json
from app import app, auth
from sanic import response
from sanic.response import html
from jinja2 import Template
from rabbitmq_helpers.request_sender_client import RequestSenderClient
from rabbitmq_helpers.request_sender_client_config import HOST, PORT
from app.models.user import get_user_by_name
from ast import literal_eval



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
@auth.login_required
async def index(request):
    """Routing function for main page"""
    return render_template('index.html')


@app.route("/getinfo")
@auth.login_required
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


@app.route('/login', methods=['GET', 'POST'])
async def login(request):
    if auth.current_user(request):
        return response.redirect('/')
    if request.method == 'POST':
        data = json.loads(request.body)
        user = get_user_by_name(data.get('username'))
        if user and user.check_password(data.get('password')):
            auth.login_user(request, user)
            return response.json({
                'message': 'succesfully logined'
            }, status=200)
        return response.json({
            'message': 'invalid username or password'
        }, status=400)

    return render_template('login.html')


@app.route('/logout')
@auth.login_required
async def logout(request):
    auth.logout_user(request)
    return response.redirect('/login')


# @app.route('/')
# @auth.login_required(user_keyword='user')
# async def profile(request, user):
#     content = '<a href="/logout">Logout</a><p>Welcome, %s</p>' % user.username
#     return response.html(content)


def handle_no_auth(request):
    return response.json(dict(message='unauthorized'), status=401)


@app.route('/api/user')
@auth.login_required(user_keyword='user', handle_no_auth=handle_no_auth)
async def api_profile(request, user):
    return response.json(dict(id=user.id, name=user.username))
