"""
Contains TestsGithubRequestSender class that provides methods for testing
of GithubRequestSender class which sends API requests to Github
"""
from heat_map_training.request_sender.github_request_sender import GithubRequestSender


def test_get_repo():
    """
    Unittest function for testing method get_repo in GithubRequestSender
    """
    assert GithubRequestSender('BoartK', 'test1').get_repo() == {
        'id': 136896178,
        'repo_name': 'test1',
        'creation_date': 1528694578,
        'owner': 'BoartK',
        'url': 'https://api.github.com/repos/BoartK/test1'
    }

    assert GithubRequestSender('testerr', 'testerr').get_repo() is None


def test_get_contributors():
    """
    Unittest function for testing method get_contributors in GithubRequestSender
    """
    assert GithubRequestSender('BoartK', 'test1').get_contributors() == [
        {
            'name': 'BoartK',
            'number_of_commits': 2,
            'email': 'BoartK',
            'url': 'https://api.github.com/users/BoartK'
        }
    ]

    assert GithubRequestSender('testerr', 'testerr').get_contributors() is None

