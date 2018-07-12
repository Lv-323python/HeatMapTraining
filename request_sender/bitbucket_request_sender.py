"""
Contains BitbucketRequestSender class that provides methods for sending API requests
to web-based hosting service Bitbucket for version control using Git
"""

import requests

from request_sender_base import RequestSender  # pylint: disable=import-error
from utils.bitbucket_helper import to_timestamp, get_gitname, get_email


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
        Gets information about repository
        in dict format with response body and status code

        :return: dict
        :Example:
        {
            "id": "unique id",
            "repo_name": "repository name",
            "creation_date": "date",
            "owner": "repository owner",
            "url": "repository url"
        }
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
            'creation_date': str(to_timestamp(repo['created_on'])),
            'owner': repo['owner']['username'],
            'url': repo['links']['self']['href']
        }

    def get_branches(self):
        """
        Gets list of branches in a repository
        in dict format with response body and status code

        :return: list of dicts
        :Example:
        [
            {
                "name": "branch name"
            },
            ...
        ]
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
        Gets information about all commits in repository
        in dict format with response body and status code

        :return: list of dicts
        :Example:
        [
            {
                "hash": "commit hash",
                "author": "commit author",
                "message": "commit message",
                "date": "date when committed converted to int"

            },
            ...
        ]
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
                'date': str(to_timestamp(commit['date']))
            } for commit in commits_page['values']
            ]

    def get_commit_by_hash(self, hash_of_commit):
        """
        Gets information about the commit by hash
        in dict format with response body

        :param hash_of_commit: string
        :return: dict
        :Example:
        {
            "hash": "commit hash",
            "author": "commit author",
            "message": "commit message",
            "date": "date when committed converted to int"

        }
        """

        assert isinstance(hash_of_commit, str), 'Inputted "hash_of_commit" type is not str'
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
            'date': str(to_timestamp(commit['date']))
        }

    def get_commits_by_branch(self, branch_name):
        """
        Gets information about commits of a specific branch
        in dict format with response body and status code

        :param branch_name: string
        :return: list of dicts
        :Example:
        [
            {
                "hash": "commit hash",
                "author": "commit author",
                "message": "commit message",
                "date": "date when committed converted to int"

            },
            ...
        ]
        """

        assert isinstance(branch_name, str), 'Inputted "branch_name" type is not str'
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
                'date': str(to_timestamp(commit['date']))
            } for commit in commits_page['values']
            ]

    def get_contributors(self):
        """
        Gets information about all contributors to repository
        in dict format with response body

        :return: list of dicts
        :Example:
        [
             {
                 "name": "contributor name",
                 "number_of_commits": "number of commits",
                 "email": "contributor email",
                 "url": "contributor url"
             },
             ...
        ]
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
                    'name': user['username'] if user else get_gitname(author['raw']),
                    'number_of_commits': 1,  # count number of commits
                    'email': get_email(author['raw']),
                    'url': user['links']['html']['href'] if user else None
                }
            else:
                # if author is already being tracked increment number of commits by one
                contributors[commit['author']['raw']]['number_of_commits'] += 1

        return list(contributors.values())
