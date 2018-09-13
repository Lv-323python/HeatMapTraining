"""
Module for creating a producer on Sanic which sends JSON to RabbitMQ
"""
import json
from app import app, auth
from app.helpers.template import render_template
from sanic import response
from rabbitmq_helpers.request_sender_client import RequestSenderClient
from rabbitmq_helpers.request_sender_client_config import HOST, PORT
from mongodb_helpers.mongodb_client import MongoDBClient
from plot_herpers.heatmap import CommitsHeatmap
from app.models.user import get_user_by_name, get_user_by_email, register_user
from app.models.user_request import get_repo_info, save_repo_info, delete_repo_info,\
    update_repo_info, get_repo_info_row
from general_helper.logger.log_config import LOG


@app.route('/', methods=['GET', 'POST'])
@auth.login_required
async def index(request):
    """Routing function for main page"""
    return render_template('index.html')


@app.route("/getinfo")
@auth.login_required(user_keyword='user')
async def getinfo(request, user):
    git_info = {
        'username': user.username,
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
    if json.loads(data) == None:
        return response.json({
            'message': 'no such url'
        }, status=400)
    return response.json(json.loads(data))


@app.route("/getheatdict")
@auth.login_required(user_keyword='user')
async def getheatdict(request, user):
    date_unit = 'D' or request.raw_args.get('date_unit', "")

    key_nodes = {
        'username': user.username,
        'git_client': request.raw_args.get('git_client', ""),
        'version': request.raw_args.get('version', ""),
        'repo': request.raw_args.get('repo', ""),
        'owner': request.raw_args.get('owner', "")
    }
    mongo_key = '-'.join(key_nodes.values())

    mongo_client = MongoDBClient()
    repository_document = mongo_client.get_entry(mongo_key)

    data_dict = None
    if repository_document:
        commits_heatmap = CommitsHeatmap.from_repository_doc(repository_document, date_unit)
        data_dict = commits_heatmap.get_data_dict()

    return response.json(data_dict)


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


@app.route('/user/requests', methods=['GET', 'POST'])
@auth.login_required(user_keyword='user', handle_no_auth=handle_no_auth)
async def get_repos(request, user):
    if request.method == 'GET':
        res = [repo.to_dict() for repo in get_repo_info(user.id)]
        return response.json(res)

    data = json.loads(request.body)
    git_info = {
        'user_id': user.id,
        'git_client': data.get('git_client', ""),
        'token': data.get('token', ""),
        'version': data.get('version', ""),
        'repo': data.get('repo', ""),
        'owner': data.get('owner', ""),
        'hash': data.get('hash', ""),
        'branch': data.get('branch', ""),
        'action': data.get('action', "")
    }

    save_repo_info(git_info)
    return response.json({
        'message': 'saved'
    }, status=201)


@app.route('/table/<id>', methods=['GET', 'DELETE', 'PUT'])
@auth.login_required(user_keyword='user', handle_no_auth=handle_no_auth)
async def interaction_with_row(request, user, id):
    if request.method == 'GET':
        res = json.dumps(get_repo_info_row(id).to_dict())
        return response.json(json.loads(res))

    if request.method == 'DELETE':
        delete_count = delete_repo_info(id)
        if delete_count:
            return response.json({
                'message': 'deleted'
            }, status=200)
        return response.json({
            'message': 'no such element'
        }, status=400)

    if request.method == 'PUT':
        data = json.loads(request.body)
        git_info = {
            'git_client': data.get('git_client', ""),
            'token': data.get('token', ""),
            'version': data.get('version', ""),
            'repo': data.get('repo', ""),
            'owner': data.get('owner', ""),
            'hash': data.get('hash', ""),
            'branch': data.get('branch', ""),
            'action': data.get('action', "")
        }
        update_count = update_repo_info(id, git_info)
        if update_count:
            return response.json({
                'message': 'updated'
            }, status=200)
        return response.json({
            'message': 'no such element, not updated'
        }, status=400)
