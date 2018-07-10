"""
Contains GithubRequestSender class that provides implementation of
interface for sending API requests
to web-based hosting services for version control using GitHub
"""
from datetime import datetime
import requests
from request_sender_base import RequestSender  # pylint: disable=import-error

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

        endpoint = '/repos/{owner}/{repo}'.format(owner=self.owner, repo=self.repo)
        response = requests.get(self.base_url + endpoint).json()
        creation_date = datetime.strptime(response['created_at'], GITHUB_TIME_FORMAT).timestamp()
        repo = {'id': response['id'],
                'repo_name': response['name'],
                'creation_date': creation_date,
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
        endpoint = '/repos/{owner}/{repo}/branches'.format(owner=self.owner, repo=self.repo)
        url = self.base_url + endpoint
        response = requests.get(url).json()
        branches = []
        for raw in response:
            if raw['name']:
                branches.append({'name': raw['name']})
        return branches

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
        endpoint = '/repos/{owner}/{repo}/commits'.format(owner=self.owner, repo=self.repo)
        response = list(requests.get(self.base_url + endpoint).json())
        commits = []
        for _, commit in enumerate(response):
            date = datetime.strptime(commit['commit']['author']['date'],
                                     GITHUB_TIME_FORMAT).timestamp()
            commits.append({'hash': commit['sha'],
                            'author': commit['commit']['author']['name'],
                            'message': commit['commit']['message'],
                            'date': date})

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
        endpoint = '/repos/{owner}/{repo}/commits?sha={branch}'.format(owner=self.owner,
                                                                       repo=self.repo,
                                                                       branch=branch_name)
        url = self.base_url + endpoint
        response = requests.get(url)
        commits = []
        if not response.status_code == 200:
            return commits
        response = response.json()
        for raw in response:
            date = datetime.strptime(raw['commit']['author']['date'],
                                     GITHUB_TIME_FORMAT).timestamp()
            one_commit = {
                'hash': raw['sha'],
                'author': raw['commit']['author']['name'],
                'message': raw['commit']['message'],
                'date': date}
            commits.append(one_commit)
        return commits

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
        endpoint = '/repos/{owner}/{repo}/commits'.format(owner=self.owner, repo=self.repo)
        response = list(requests.get(self.base_url + endpoint).json())
        for _, commit in enumerate(response):
            date = datetime.strptime(commit['commit']['author']['date'],
                                     GITHUB_TIME_FORMAT).timestamp()
            if hash_of_commit == commit['sha']:
                commit_by_hash = ({'hash': commit['sha'],
                                   'author': commit['commit']['author']['name'],
                                   'message': commit['commit']['message'],
                                   'date': date})

        return commit_by_hash

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
        ]
        """
        endpoint = '/repos/{owner}/{repo}/contributors'.format(owner=self.owner, repo=self.repo)
        url = self.base_url + endpoint
        response = requests.get(url).json()
        contributors = []

        for raw in response:
            contributor = {'name': raw['login'],
                           'number_of_commits': raw['contributions'],
                           'email': raw['login'],
                           'url': raw['url']}
            contributors.append(contributor)
        return contributors
