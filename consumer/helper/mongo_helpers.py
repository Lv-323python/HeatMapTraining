from functools import wraps
import json
from helper.mongodb_client import MongoDBClient

def mongo_store(worker_f):

    @wraps(worker_f)
    def decorator(body):

        body = json.loads(body)
        mongo_client = MongoDBClient()
        key_nodes = {
            'username': body['username'],
            'git_client': body['git_client'],
            'version': body['version'],
            'repo': body['repo'],
            'owner': body['owner']
        }

        #  !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

        response = None
        detailed_response = None
        if body['action'] == 'get_commits':
            key = '-'.join(key_nodes.values())
            response = mongo_client.get_entry(key)

        if not response:
            response = worker_f(**body)
            detailed_response = response
            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            # store in db only if get_commits was chosen
            if body['action'] == 'get_commits':
                body['action'] = 'get_repo'
                repo_info = worker_f(**body)

                detailed_response = {
                    'repo': repo_info,
                    'branches': None,
                    'commits': response,
                    'contributors': None
                }
                mongo_client.set_entry(key, detailed_response)
            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        return detailed_response

    return decorator




