"""
Contains RequestSenderGitLab class that provides realisation for sending API requests
to web-based hosting services for version control using Git
"""

from datetime import datetime
import requests
from request_sender_base import RequestSender


class RequestSenderGitLab(RequestSender):
    """
        GitLab class that provides realisation for sending API requests
        to web-based hosting services for version control using Git
    """

    def get_repo(self):
        """
        Takes repository name on GitLab and owner as parameters and
        returns repository info in JSON format
        example:
        {
            "id": "unique id",
            "repo_name": "repository name",
            "creation_date": "date",
            "owner": "repository owner",
            "url": "repository url"
        }

        :return: string - JSON formatted response
        """
        # get url of remote repository given as input
        url_repo = self.base_url + self.owner + "%2F" + self.repo

        # get JSON with repository info
        repo_info = requests.get(url_repo).json()

        # retrieve only info about repository
        repo = {"id": repo_info['id'],
                "repo_name": repo_info['name'],
                "creation_date": repo_info['created_at'],
                "owner": repo_info['path_with_namespace'].split('/')[0],
                "url": repo_info['web_url']}

        return repo

    def get_branches(self):
        """
        get branches of given repository on GitLab
        example:
        [
            {
                "name": "branch name"
            },
            ...
        ]

        :return: list of dicts
        """

        # get url of remote repository given as input
        url_branches = self.base_url + self.owner + "%2F" + self.repo + "/repository/branches"

        # get JSON about branches
        branches_info = requests.get(url_branches).json()

        # retrieve only info about name of the branches
        branches = [{"name": branch['name']} for branch in branches_info]

        return branches

    def get_commits(self):
        """
        Takes repository name and owner as parameters and
        returns information about commits in list of dictionaries
        example
        [
            {
                "hash": "commit hash",
                "author": "commit author",
                "message": "commit message",
                "date": "date when committed"

            },
            ...
        ]

        :return: string - list of dictionaries
        """
        # get url of remote repository given as input
        url_commits = self.base_url + self.owner + "%2F" + self.repo + "/repository/commits"

        # get JSON about commits
        commits_info = requests.get(url_commits).json()

        pat_time = "%Y-%m-%dT%H:%M:%S"

        # retrieve only info about commits
        commits = [{'hash': commit['id'],
                    'author': commit['committer_name'],
                    'message': commit['message'],
                    'date': int(datetime.strptime(commit['created_at'][:-5], pat_time).timestamp())}
                   for commit in commits_info]

        return commits
