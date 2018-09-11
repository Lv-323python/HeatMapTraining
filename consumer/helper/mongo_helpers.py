from functools import wraps
import json
from helper.mongodb_client import MongoDBClient

def mongo_store(worker_f):

    @wraps(worker_f)
    def decorator(body):

        body = json.loads(body)

        if body['action'] == 'pull_repo':

            mongo_client = MongoDBClient()
            key_nodes = {
                'username': body['username'],
                'git_client': body['git_client'],
                'version': body['version'],
                'repo': body['repo'],
                'owner': body['owner']
            }

            mongo_key = '-'.join(key_nodes.values())
            mongo_response = mongo_client.get_entry(mongo_key)
            if mongo_response:
                # works only for bitbucket
                # NOTE: updating only commits info !!
                mongo_response = mongo_response.get('value')

                body['action'] = 'get_updated_all_commits'
                body['old_commits'] = mongo_response['commits']
                mongo_response['commits'] = worker_f(**body)
                # just to notify the user
                response = {'message': f'Successfully updated repository!'}
            else:
                mongo_response = {}
                for action, key in [('get_repo', 'repo'),
                                    ('get_all_commits', 'commits'),
                                    ('get_branches', 'branches'),
                                    ('get_contributors', 'contributors')]:

                    body['action'] = action
                    mongo_response[key] = worker_f(**body)
                response = {'message': f'Successfully pulled repository down!'}

            mongo_client.set_entry(mongo_key, mongo_response)

        else:
            response = worker_f(**body)

        return response

    return decorator




