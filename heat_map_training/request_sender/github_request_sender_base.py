"""
Contains GithubRequestSenderBase class that provides interface for sending API requests
to web-based hosting services for version control.
"""
import requests

from heat_map_training.request_sender.request_sender_base \
    import RequestSender
from heat_map_training.utils.request_status_codes import STATUS_CODE_OK


class GithubRequestSenderBase(RequestSender):
    """
    Github interface which is a platform for sending API requests
    to web-based hosting services for version control.
    Supports both RestAPI and GraphQl.
    """

    def __init__(self, base_url, owner, repo, query, token=''):
        super().__init__(base_url, owner, repo)
        self.query = query
        self.token = token
        self.headers = {
            'Authorization': 'token {token}'.format(token=token),
        }

    def _request(self, param):
        # if self.query is True, param will be a query to post
        # else - param will be an endpoint to form a url
        if self.query:
            query_body = {'query': param}
            response = requests.post(url=self.base_url,
                                     json=query_body,
                                     headers=self.headers)
        else:
            url = self.base_url + param
            response = requests.get(url=url,
                                    headers=self.headers)
        if response.status_code != STATUS_CODE_OK:
            return None
        return response.json()

    def get_repo(self):
        """
        Gets repository in dict format

        :return: dict
        """
        pass

    def get_branches(self):
        """
        Gets list of branches in a repository

        :return: list of dicts
        """
        pass

    def get_commits(self):
        """
        Gets all commits in repository in dict

        :return: list of dicts
        """
        pass

    def get_commits_by_branch(self, branch_name):
        """
        Gets commits of a specific branch in dict format

        :param branch_name: string
        :return: list of dicts
        """

        pass

    def get_commit_by_hash(self, hash_of_commit):
        """
        Gets the commit by hash in dict format with response body

        :param hash_of_commit: string
        :return: dict
        """

        pass

    def get_contributors(self):
        """
        Gets all contributors to repository in dict format with response body

        :return: list of dicts
        """
        pass
