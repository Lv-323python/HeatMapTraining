import pytest
from unittest import mock
from heat_map_training.request_sender.bitbucket_request_sender import BitbucketRequestSender
from heat_map_training.utils.request_status_codes import STATUS_CODE_OK, STATUS_CODE_NOT_FOUND
from tests.bitbucket_mock_data import REPO_DATA, BRANCHES_DATA, COMMITS_DATA, \
    COMMIT_BY_AWESOME_BRANCH, COMMIT_BY_BEAUTIFUL_BRANCH, COMMIT_BY_MASTER, COMMIT_BY_HASH_35a363

REPO = "publicbitbucketrepo"
USER = "partsey"
BRANCH = "awesome-feature"
COMMIT_HASH = "35a363addc596e1f3a0580d3dec1b78689be991d"
FALSE_USER = "false_user"
FALSE_REPO = "false_repo"
FALSE_BRANCH = "false_branch"
FALSE_COMMIT_HASH = "0" * len(COMMIT_HASH)


def mocked_requests_get(*args):
    class MockResponse:
        def __init__(self, json_data, status_code):
            self.json_data = json_data
            self.status_code = status_code

        def json(self):
            return self.json_data

    if args[0] == 'https://api.bitbucket.org/2.0/repositories/partsey/publicbitbucketrepo/commits':
        return MockResponse(COMMITS_DATA, STATUS_CODE_OK)
    elif args[0] == 'https://api.bitbucket.org/2.0/repositories/partsey/publicbitbucketrepo':
        return MockResponse(REPO_DATA, STATUS_CODE_OK)
    elif args[0] == 'https://api.bitbucket.org/2.0/repositories/partsey/publicbitbucketrepo/refs/branches':
        return MockResponse(BRANCHES_DATA, STATUS_CODE_OK)
    elif args[0] == 'https://api.bitbucket.org/2.0/repositories/partsey/publicbitbucketrepo/commits/awesome-feature':
        return MockResponse(COMMIT_BY_AWESOME_BRANCH, STATUS_CODE_OK)
    elif args[0] == 'https://api.bitbucket.org/2.0/repositories/partsey/publicbitbucketrepo/commits/beautiful-feature':
        return MockResponse(COMMIT_BY_BEAUTIFUL_BRANCH, STATUS_CODE_OK)
    elif args[0] == 'https://api.bitbucket.org/2.0/repositories/partsey/publicbitbucketrepo/commits/master':
        return MockResponse(COMMIT_BY_MASTER, STATUS_CODE_OK)
    elif args[0] == 'https://api.bitbucket.org/2.0/repositories/partsey/publicbitbucketrepo/commit/35a363addc596e1f3a0580d3dec1b78689be991d':
        return MockResponse(COMMIT_BY_HASH_35a363, STATUS_CODE_OK)

    return MockResponse(None, STATUS_CODE_NOT_FOUND)


@pytest.fixture(scope='module')
def create_repo_data():
    return BitbucketRequestSender(USER, REPO)


@pytest.fixture(scope='module')
def create_non_existing_repo_data():
    return BitbucketRequestSender("__", "__")


@mock.patch('requests.get', side_effect=mocked_requests_get)
def test_get_repo_success(mocker):
    expected_result = {
        'id': 'bd061b16-a281-4368-bc45-c2f78f8eb63c',
        'repo_name': 'PublicBitbucketRepo',
        'creation_date': '1530188954',
        'owner': 'partsey',
        'url': 'https://api.bitbucket.org/2.0/repositories/partsey/publicbitbucketrepo'
    }
    assert create_repo_data().get_repo() == expected_result, "Received data does not match the expected result"


@mock.patch('heat_map_training.request_sender.bitbucket_request_sender.requests.get', side_effect=mocked_requests_get)
def test_get_repo_fail(mocker):
    assert create_non_existing_repo_data().get_repo() is None, "Bad data request"


@mock.patch('heat_map_training.request_sender.bitbucket_request_sender.requests.get', side_effect=mocked_requests_get)
def test_get_branches_success(mocker):
    expected_result = [{'name': 'awesome-feature'}, {'name': 'beautiful-feature'}, {'name': 'master'}]
    assert create_repo_data().get_branches() == expected_result, "Received data does not match the expected result"


@mock.patch('heat_map_training.request_sender.bitbucket_request_sender.requests.get', side_effect=mocked_requests_get)
def test_get_branches_fail(mocker):
    assert create_non_existing_repo_data().get_branches() is None, "Bad data request"


