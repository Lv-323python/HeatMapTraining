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


def test_get_commits():
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

def test_get_commit_by_hash():
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
