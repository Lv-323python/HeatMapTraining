"""
Contains BitbucketRequestSender class that provides methods for sending API requests
to web-based hosting service Bitbucket for version control using Git
"""

import datetime
import json
import requests

from request_sender_base import RequestSender  # pylint: disable=import-error


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


def _get_username(commit):
    """
    Returns username after check for user field.

    :param commit: dict - commit information
    :return: str - commit username from 'user' or from 'raw'
    """

    if 'user' in commit:
        result_name = commit['user']['username']
    else:
        result_name = commit['raw'][1:commit['raw'].find('<') - 1]
    return result_name


def _parse_repo(repo):
    """
    Returns information about repository so that it matches specified format

    Example:
    {
        "id": "unique id",
        "repo_name": "repository name",
        "creation_date": "date",
        "owner": "repository owner",
        "url": "repository url"
    }

    :param repo: dict - contains information about repository
    :return: dict - contains information about repository in specified format
    """

    return {
        'id': repo['uuid'],
        'repo_name': repo['name'],
        'creation_date': str(_timestamp(repo['created_on'])),
        'owner': repo['owner']['username'],
        'url': repo['links']['self']['href']
    }


def _parse_branch(branch):
    """
    Returns information about branch so that it matches specified format

    Example:
    {
        "id": "unique id",
        "repo_name": "repository name",
        "creation_date": "date",
        "owner": "repository owner",
        "url": "repository url"
    }

    :param branch: dict - contains information about branch
    :return: dict - contains information about branch in specified format
    """
    return {
        'name': branch['name']
    }


def _parse_commit(commit):
    """
    Returns information about commit so that it matches specified format

    Example:
    {
        "id": "unique id",
        "repo_name": "repository name",
        "creation_date": "date",
        "owner": "repository owner",
        "url": "repository url"
    }

    :param repo: dict - contains information about commit
    :return: dict - contains information about commit in specified format
    """
    return {
        'hash': commit['hash'],
        'author': (
            commit['author']['user']['username'] if 'user' in commit['author']
            else commit['author']['raw']
        ),
        'message': commit['message'],
        'date': str(_timestamp(commit['date']))
    }


def _parse_paginated(deserialized_page_obj, parser):
    """
    Returns list of parsed values using specified parser function

    :param deserialized_page_obj: dict - that represents deserialized page of values
    :param parser: function - will be applied to each element on the page
    :return: list of parsed values
    """

    values = []
    for value in deserialized_page_obj['values']:
        values.append(parser(value))
    return values


def _parse_branches(branches_page):
    """
    Returns list of dicts that contain information about branch so that it matches specified format

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
    return _parse_paginated(deserialized_page_obj=branches_page, parser=_parse_branch)


def _parse_commits(commits_page):
    """
    Returns list of dicts that contain information about commmit so that it matches specified format

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
    return _parse_paginated(deserialized_page_obj=commits_page, parser=_parse_commit)


def _parse_contributors(deserialized_commits):
    """
    Returns list of dicts that contain information about contributors
    so that it matches specified format

    Example:
    [
        {
            "name": "contributor name",
            "number_of_commits": "number of commits",
            "email": "contributor email",
            "url": "contributor url"
        },
        ...
    ]
    :param response: string
    :return: list of dicts
    """

    commits = [repo_name['author'] for repo_name in deserialized_commits['values']]

    contributors_inf = \
        {_get_username(contrib): {
            'raw': contrib['raw'],
            'href': contrib['user']['links']['html']['href'] if 'user' in contrib else 'None'
        } for contrib in commits}

    result = \
        [{'name': contrib,
          'number_of_commits':
              len(list(filter(lambda x, cont=contrib: _get_username(x) == cont, commits))),
          'email':
              contributors_inf[contrib]['raw'][contributors_inf[contrib]['raw'].find('<') + 1:-1],
          'url': contributors_inf[contrib]['href']} for contrib in contributors_inf.keys()]
    return result


class BitbucketRequestSender(RequestSender):
    """
    Provides methods for sending API requests to web-based hosting service Bitbucket
    for version control using Git
    """

    def __init__(self, owner, repo, base_url='https://api.bitbucket.org/2.0'):
        super().__init__(base_url=base_url, owner=owner, repo=repo)

    def _get_request(self, endpoint):
        """
        Sends GET request to URL

        :param endpoint: string - endpoint url
        :return: string - in JSON format
        """
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

        :return: dict - contains information about repository in specified format
        """

        repo_endpoint = f'/repositories/{self.owner}/{self.repo}'
        response = self._get_request(repo_endpoint)
        deserialized_repo = _deserialize(response)
        return _parse_repo(deserialized_repo)

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

        :return: list of dicts
        """

        branches_endpoint = f'/repositories/{self.owner}/{self.repo}/refs/branches'
        response = self._get_request(branches_endpoint)
        deserialized_branches = _deserialize(response)
        return _parse_branches(deserialized_branches)

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

        :return: list of dicts
        """

        commits_endpoint = f'/repositories/{self.owner}/{self.repo}/commits'
        response = self._get_request(commits_endpoint)
        deserialized_commits = _deserialize(response)
        return _parse_commits(deserialized_commits)

    def get_commit_by_hash(self, hash_of_commit):
        """
        returns JSON formatted information about commit by its hash

        Example:
        {
                "hash": "commit hash",
                "author": "commit author",
                "message": "commit message",
                "date": "date when committed"
        }

        :return: dict - contains information about commit in specified format
        """

        commit_endpoint = f'/repositories/{self.owner}/{self.repo}/commit/{hash_of_commit}'
        response = self._get_request(commit_endpoint)
        deserialized_commit = _deserialize(response)
        return _parse_commit(deserialized_commit)

    def get_commits_by_branch(self, branch_name):
        """
        Returns information about commits (in branch specified)

        example:
        [
            {
                "hash": "commit hash",
                "author": "commit author",
                "message": "commit message",
                "date": "date when committed"

            },
            ...
        ]

        :param branch_name: string
        :return: list of dicts
        """
        branch_commits_endpoint = f'/repositories/{self.owner}/{self.repo}/commits/{branch_name}'
        response = self._get_request(branch_commits_endpoint)
        deserialized_branch_commits = _deserialize(response)
        return _parse_commits(deserialized_branch_commits)

    def get_contributors(self):
        """
        Returns information about contributors in JSON format
        Example:
        [
            {
                "name": "contributor name",
                "number_of_commits": "number of commits",
                "email": "contributor email",
                "url": "contributor url"
            },
            ...
        ]

        :return: list of dicts
        """

        commits_endpoint = f'/repositories/{self.owner}/{self.repo}/commits'
        response = self._get_request(commits_endpoint)
        deserialized_commits = _deserialize(response)
        return _parse_contributors(deserialized_commits)
