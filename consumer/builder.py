from heat_map_training.request_sender.bitbucket_request_sender import BitbucketRequestSender
from heat_map_training.request_sender.github_request_sender import GithubRequestSender
from heat_map_training.request_sender.gitlab_request_sender import GitLabRequestSender
from heat_map_training.request_sender.gitlab_v3_request_sender_base import GitLabV3RequestSender

"""
This is a class builder that returns instance of provider depending on its git_client
"""


class Builder:
    def __init__(self, git_client, version, repo, owner, token=''):
        self.git_client = git_client
        self.version = version
        self.repo = repo
        self.owner = owner
        self.token = token

    def build_provider(self):
        """
        This method is responsible for building provider with given methods.
        Note that GitHub provider takes token as a positional parameter
        :return: instance of provider class
        """
        if self.git_client == 'bitbucket':
            return BitbucketRequestSender(self.repo, self.owner)
        elif self.git_client == 'gitlab':
            if self.version == '3':
                return GitLabV3RequestSender(self.repo, self.owner)
            else:
                return GitLabRequestSender(self.repo, self.owner)
        elif self.git_client == 'github':
            return GithubRequestSender(self.repo, self.owner, self.token)
