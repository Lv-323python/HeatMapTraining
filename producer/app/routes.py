"""
Module for creating a producer on Sanic which sends JSON to RabbitMQ
"""
import os
import json
from app import app, auth
from sanic import response
from sanic.response import html
from sanic_wtf import SanicForm
from wtforms import SubmitField, TextField
from jinja2 import Template
from rabbitmq_helpers.request_sender_client import RequestSenderClient
from rabbitmq_helpers.request_sender_client_config import HOST, PORT
from app.database import scoped_session
from app.models.user import User, get_user_by_name


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

#
# @app.route('/', methods=['GET', 'POST'])
# async def index(request):
#     """Routing function for main page"""
#     form = FeedbackForm(request)
#     if request.method == 'POST':
#         git_client = form.git_client.data
#         token = form.token.data
#         version = form.version.data
#         repo = form.repo.data
#         owner = form.owner.data
#         hash = form.hash.data
#         branch = form.branch.data
#         action = form.action.data
#         git_info = {
#             'git_client': git_client,
#             'token': token,
#             'version': version,
#             'repo': repo,
#             'owner': owner,
#             'hash': hash,
#             'branch': branch,
#             'action': action}
#
#         request_sender_rpc = RequestSenderClient(host=HOST, port=PORT)
#         data = request_sender_rpc.call(json.dumps(git_info))
#
#         return response.json(json.loads(data))
#     return render_template('index.html')






@app.route('/login', methods=['GET', 'POST'])
async def login(request):
    if auth.current_user(request):
        return response.redirect('/')
    if request.method == 'POST':
        user = get_user_by_name(request.form.get('username'))
        if user and user.check_password(request.form.get('password')):
            auth.login_user(request, user)
            return response.json({
                'message': 'succesfully logined'
            }, status=200)
        return response.json({
            'message': 'invalid username or password'
        }, status=400)



        # with scoped_session() as session:
        #     user = session.query(User).filter_by(username=request.form.get('username')).first()
        #     #user = User.query.filter_by(username=request.form.get('username')).first()
        #     #user = User.query.filter_by(username=request.form.get('username')).first()
        #     if user is None or not user.check_password(request.form.get('password')):
        #         message = 'invalid username or password'
        #         return response.redirect('/')
        #     auth.login_user(request, user)
        #     return response.redirect('/')

        # # for demonstration purpose only, you should use more robust method
        # if username == 'demo' and password == '1234':
        #     # use User proxy in sanic_auth, this should be some ORM model
        #     # object in production, the default implementation of
        #     # auth.login_user expects User.id and User.name available
        #     user = User(id=1, name=username)
        #     auth.login_user(request, user)
        #     return response.redirect('/')
        # message = 'invalid username or password'
    return response.html(LOGIN_FORM)


@app.route('/logout')
@auth.login_required
async def logout(request):
    auth.logout_user(request)
    return response.redirect('/login')


@app.route('/')
@auth.login_required(user_keyword='user')
async def profile(request, user):
    content = '<a href="/logout">Logout</a><p>Welcome, %s</p>' % user.username
    return response.html(content)


def handle_no_auth(request):
    return response.json(dict(message='unauthorized'), status=401)


@app.route('/api/user')
@auth.login_required(user_keyword='user', handle_no_auth=handle_no_auth)
async def api_profile(request, user):
    return response.json(dict(id=user.id, name=user.username))