@mock.patch('heat_map_training.request_sender.bitbucket_request_sender.requests.get', side_effect=mocked_requests_get)
def test_get_commits_success(mocker):
    expected_result = [
        {
            "hash": "ad28081b8f17286689d1fef7efaad33dfcd6c4f3",
            "author": "fake_user",
            "message": "added file.txt\n",
            "date": "1532321287",
            "branches": [
                "beautiful-feature"
            ]
        },
        {
            "hash": "35a363addc596e1f3a0580d3dec1b78689be991d",
            "author": "partsey",
            "message": "Merge branch 'beautiful-feature'\n",
            "date": "1531728161",
            "branches": [
                "awesome-feature",
                "master"
            ]
        },
        {
            "hash": "8b4a937ad98639fa3231cfa4b29dd0e8b25a6dd6",
            "author": "partsey",
            "message": "created temp2.txt\n",
            "date": "1531728062",
            "branches": [
                "awesome-feature",
                "beautiful-feature",
                "master"
            ]
        },
        {
            "hash": "967449717d302d6f20d3c800f9964fc467aa8dc5",
            "author": "partsey",
            "message": "created temp1.txt\n",
            "date": "1531727950",
            "branches": [
                "awesome-feature",
                "master"
            ]
        },
        {
            "hash": "992572f32da2743ad8e86ad1cc7338284c3792c6",
            "author": "partsey",
            "message": "created temp.txt\n",
            "date": "1531727775",
            "branches": [
                "awesome-feature",
                "beautiful-feature",
                "master"
            ]
        },
        {
            "hash": "8333878971e78108e3a3fff76bd44ed308a5fada",
            "author": "partsey",
            "message": "initial commit + created  README.md\n",
            "date": "1530189123",
            "branches": [
                "awesome-feature",
                "beautiful-feature",
                "master"
            ]
        }
    ]
    assert create_repo_data().get_commits() == expected_result, "Received data does not match the expected result"


@mock.patch('heat_map_training.request_sender.bitbucket_request_sender.requests.get', side_effect=mocked_requests_get)
def test_get_commits_fail(mocker):
    assert create_non_existing_repo_data().get_commits() is None, "Bad data request"


@mock.patch('heat_map_training.request_sender.bitbucket_request_sender.requests.get', side_effect=mocked_requests_get)
def test_get_commit_by_hash_success(mocker):
    expected_result = {'branches': ['awesome-feature', 'master'],
                       'hash': '35a363addc596e1f3a0580d3dec1b78689be991d',
                       'author': 'partsey',
                       'message': "Merge branch 'beautiful-feature'\n",
                       'date': '1531728161'}
    assert create_repo_data().get_commit_by_hash("35a363addc596e1f3a0580d3dec1b78689be991d") \
           == expected_result, "Received data does not match the expected result"


@mock.patch('heat_map_training.request_sender.bitbucket_request_sender.requests.get', side_effect=mocked_requests_get)
def test_get_commits_by_hash_fail(mocker):
    assert create_non_existing_repo_data().get_commit_by_hash(
        "35a363addc596e1f3a0580d3dec1b78689be991d") is None, "Bad data request"


@mock.patch('heat_map_training.request_sender.bitbucket_request_sender.requests.get', side_effect=mocked_requests_get)
def test_get_commits_by_branch_success(mocker):
    expected_result = [{'hash': '35a363addc596e1f3a0580d3dec1b78689be991d', 'author': 'partsey',
                        'message': "Merge branch 'beautiful-feature'\n", 'date': '1531728161'},
                       {'hash': '8b4a937ad98639fa3231cfa4b29dd0e8b25a6dd6', 'author': 'partsey',
                        'message': 'created temp2.txt\n', 'date': '1531728062'},
                       {'hash': '967449717d302d6f20d3c800f9964fc467aa8dc5', 'author': 'partsey',
                        'message': 'created temp1.txt\n', 'date': '1531727950'},
                       {'hash': '992572f32da2743ad8e86ad1cc7338284c3792c6', 'author': 'partsey',
                        'message': 'created temp.txt\n', 'date': '1531727775'},
                       {'hash': '8333878971e78108e3a3fff76bd44ed308a5fada', 'author': 'partsey',
                        'message': 'initial commit + created  README.md\n', 'date': '1530189123'}]
    assert create_repo_data().get_commits_by_branch("awesome-feature") == expected_result, \
        "Received data does not match the expected result"


@mock.patch('heat_map_training.request_sender.bitbucket_request_sender.requests.get', side_effect=mocked_requests_get)
def test_get_commits_by_branch_fail(mocker):
    assert create_non_existing_repo_data().get_commits_by_branch("awesome-feature") is None, "Bad data request"


@mock.patch('heat_map_training.request_sender.bitbucket_request_sender.requests.get', side_effect=mocked_requests_get)
def test_get_contributors_success(mocker):
    expected_result = [{'name': 'fake_user', 'number_of_commits': 1, 'email': 'user@example.com', 'url': None},
                       {'name': 'partsey', 'number_of_commits': 4, 'email': 'partsey2412@gmail.com',
                        'url': 'https://bitbucket.org/partsey/'},
                       {'name': 'partsey', 'number_of_commits': 1, 'email': 'partsey2412@gmail.com',
                        'url': 'https://bitbucket.org/partsey/'}]
    assert create_repo_data().get_contributors() == expected_result, "Received data does not match the expected result"


@mock.patch('heat_map_training.request_sender.bitbucket_request_sender.requests.get', side_effect=mocked_requests_get)
def test_get_contributors_fail(mocker):
    assert create_non_existing_repo_data().get_contributors() is None, "Bad data request"
