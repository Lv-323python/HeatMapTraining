"""
Contains GitLabV3RequestSender class that provides realisation for sending API requests
to web-based hosting services for version control using Git
"""

import requests
from heat_map.request_sender.gitlab_request_sender import \
    GitLabRequestSender  # pylint: disable=import-error
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
