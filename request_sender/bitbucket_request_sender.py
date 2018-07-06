"""
Contains BitbucketRequestSender class that provides methods for sending API requests
to web-based hosting service Bitbucket for version control using Git
"""

import datetime
import json
import requests

from request_sender_base import RequestSender


def _timestamp(date_time_str):
    """
    Converts datetime string to timestamp

    :param date_time_str: string - datetime string
    :return: int - timestamp
    """
    return int(datetime.datetime.strptime(date_time_str[0:19], "%Y-%m-%dT%H:%M:%S").timestamp())


def _deserialize(json_text):
    """
    Deserializes JSON formatted text

    :param json_text: string - text in JSON format
    :return: deserialized python objects
    """
    return json.loads(json_text)


def _parse_repo_response(response):
    """
    Returns request response so that it matches specified format

    Example:
    {
        "id": "unique id",
        "repo_name": "repository name",
        "creation_date": "date",
        "owner": "repository owner",
        "url": "repository url"
    }

    :param response: string
    :return: dict - repo info
    """
    deserialized_response = _deserialize(response)
    repo_info = {
        'id': deserialized_response['uuid'],
        'repo_name': deserialized_response['name'],
        'creation_date': str(_timestamp(deserialized_response['created_on'])),
        'owner': deserialized_response['owner']['username'],
        'url': deserialized_response['links']['self']['href']
    }
    return repo_info


def _parse_branches_response(response):
    """
    Returns request response so that it matches specified format
    Example:
    [
        {
            "name": "branch name"
        },
        ...
    ]

    :param response: string
    :return: list of dicts
    """
    branches_info = []
    deserialized_response = _deserialize(response)
    for branch in deserialized_response['values']:
        branches_info.append({
            'name': branch['name']
        })
    return branches_info


def _parse_commits_response(response):
    """
    Returns request response so that it matches specified format
    Example:
    [
        {
            "hash": "commit hash",
            "author": "commit author",
            "message": "commit message",
            "date": "date when committed"
        },
        ...
    ]

    :param response: string
    :return: list of dicts
    """

    commits_info = []
    deserialized_response = _deserialize(response)
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


class BitbucketRequestSender(RequestSender):
    """
    Provides methods for sending API requests to web-based hosting service Bitbucket
    for version control using Git
    """

    def __init__(self, owner, name, base_url='https://api.bitbucket.org/2.0'):
        super().__init__(base_url=base_url, owner=owner, name=name)

    def _get_request(self, endpoint):
        return requests.get(self.base_url + endpoint).text

    def get_repo(self):
        """
        returns repository info in JSON format
        Example:
        {
            "id": "unique id",
            "repo_name": "repository name",
            "creation_date": "date",
            "owner": "repository owner",
            "url": "repository url"
        }

        :return: string - JSON formatted response
        """

        repo_endpoint = f'/repositories/{self.owner}/{self.name}'
        response = self._get_request(repo_endpoint)
        return _parse_repo_response(response)

    def get_branches(self):
        """
        returns information about branches in JSON format
        Example:
        [
            {
                "name": "branch name"
            },
            ...
        ]

        :return: string - JSON formatted response
        """

        branches_endpoint = f'/repositories/{self.owner}/{self.name}/refs/branches'
        response = self._get_request(branches_endpoint)
        return _parse_branches_response(response)

    def get_commits(self):
        """
        Returns information about commits in JSON format
        Example:
        [
            {
                "hash": "commit hash",
                "author": "commit author",
                "message": "commit message",
                "date": "date when committed"
            },
            ...
        ]

        :return: string - JSON formatted response
        """

        commits_endpoint = f'/repositories/{self.owner}/{self.name}/commits'
        response = self._get_request(commits_endpoint)
        return _parse_commits_response(response)
