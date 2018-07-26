"""
Contains GitLabV3RequestSender class that provides realisation for sending API requests
to web-based hosting services for version control using Git
"""

import requests
from heat_map_training.request_sender.gitlab_request_sender import \
    GitLabRequestSender  # pylint: disable=import-error
from heat_map_training.utils.helper import format_date_to_int
from heat_map_training.utils.request_status_codes import STATUS_CODE_OK

TOKEN = "?private_token="


class GitLabV3RequestSender(GitLabRequestSender):
    """
        GitLab class that provides realisation for sending API requests
        to web-based hosting services for version control using Git on version 3 API
    """

    def __init__(self, owner, repo, base_url="http://boart-lenovo-ideapad-y510p/api/v3/projects/"):
        GitLabRequestSender.__init__(
            self,
            base_url=base_url,
            owner=owner,
            repo=repo)
        self.token = TOKEN

    def _get_branch_for_commit(self, commit_hash):
        api_gitlab = (self.base_url + self.owner + "%2F" + self.repo + "/repository/commits/" +
                      commit_hash + "/statuses" + self.token)
        branch_info = requests.get(api_gitlab).json()
        try:
            return branch_info[0]['ref']
        except IndexError:
            return None

    def get_commits(self):
        """
        Takes repository name and owner as parameters and
        returns information about commits in list of dictionaries

        :return: list of dictionaries.
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
        """
        # get url of remote repository given as input
        url_commits = (self.base_url + self.owner + "%2F" + self.repo + "/repository/commits" +
                       self.token)

        response = requests.get(url_commits)

        if not response.status_code == STATUS_CODE_OK:
            return None

        # get JSON about commits
        commits_info = requests.get(url_commits).json()

        # retrieve only info about commits
        commits = [{
            "hash": commit["id"],
            "author": commit["committer_name"],
            "message": commit["message"],
            "date": format_date_to_int(commit["created_at"][:26] + commit["created_at"][27:29],
                                       "%Y-%m-%dT%H:%M:%S.%f%z"),
            "branch": self._get_branch_for_commit(commit["id"])
        } for commit in commits_info]

        return commits

    def get_commit_by_hash(self, hash_of_commit):
        """
        Takes hash of the commit and returns info about it in JSON format

        :param hash_of_commit: string
        :return: dictionary.
        Example:
        {
            "hash": "commit hash",
            "author": "commit author",
            "message": "commit message",
            "date": "date when committed"

        }
        """
        # get url of remote repository given as input
        url_commit = (self.base_url + self.owner + "%2F" + self.repo +
                      "/repository/commits/" + hash_of_commit + self.token)

        response = requests.get(url_commit)

        if not response.status_code == STATUS_CODE_OK:
            return None

        # get JSON about one commit
        commit_info = requests.get(url_commit).json()

        commit = {
            "hash": commit_info["id"],
            "author": commit_info["author_name"],
            "message": commit_info["message"],
            "date": format_date_to_int(commit_info["created_at"][:26] +
                                       commit_info["created_at"][27:29],
                                       "%Y-%m-%dT%H:%M:%S.%f%z"),
            "branch": self._get_branch_for_commit(hash_of_commit)
        }
        # retrieve only info about one commit

        return commit

    def get_commits_by_branch(self, branch_name):
        """
        Takes repository branches as parameters and
        returns information about last 20 commits per branch
        in dictionary

        :return: list of dictionaries.
        Example:
            [{

                "hash": "commit hash",
                "author": "commit author",
                "message": "commit message",
                "date": "date when committed"

             },
            ...]
        """

        api_commits_by_branch = (self.base_url + self.owner + "%2F" + self.repo +
                                 "/repository/commits" + self.token +
                                 "&" + "ref_name=" + branch_name)

        # get response and check it's validation
        response = requests.get(api_commits_by_branch)

        if not response.status_code == STATUS_CODE_OK:
            return None

        # get json of commits
        commits_json = response.json()

        if not commits_json:
            return None

        # make a list of dicts concerning commits per branch
        commits = [{
            "hash": commit["id"],
            "author": commit["committer_name"],
            "message": commit["message"],
            "date": format_date_to_int(commit["created_at"][:26] + commit["created_at"][27:29],
                                       "%Y-%m-%dT%H:%M:%S.%f%z")
        } for commit in commits_json]

        return commits
