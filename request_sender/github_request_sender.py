"""
Contains GithubRequestSender class that provides implementation of
interface for sending API requests
to web-based hosting services for version control using GitHub
"""
import requests
from request_sender_base import RequestSender  # pylint: disable=import-error
from utils.helper import format_date_to_int

GITHUB_TIME_FORMAT = "%Y-%m-%dT%H:%M:%SZ"


class GithubRequestSender(RequestSender):
    """
    Class that provides implementation of interface for sending API requests
    to web-based hosting services for version control using GitHub
    """

    def __init__(self, owner, repo, base_url="https://api.github.com"):
        RequestSender.__init__(self,
                               base_url=base_url,
                               owner=owner,
                               repo=repo)
        self.repos_api_url = f'/repos/{self.owner}/{self.repo}'

    def get_repo(self):
        """
        Gets information about repository
        in dict format with response body and status code

        :return: dict,
        :raise NotImplementedError
        :Example:
        {
            "id": "unique id",
            "repo_name": "repository name",
            "creation_date": "date",
            "owner": "repository owner",
            "url": "repository url"
        }
        """

        endpoint = self.repos_api_url
        response = requests.get(self.base_url + endpoint)
        if not response.status_code == 200:
            return None
        response = response.json()
        repo = {'id': response['id'],
                'repo_name': response['name'],
                'creation_date': format_date_to_int(response['created_at'], GITHUB_TIME_FORMAT),
                'owner': response['owner']['login'],
                'url': response['url']}
        return repo

    def get_branches(self):
        """
        Gets list of branches in a repository
        in dict format with response body and status code

        :return: dict
        :raise NotImplementedError
        :Example:
        [
            {
                "name": "branch name"
            },
            ...
        ]
        """
        endpoint = self.repos_api_url + '/branches'
        url = self.base_url + endpoint
        response = requests.get(url)
        if not response.status_code == 200:
            return None
        response = response.json()
        return list(map(lambda x: {'name': x['name']}, response))

    def get_commits(self):
        """
        Gets information about all commits in repository
        in dict format with response body and status code

        :return: dict
        :raise NotImplementedError
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
        endpoint = self.repos_api_url + '/commits'
        response = requests.get(self.base_url + endpoint)
        if not response.status_code == 200:
            return None
        response = response.json()
        return [
            {'hash': commit['sha'],
             'author': commit['commit']['author']['name'],
             'message': commit['commit']['message'],
             'date': format_date_to_int(commit['commit']['author']['date'], GITHUB_TIME_FORMAT)}
            for commit in response]

    def get_commits_by_branch(self, branch_name):
        """
        Gets information about commits of a specific branch
        in dict format with response body and status code

        :param branch_name: string
        :return: dict
        :raise NotImplementedError
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
        endpoint = self.repos_api_url + f'/commits?sha={branch_name}'
        url = self.base_url + endpoint
        response = requests.get(url)
        if not response.status_code == 200:
            return None
        response = response.json()
        return list(map(lambda x: {
            'hash': x['sha'],
            'author': x['commit']['author']['name'],
            'message': x['commit']['message'],
            'date': format_date_to_int(x['commit']['author']['date'], GITHUB_TIME_FORMAT)
        }, response))

    def get_commit_by_hash(self, hash_of_commit):
        """
        Gets information about the commit by hash
        in dict format with response body

        :param hash_of_commit: string
        :return: dict
        :raise NotImplementedError
        :Example:
        {
            "hash": "commit hash",
            "author": "commit author",
            "message": "commit message",
            "date": "date when committed converted to int"

        }
        """
        endpoint = self.repos_api_url + f'/commits/{hash_of_commit}'
        response = requests.get(self.base_url + endpoint)
        if not response.status_code == 200:
            return None
        response = response.json()
        return {
            'hash': response['sha'],
            'author': response['commit']['author']['name'],
            'message': response['commit']['message'],
            'date': format_date_to_int(response['commit']['author']['date'], GITHUB_TIME_FORMAT)
        }

    def get_contributors(self):
        """
        Gets information about all contributors to repository
        in dict format with response body

        :return: dict
        :raise NotImplementedError
        :Example:
        [
             {
                 "name": "contributor name",
                 "number_of_commits": "number of commits",
                 "email": "contributor email",
                 "url": "contributor url"
             },
             ...
        ]g
        """
        endpoint = self.repos_api_url + '/contributors'
        url = self.base_url + endpoint
        response = requests.get(url)
        if not response.status_code == 200:
            return None
        response = response.json()
        return list(map(lambda x: {
            'name': x['login'],
            'number_of_commits': x['contributions'],
            'email': x['login'],
            'url': x['url']}, response))
