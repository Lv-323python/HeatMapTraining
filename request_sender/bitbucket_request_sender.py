"""
Contains BitbucketRequestSender class that provides methods for sending API requests
to web-based hosting service Bitbucket for version control using Git
"""

import datetime
import requests

from request_sender_base import RequestSender  # pylint: disable=import-error


def _timestamp(date_time_str):
    """
    Converts datetime string to timestamp

    :param date_time_str: string - datetime string
    :return: int - timestamp
    """
    return int(datetime.datetime.strptime(date_time_str[0:19], "%Y-%m-%dT%H:%M:%S").timestamp())


def _get_gitname(author_raw):
    """
    Extracts author gitname from author_raw string

    :param author_raw: string
    :return: string
    """
    return author_raw[:author_raw.find('<')-1]


def _get_email(author_raw):
    """
    Extracts author email from author_raw string

    :param author_raw: string
    :return: string
    """
    return author_raw[author_raw.find('<')+1:-1]


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
        :return: response object
        """
        return requests.get(self.base_url + endpoint)

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

        # guard condition
        if response.status_code != 200:
            return {}, response.status_code

        repo = response.json()
        return {
            'id': repo['uuid'],
            'repo_name': repo['name'],
            'creation_date': str(_timestamp(repo['created_on'])),
            'owner': repo['owner']['username'],
            'url': repo['links']['self']['href']
        }

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

        # guard condition
        if response.status_code != 200:
            return None

        branches_page = response.json()
        return [
            {
                'name': branch['name']
            } for branch in branches_page['values']
        ]

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

        # guard condition
        if response.status_code != 200:
            return None

        commits_page = response.json()
        return [
            {
                'hash': commit['hash'],
                'author': (
                    commit['author']['user']['username'] if 'user' in commit['author']
                    else commit['author']['raw']
                ),
                'message': commit['message'],
                'date': str(_timestamp(commit['date']))
            } for commit in commits_page['values']
        ]

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

        # guard condition
        if response.status_code != 200:
            return None

        # deserialize commit
        commit = response.json()
        return {
            'hash': commit['hash'],
            'author': (
                commit['author']['user']['username'] if 'user' in commit['author']
                else commit['author']['raw']
            ),
            'message': commit['message'],
            'date': str(_timestamp(commit['date']))
        }

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

        # guard condition
        if response.status_code != 200:
            return None

        commits_page = response.json()
        return [
            {
                'hash': commit['hash'],
                'author': (
                    commit['author']['user']['username'] if 'user' in commit['author']
                    else commit['author']['raw']
                ),
                'message': commit['message'],
                'date': str(_timestamp(commit['date']))
            } for commit in commits_page['values']
        ]

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

        # guard condition
        if response.status_code != 200:
            return None

        commits_page = response.json()
        contributors = {}

        # for each commit
        for commit in commits_page['values']:
            author = commit['author']  # dict with author's properties

            # author['raw'] - unique string 'user_gitname <user_email>'
            # if we haven't tracked commit author yet
            if author['raw'] not in contributors:

                # check if author has key 'user' means check if author has bitbucket account,
                #  if doesn't return  None
                user = author.get('user')

                # start tracking commit author
                contributors[author['raw']] = {
                    # if has account assign account's username else author's gitname
                    'name': user['username'] if user else _get_gitname(author['raw']),
                    'number_of_commits': 1,  # count number of commits
                    'email': _get_email(author['raw']),
                    'url': user['links']['html']['href'] if user else None
                }
            else:
                # if author is already being tracked increment number of commits by one
                contributors[commit['author']['raw']]['number_of_commits'] += 1

        return list(contributors.values())
