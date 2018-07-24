"""
Contains RequestSenderGitLab class that provides realisation for sending API requests
to web-based hosting services for version control using Git
"""

import requests
from heat_map_training.request_sender.request_sender_base import \
    RequestSender  # pylint: disable=import-error
from heat_map_training.utils.helper import format_date_to_int
from heat_map_training.utils.request_status_codes import STATUS_CODE_OK


class GitLabRequestSender(RequestSender):

    """
        GitLab class that provides realisation for sending API requests
        to web-based hosting services for version control using Git
    """

    def __init__(self, owner, repo, base_url="https://gitlab.com/api/v4/projects/"):
        RequestSender.__init__(
            self,
            base_url=base_url,
            owner=owner,
            repo=repo
        )

    def get_repo(self):
        # get url of remote repository given as input
        """
        Takes repository name on GitLab and owner as parameters and
        returns repository info in JSON format

        :return: dictionary.
        Example:
        {
            "id": "unique id",
            "repo_name": "repository name",
            "creation_date": "date",
            "owner": "repository owner",
            "url": "repository url"
        }
        """
        url_repo = self.base_url + self.owner + "%2F" + self.repo

        # get response and check it's validation
        response = requests.get(url_repo)

        if not response.status_code == STATUS_CODE_OK:
            return None

        # get json of repository
        repo_info = response.json()

        # retrieve only info about repository
        repo = {
            "id": repo_info["id"],
            "repo_name": repo_info["name"],
            "creation_date": format_date_to_int(repo_info["created_at"][:-5], "%Y-%m-%dT%H:%M:%S"),
            "owner": repo_info["path_with_namespace"].split("/")[0],
            "url": repo_info["web_url"]
        }

        return repo

    def get_branches(self):
        """
        get branches of given repository on GitLab

        :return: list of dictionaries.
        Example:
        [
            {
                "name": "branch name"
            },
            ...
        ]
        """

        # get url of remote repository given as input
        url_branches = self.base_url + self.owner + "%2F" + self.repo + "/repository/branches"

        # get response and check it's validation
        response = requests.get(url_branches)

        if not response.status_code == STATUS_CODE_OK:
            return None

        # get json of branches
        branches_info = response.json()

        # retrieve only info about name of the branches
        branches = [{"name": branch["name"]} for branch in branches_info]

        return branches

    def _get_branch_for_commit(self, commit_hash):
        """
        function that gets branch for particular commit
        :param commit_hash: string
        :return: string
        """
        api_gitlab = (self.base_url + self.owner + "%2F" + self.repo + "/repository/commits/" +
                      commit_hash + "/refs")

        branch_info = requests.get(api_gitlab).json()

        return branch_info[0]['name']

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
        url_commits = self.base_url + self.owner + "%2F" + self.repo + "/repository/commits"

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
            "date": format_date_to_int(commit["created_at"][:-5], "%Y-%m-%dT%H:%M:%S"),
            "branch": self._get_branch_for_commit(commit["id"])
        } for commit in commits_info]

        return commits

    def get_contributors(self):
        """
        Takes repository name and owner as parameters and returns
        information about contributors in JSON format

        :return: list of dictionaries.
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
        """
        # get url of remote repository given as input
        url_contributors = (self.base_url + self.owner + "%2F" + self.repo +
                            "/repository/contributors")

        # get response and check it's validation
        response = requests.get(url_contributors)

        if not response.status_code == STATUS_CODE_OK:
            return None

        # get json of contributors
        contributors_info = response.json()

        # retrieve only info about contributors
        contributors = [{
            "name": contributors_info[i]["name"],
            "number_of_commits": contributors_info[i]["commits"],
            "email": contributors_info[i]["email"],
            "url": "None"  # to be continued...
        } for i in range(len(contributors_info))]

        return contributors

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
                      "/repository/commits/" + hash_of_commit)

        response = requests.get(url_commit)

        if not response.status_code == STATUS_CODE_OK:
            return None

        # get JSON about one commit
        commit_info = requests.get(url_commit).json()

        commit = {
            "hash": commit_info["id"],
            "author": commit_info["author_name"],
            "message": commit_info["message"],
            "date": format_date_to_int(commit_info["committed_date"][:-5], "%Y-%m-%dT%H:%M:%S"),
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
                                 "/repository/commits?ref_name=" + branch_name)

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
            "date": format_date_to_int(commit["created_at"][:-5], "%Y-%m-%dT%H:%M:%S")
        } for commit in commits_json]

        return commits
