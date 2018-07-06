"""
Contains BitbucketRequestSender class that provides methods for sending API requests
to web-based hosting service Bitbucket for version control using Git
"""

import datetime
import json
import requests

from request_sender_base import RequestSender


def _timestamp(date_time_str):
    return datetime.datetime.strptime(date_time_str[0:19], "%Y-%m-%dT%H:%M:%S").timestamp()


class BitbucketRequestSender(RequestSender):
    """
    Provides methods for sending API requests to web-based hosting service Bitbucket
    for version control using Git
    """

    def __init__(self, base_url='https://api.bitbucket.org/2.0'):
        super().__init__(base_url)

    def _get_request(self, endpoint):
        return requests.get(self.base_url + endpoint).text

    @staticmethod
    def _deserialize(json_text):
        return json.loads(json_text)


    def _parse_repo_response(self, response):
        deserialized_response = self._deserialize(response)
        repo_info = {
            'id': deserialized_response['uuid'],
            'repo_name': deserialized_response['name'],
            'creation_date': str(_timestamp(deserialized_response['created_on'])),
            'owner': deserialized_response['owner']['username'],
            'url': deserialized_response['links']['self']['href']
        }

        return repo_info

    def _parse_branches_response(self, response):
        branches_info = []
        deserialized_response = self._deserialize(response)
        for branch in deserialized_response['values']:
            branches_info.append({
                'name': branch['name']
            })

        return branches_info

    def _parse_commits_response(self, response):
        commits_info = []
        deserialized_response = self._deserialize(response)
        for commit in deserialized_response['values']:
            commits_info.append({
                'hash': commit['hash'],
                'author': (
                    commit['author']['user']['username'] if 'user' in commit['author']
                    else commit['author']['raw']
                ),
                'message': commit['message'],
                'date': str(_timestamp(commit['date']))
            })
        return commits_info

    def get_repo(self, name, owner):
        repo_endpoint = f'/repositories/{owner}/{name}'
        response = self._get_request(repo_endpoint)
        return self._parse_repo_response(response)

    def get_branches(self, name, owner):
        branches_endpoint = f'/repositories/{owner}/{name}/refs/branches'
        response = self._get_request(branches_endpoint)
        return self._parse_branches_response(response)

    def get_commits(self, name, owner):
        commits_endpoint = f'/repositories/{owner}/{name}/commits'
        response = self._get_request(commits_endpoint)
        return self._parse_commits_response(response)
