"""
Module for creating a producer on Sanic which sends JSON to RabbitMQ
"""
import json
from app import app, auth
from app.helpers.template import render_template
from sanic import response
from rabbitmq_helpers.request_sender_client import RequestSenderClient
from rabbitmq_helpers.request_sender_client_config import HOST, PORT
from mongodb_helpers.mongo_response_builder import MongoResponseBuilder, HEAT_CHOICES
from app.models.user import get_user_by_name, get_user_by_email, register_user
from general_helper.logger.log_config import LOG


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


@app.route("/getheatdict")
@auth.login_required
async def getheatdict(request):
    git_info = {
        'git_client': request.raw_args.get('git_client', ""),
        'token': request.raw_args.get('token', ""),
        'repo': request.raw_args.get('repo', ""),
        'owner': request.raw_args.get('owner', ""),
        'form_of_date': request.raw_args.get('form_of_date', "")
    }
    mongo_builder=MongoResponseBuilder()
    return response.json(mongo_builder.build_heat_dict(git_info))


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


@app.route('/register', methods=['GET', 'POST'])
def register(request):
    if auth.current_user(request):
        return response.redirect('/')

    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        if not get_user_by_name(username) and not get_user_by_email(email):
            register_user(username, email, password)
            return response.redirect(app.url_for('login'))
    return render_template('register.html')


def handle_no_auth(request):
    return response.json(dict(message='unauthorized'), status=401)


@app.route('/api/user')
@auth.login_required(user_keyword='user', handle_no_auth=handle_no_auth)
async def api_profile(request, user):
    return response.json(dict(id=user.id, name=user.username))
