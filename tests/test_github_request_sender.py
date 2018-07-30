"""
Contains functions for testing
of GithubRequestSender class which sends API requests to Github
"""
from heat_map_training.request_sender.github_request_sender import GithubRequestSender
from unittest import mock


def mock_response(status_code=200, json_data="{test}"):
    """
    since we typically test a bunch of different
    requests calls for a service, we are going to do
    a lot of mock responses, so its usually a good idea
    to have a helper function that builds these things
    """

    mock_resp = mock.Mock()

    mock_resp.json = mock.Mock(return_value=json_data)
    mock_resp.status_code = status_code

    return mock_resp

a = mock_response()
print(a.json.__dict__)
print(a.status_code)



def test_get_repo_success():
    assert GithubRequestSender('BoartK', 'test1').get_repo() == {
        'id': 136896178,
        'repo_name': 'test1',
        'creation_date': 1528694578,
        'owner': 'BoartK',
        'url': 'https://api.github.com/repos/BoartK/test1'
    }


def test_get_repo_fail():
    assert GithubRequestSender('testerr', 'testerr').get_repo() is None


def test_get_contributors_success():
    assert GithubRequestSender('BoartK', 'test1').get_contributors() == [
        {
            'name': 'BoartK',
            'number_of_commits': 2,
            'email': 'BoartK',
            'url': 'https://api.github.com/users/BoartK'
        }
    ]


def test_get_contributors_fail():
    assert GithubRequestSender('testerr', 'testerr').get_contributors() is None


def test_get_commits_success():
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


def test_get_commits_fail():
    # check output if given wrong owner or repository
    assert GithubRequestSender('mixa1901', 'unknown').get_commits() is None


def test_get_commit_by_hash_success():
    # check output for correctness
    assert GithubRequestSender('mixa1901', 'test').get_commit_by_hash(
        '5a8a11fa7b0fc08d59e0fd7c435c3073459ae87a') == {
               'hash': '5a8a11fa7b0fc08d59e0fd7c435c3073459ae87a',
               'author': 'mixa1901',
               'message': 'test2',
               'date': 1531637855
           }


def test_get_commit_by_hash_wrong_attr_fail():
    # check output if given wrong owner or repository
    assert GithubRequestSender('mixa1901', 'unknown').get_commit_by_hash('unknown') is None


def test_get_commit_by_hash_wrong_hash_fail():
    # check output if given wrong hash
    assert GithubRequestSender('mixa1901', 'test').get_commit_by_hash('unknown') is None

@mock.patch('requests.get')
def test_get_branches_success(mocker):
    mocker
    assert GithubRequestSender('Freon404', 'test_rep').get_branches() == [
        {
            "name": "master",
        },
        {
            "name": "new_branch"
        }
    ]


def test_get_branches_fail():
    assert GithubRequestSender('Freon404', "don't exist").get_branches() is None


def test_get_commits_by_branch_success():
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


def test_get_commits_by_branch_fail():
    assert GithubRequestSender('Freon404', 'test_rep').get_commits_by_branch('fake') is None
