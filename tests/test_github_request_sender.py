"""
Contains TestsRequestSenderGitHub class that provides methods for testing
of GitHubRequestSender class which sends API requests to GitHub
"""

from heat_map_training.request_sender.github_request_sender import GithubRequestSender


class TestsGithubRequestSender:
    """
    Provides pytests for testing RequestSenderBase methods realized by GithubRequestSender
    """

    def test_get_commits(self):
        """
        Unittest function for testing method get_commits in GithubRequestSender
        """
        assert GithubRequestSender('mixa1901', 'test').get_commits() == [
            {
                'hash': '5a8a11fa7b0fc08d59e0fd7c435c3073459ae87a',
                'author': 'mixa1901',
                'message': 'test2',
                'date': 1531637855
            },
            {
                'hash': 'e9298428816b7419afd11af2397f7f3745f727d9',
                'author': 'mixa1901',
                'message': 'first commit',
                'date': 1531637760
            }
        ]

        assert GithubRequestSender('unknown', 'unknown').get_commits() is None

    def test_get_commit_by_hash(self):
        """
        Unittest function for testing method get_commit_by_hash in GithubRequestSender
        """
        assert GithubRequestSender('mixa1901', 'test').get_commit_by_hash(
            '5a8a11fa7b0fc08d59e0fd7c435c3073459ae87a') == {
                   'hash': '5a8a11fa7b0fc08d59e0fd7c435c3073459ae87a',
                   'author': 'mixa1901',
                   'message': 'test2',
                   'date': 1531637855
               }

        assert GithubRequestSender('unknown', 'unknown').get_commit_by_hash('unknown') is None
