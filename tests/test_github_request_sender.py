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

    # check output for correctness
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

    # check output if given wrong owner or repository
    assert GithubRequestSender('mixa1901', 'unknown').get_commits() is None


def test_get_commit_by_hash():
    """
    Unittest function for testing method get_commit_by_hash in GithubRequestSender
    """

    # check output for correctness
    assert GithubRequestSender('mixa1901', 'test').get_commit_by_hash(
        '5a8a11fa7b0fc08d59e0fd7c435c3073459ae87a') == {
               'hash': '5a8a11fa7b0fc08d59e0fd7c435c3073459ae87a',
               'author': 'mixa1901',
               'message': 'test2',
               'date': 1531637855
           }

    # check output if given wrong owner or repository
    assert GithubRequestSender('mixa1901', 'unknown').get_commit_by_hash('unknown') is None

    # check output if given wrong hash
    assert GithubRequestSender('mixa1901', 'test').get_commit_by_hash('unknown') is None

def test_get_branches():
    """
    Unittest function for testing method get_branches in GithubRequestSender
    """
    assert GithubRequestSender('Freon404', 'test_rep').get_branches() == [
        {
            "name": "master",
        },
        {
            "name": "new_branch"
        }
    ]
    assert GithubRequestSender('Freon404', "don't exist").get_branches() is None


def test_get_commits_by_branch():
    """
    Unittest function for testing method get_commits_by_branch in GithubRequestSender
    """
    assert GithubRequestSender('Freon404', 'test_rep').get_commits_by_branch('master') == [
        {
            'hash': '159a52c9f395bf7f3b87c092585164976e9aeabc',
            'author': 'Yura_Vovk',
            'message': 'remove file.txt',
            'date': 1528650292
        },
        {
            'hash': '20428ee505b241e151563905420adf4145fe6734',
            'author': 'Yura_Vovk',
            'message': 'Last commit in test',
            'date': 1528646385
        },
        {
            'hash': '092174658c618bcf7fb035a508d7fd626ab232d2',
            'author': 'Yura_Vovk',
            'message': "Yeah, it's working",
            'date': 1528646269
        },
        {
            'hash': 'e547495cbba61b7f766330c04ece889f02cef437',
            'author': 'Yura_Vovk',
            'message': 'first commit',
            'date': 1528530717
        }]
    assert GithubRequestSender('Freon404', 'test_rep').get_commits_by_branch('fake') is None
