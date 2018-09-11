from functools import wraps
import json
from helper.mongodb_client import MongoDBClient

def mongo_store(worker_f):

    @wraps(worker_f)
    def decorator(body):

        body = json.loads(body)


        #  !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

        response = None
        detailed_response = None
        # if body['action'] == 'pull_repo':
        #     key = '-'.join(key_nodes.values())
        #     response = mongo_client.get_entry(key)

        if not response:
            response = worker_f(**body)
            detailed_response = response
            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            # store in db only if get_commits was chosen
            if body['action'] == 'pull_repo':

                mongo_client = MongoDBClient()
                key_nodes = {
                    'username': body['username'],
                    'git_client': body['git_client'],
                    'version': body['version'],
                    'repo': body['repo'],
                    'owner': body['owner']
                }

                key = '-'.join(key_nodes.values())
                response = mongo_client.get_entry(key)
                if response:
                    body['action'] = 'get_all'
                    # get updated commits
                    pass
                else:
                    for action, key in [('get_repo', 'repo'),
                                        ('get_commits', 'commits'),
                                        ('get_branches', 'branches'),
                                        ('get_contributors', 'contributors')]:

                        body['action'] = action
                        detailed_response['key'] = worker_f(**body)

                    mongo_client.set_entry(key, detailed_response)
            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        return detailed_response

    return decorator




