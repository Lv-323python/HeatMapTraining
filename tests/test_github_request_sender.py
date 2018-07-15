"""
Contains TestsRequestSenderGitHub class that provides methods for testing
of GitHubRequestSender class which sends API requests to GitHub
"""

from heat_map_training.request_sender import github_request_sender


a = github_request_sender.GithubRequestSender('Lv-323python', 'HeatMapTraining')
print(a.get_contributors())

class TestsRequestSenderGitHub:
    """
    Provides pytests for testing RequestSenderBase methods realized by BitbucketRequestSender
    """
    def test_function(self):
        """

        :return:
        """
        pass

    def test_function_2(self):
        """

        :return:
        """
        pass
