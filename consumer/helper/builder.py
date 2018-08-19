"""
This module provides a builder that returns instance of provider class
"""
from heat_map.request_sender.bitbucket_request_sender \
    import BitbucketRequestSender, BitbucketServerRequestSender
from heat_map.request_sender.github_request_sender import GithubRequestSender
from heat_map.request_sender.gitlab_request_sender import GitLabRequestSender
from heat_map.request_sender.gitlab_v3_request_sender_base import GitLabV3RequestSender
from general_helper.logger.log_error_decorators import try_except_decor


class Builder:
    """
    This is a class builder that returns instance of provider depending on its git_client
    """

    @try_except_decor
    def __init__(self, request_dict):
        self.git_client = request_dict['git_client']
        self.version = request_dict['version']
        self.repo = request_dict['repo']
        self.owner = request_dict['owner']
        self.token = request_dict['token']
        self.provider = None

    @try_except_decor
    def __enter__(self):
        """
        This method is responsible for building provider with given methods.
        Note that GitHub provider takes token as a positional parameter
        :return: instance of provider class
        """
        if self.git_client == 'bitbucket':
            if self.version == '1':
                self.provider = BitbucketServerRequestSender(self.owner, self.repo)
            elif self.version == '2':
                self.provider = BitbucketRequestSender(self.owner, self.repo)
        elif self.git_client == 'gitlab':
            if self.version == '3':
                self.provider = GitLabV3RequestSender(self.owner, self.repo)
            self.provider = GitLabRequestSender(self.owner, self.repo)
        elif self.git_client == 'github':
            self.provider = GithubRequestSender(self.owner, self.repo, self.token)
        return self.provider

    @try_except_decor
    def __exit__(self, exc_type, exc_val, exc_tb):
        del self.provider
