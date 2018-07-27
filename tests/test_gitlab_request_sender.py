"""
Contains functions for testing GitlabRequestSender class functionality
from gitlab_request_sender.py
"""

import pytest
from pytest_mock import mocker
from heat_map_training.request_sender.gitlab_request_sender import RequestSenderGitLab
from heat_map_training.utils.request_status_codes import STATUS_CODE_OK, STATUS_CODE_NOT_FOUND

# base API url
GITLAB_API_BASE_URL = 'https://gitlab.com/api/v4/projects/' or 'https://gitlab.com/api/v4'

# constant variables used in tests
COMMIT_HASH = '130eabe9061c46b5ec90676735be9a8bfd1fa064'
BRANCH = 'feature-awesome'
NON_EXISTING_BRANCH = '_'
NON_EXISTING_COMMIT_HASH = '0' * len(COMMIT_HASH)

# endpoint urls
REPO_URL = 'https://gitlab.com/api/v4/projects/partsey%2Fmy-awesome-project'
BRANCHES_URL = 'https://gitlab.com/api/v4/projects/partsey%2Fmy-awesome-project/repository/branches'
COMMITS_URL = 'https://gitlab.com/api/v4/projects/partsey%2Fmy-awesome-project/repository/commits'
COMMITS_BY_HASH_URL = 'https://gitlab.com/api/v4/projects/partsey%2Fmy-awesome-project/repository/commits/130eabe9061c46b5ec90676735be9a8bfd1fa064'
COMMITS_BY_BRANCH_URL = 'https://gitlab.com/api/v4/projects/partsey%2Fmy-awesome-project/repository/commits?ref_name=feature-awesome'
CONTRIBUTORS_URL = 'https://gitlab.com/api/v4/projects/partsey%2Fmy-awesome-project/repository/contributors'

# raw request responses
GET_REPO_ON_REAL_REPO_RESPONSE_DICT = {
    'avatar_url': None,
    'created_at': '2018-07-03T06:32:41.364Z',
    'default_branch': 'master',
    'description': 'my first project',
    'forks_count': 0,
    'http_url_to_repo': 'https://gitlab.com/partsey/my-awesome-project.git',
    'id': 7335647,
    'last_activity_at': '2018-07-17T14:23:04.337Z',
    'name': 'my-awesome-project',
    'name_with_namespace': 'Ruslan Partsey / my-awesome-project',
    'path': 'my-awesome-project',
    'path_with_namespace': 'partsey/my-awesome-project',
    'readme_url': 'https://gitlab.com/partsey/my-awesome-project/blob/master/README.md',
    'ssh_url_to_repo': 'git@gitlab.com:partsey/my-awesome-project.git',
    'star_count': 0,
    'tag_list': [],
    'web_url': 'https://gitlab.com/partsey/my-awesome-project'
}
GET_BRANCHES_ON_REAL_REPO_RESPONSE_LIST = [
    {
        'can_push': False,
        'commit': {'author_email': 'user@example.com',
                   'author_name': 'fake_user',
                   'authored_date': '2018-07-23T07:05:05.000+00:00',
                   'committed_date': '2018-07-23T07:05:05.000+00:00',
                   'committer_email': 'user@example.com',
                   'committer_name': 'fake_user',
                   'created_at': '2018-07-23T07:05:05.000+00:00',
                   'id': '85b5fddfa49036a0520d6791ef87121af2c11696',
                   'message': 'addded temp_file.txt',
                   'parent_ids': None,
                   'short_id': '85b5fddf',
                   'title': 'addded temp_file.txt'},
        'developers_can_merge': False,
        'developers_can_push': False,
        'merged': False,
        'name': 'feature-awesome',
        'protected': False
    },
    {
        'can_push': False,
        'commit': {'author_email': 'partsey2412@gmail.com',
                   'author_name': 'Ruslan Partsey',
                   'authored_date': '2018-07-03T06:37:25.000+00:00',
                   'committed_date': '2018-07-03T06:37:25.000+00:00',
                   'committer_email': 'partsey2412@gmail.com',
                   'committer_name': 'Ruslan Partsey',
                   'created_at': '2018-07-03T06:37:25.000+00:00',
                   'id': '130eabe9061c46b5ec90676735be9a8bfd1fa064',
                   'message': 'add README.md',
                   'parent_ids': None,
                   'short_id': '130eabe9',
                   'title': 'add README.md'},
        'developers_can_merge': False,
        'developers_can_push': False,
        'merged': False,
        'name': 'master',
        'protected': False
    }
]
GET_COMMITS_ON_REAL_REPO_RESPONSE_LIST = [
    {
        'author_email': 'user@example.com',
        'author_name': 'fake_user',
        'authored_date': '2018-07-23T07:05:05.000Z',
        'committed_date': '2018-07-23T07:05:05.000Z',
        'committer_email': 'user@example.com',
        'committer_name': 'fake_user',
        'created_at': '2018-07-23T07:05:05.000Z',
        'id': '85b5fddfa49036a0520d6791ef87121af2c11696',
        'message': 'addded temp_file.txt\n',
        'parent_ids': ['a01ed2932871a4bcbd7b3d872809e3651c5546f4'],
        'short_id': '85b5fddf',
        'title': 'addded temp_file.txt'
    },
    {
        'author_email': 'user@example.com',
        'author_name': 'fake_user',
        'authored_date': '2018-07-23T07:03:52.000Z',
        'committed_date': '2018-07-23T07:03:52.000Z',
        'committer_email': 'user@example.com',
        'committer_name': 'fake_user',
        'created_at': '2018-07-23T07:03:52.000Z',
        'id': '87b41aee43f607d0622f58e74409849ebe800b77',
        'message': 'added paragraph\n',
        'parent_ids': ['a01ed2932871a4bcbd7b3d872809e3651c5546f4'],
        'short_id': '87b41aee',
        'title': 'added paragraph'
    },
    {
        'author_email': 'user@example.com',
        'author_name': 'fake_user',
        'authored_date': '2018-07-23T07:01:49.000Z',
        'committed_date': '2018-07-23T07:01:49.000Z',
        'committer_email': 'user@example.com',
        'committer_name': 'fake_user',
        'created_at': '2018-07-23T07:01:49.000Z',
        'id': 'a01ed2932871a4bcbd7b3d872809e3651c5546f4',
        'message': 'created text_file.txt\n',
        'parent_ids': ['130eabe9061c46b5ec90676735be9a8bfd1fa064'],
        'short_id': 'a01ed293',
        'title': 'created text_file.txt'
    },
    {
        'author_email': 'partsey2412@gmail.com',
        'author_name': 'Ruslan Partsey',
        'authored_date': '2018-07-03T06:37:25.000Z',
        'committed_date': '2018-07-03T06:37:25.000Z',
        'committer_email': 'partsey2412@gmail.com',
        'committer_name': 'Ruslan Partsey',
        'created_at': '2018-07-03T06:37:25.000Z',
        'id': '130eabe9061c46b5ec90676735be9a8bfd1fa064',
        'message': 'add README.md\n',
        'parent_ids': [],
        'short_id': '130eabe9',
        'title': 'add README.md'
    }
]
GET_COMMIT_BY_HASH_ON_REAL_REPO_RESPONSE_DICT = {
    'author_email': 'partsey2412@gmail.com',
    'author_name': 'Ruslan Partsey',
    'authored_date': '2018-07-03T06:37:25.000Z',
    'committed_date': '2018-07-03T06:37:25.000Z',
    'committer_email': 'partsey2412@gmail.com',
    'committer_name': 'Ruslan Partsey',
    'created_at': '2018-07-03T06:37:25.000Z',
    'id': '130eabe9061c46b5ec90676735be9a8bfd1fa064',
    'last_pipeline': None,
    'message': 'add README.md\n',
    'parent_ids': [],
    'project_id': 7335647,
    'short_id': '130eabe9',
    'stats': {'additions': 0, 'deletions': 0, 'total': 0},
    'status': None,
    'title': 'add README.md'}
GET_COMMITS_BY_BRANCH_ON_REAL_REPO_RESPONSE_LIST = [
    {
        'author_email': 'user@example.com',
        'author_name': 'fake_user',
        'authored_date': '2018-07-23T07:05:05.000Z',
        'committed_date': '2018-07-23T07:05:05.000Z',
        'committer_email': 'user@example.com',
        'committer_name': 'fake_user',
        'created_at': '2018-07-23T07:05:05.000Z',
        'id': '85b5fddfa49036a0520d6791ef87121af2c11696',
        'message': 'addded temp_file.txt\n',
        'parent_ids': ['a01ed2932871a4bcbd7b3d872809e3651c5546f4'],
        'short_id': '85b5fddf',
        'title': 'addded temp_file.txt'
    },
    {
        'author_email': 'user@example.com',
        'author_name': 'fake_user',
        'authored_date': '2018-07-23T07:01:49.000Z',
        'committed_date': '2018-07-23T07:01:49.000Z',
        'committer_email': 'user@example.com',
        'committer_name': 'fake_user',
        'created_at': '2018-07-23T07:01:49.000Z',
        'id': 'a01ed2932871a4bcbd7b3d872809e3651c5546f4',
        'message': 'created text_file.txt\n',
        'parent_ids': ['130eabe9061c46b5ec90676735be9a8bfd1fa064'],
        'short_id': 'a01ed293',
        'title': 'created text_file.txt'
    },
    {
        'author_email': 'partsey2412@gmail.com',
        'author_name': 'Ruslan Partsey',
        'authored_date': '2018-07-03T06:37:25.000Z',
        'committed_date': '2018-07-03T06:37:25.000Z',
        'committer_email': 'partsey2412@gmail.com',
        'committer_name': 'Ruslan Partsey',
        'created_at': '2018-07-03T06:37:25.000Z',
        'id': '130eabe9061c46b5ec90676735be9a8bfd1fa064',
        'message': 'add README.md\n',
        'parent_ids': [],
        'short_id': '130eabe9',
        'title': 'add README.md'
    }
]
GET_CONTRIBUTORS_ON_REAL_REPO_RESPONSE_LIST = [
    {
        'additions': 0,
        'commits': 1,
        'deletions': 0,
        'email': 'partsey2412@gmail.com',
        'name': 'Ruslan Partsey'
    },
    {
        'additions': 0,
        'commits': 2,
        'deletions': 0,
        'email': 'user@example.com',
        'name': 'fake_user'
    }
]


def _patch_requests(mocker, status_code, response=None):
    """
    Patches requests module as well as requests.get function and its response

    :param mocker: mocker object - defined in pytest_mock module
    :param status_code: int - response status code
    :param response: dict or list
    :return: mock requests module
    """
    mock_requests = mocker.patch('heat_map_training.request_sender.gitlab_request_sender.requests')
    if status_code != STATUS_CODE_OK:
        mock_requests.get.return_value = mocker.Mock(status_code=status_code)
    else:
        mock_requests.get.return_value = mocker.Mock(
            status_code=status_code,
            json=mocker.Mock(return_value=response)
        )
    return mock_requests


@pytest.fixture(scope='module')
def real_repo():
    """
    Returns RequestSenderGitLab instance that in mapped to real repository in Bitbucket Cloud

    :return: RequestSenderGitLab instance
    """
    return RequestSenderGitLab('partsey', 'my-awesome-project', GITLAB_API_BASE_URL)


@pytest.fixture(scope='module')
def non_existing_repo():
    """
    Returns RequestSenderGitLab instance that in mapped to non existing repository in Bitbucket Cloud

    :return: RequestSenderGitLab instance
    """
    return RequestSenderGitLab(owner='_', repo='_', base_url=GITLAB_API_BASE_URL)


@pytest.mark.refactored
def test_get_repo_on_real_repo(real_repo, mocker):
    mock_requests = _patch_requests(mocker, STATUS_CODE_OK, GET_REPO_ON_REAL_REPO_RESPONSE_DICT)
    expected_repo = {
        'creation_date': 1530588761,
        'id': 7335647,
        'owner': 'partsey',
        'repo_name': 'my-awesome-project',
        'url': 'https://gitlab.com/partsey/my-awesome-project'
    }
    assert real_repo.get_repo() == expected_repo
    mock_requests.get.assert_called_with(REPO_URL)


@pytest.mark.refactored
def test_get_repo_on_non_existing_repo(non_existing_repo, mocker):
    _patch_requests(mocker, STATUS_CODE_NOT_FOUND)
    assert non_existing_repo.get_repo() is None
    # mock_requests.get.assert_called_with('https://gitlab.com/api/v4/projects/_%2F_')


@pytest.mark.refactored
def test_get_branches_on_real_repo(real_repo, mocker):
    mock_requests = _patch_requests(mocker, STATUS_CODE_OK, GET_BRANCHES_ON_REAL_REPO_RESPONSE_LIST)
    expected_branches = [
        {
            'name': 'feature-awesome'
        },
        {
            'name': 'master'
        }
    ]
    assert real_repo.get_branches() == expected_branches
    mock_requests.get.assert_called_with(BRANCHES_URL)


@pytest.mark.refactored
def test_get_branches_on_non_existing_repo(non_existing_repo, mocker):
    _patch_requests(mocker, STATUS_CODE_NOT_FOUND)
    assert non_existing_repo.get_branches() is None
    # mock_requests.get.assert_called_with('https://gitlab.com/api/v4/projects/_%2F_/repository/branches')


@pytest.mark.refactored
def test_get_commits_on_real_repo(real_repo, mocker):
    mock_requests = _patch_requests(mocker, STATUS_CODE_OK, GET_COMMITS_ON_REAL_REPO_RESPONSE_LIST)
    expected_commits = [
        {
            'author': 'fake_user',
            'date': 1532318705,
            'hash': '85b5fddfa49036a0520d6791ef87121af2c11696',
            'message': 'addded temp_file.txt\n',
            'branches': ['feature-awesome']
        },
        {
            'author': 'fake_user',
            'date': 1532318632,
            'hash': '87b41aee43f607d0622f58e74409849ebe800b77',
            'message': 'added paragraph\n',
            'branches': ['master']
        },
        {
            'author': 'fake_user',
            'date': 1532318509,
            'hash': 'a01ed2932871a4bcbd7b3d872809e3651c5546f4',
            'message': 'created text_file.txt\n',
            'branches': ['master', 'feature-awesome']
        },
        {
            'author': 'Ruslan Partsey',
            'date': 1530589045,
            'hash': '130eabe9061c46b5ec90676735be9a8bfd1fa064',
            'message': 'add README.md\n',
            'branches': ['master', 'feature-awesome']
        }
    ]
    assert real_repo.get_commits() == expected_commits
    mock_requests.get.assert_called_with(COMMITS_URL)


@pytest.mark.refactored
def test_get_commits_on_non_existing_repo(non_existing_repo, mocker):
    _patch_requests(mocker, STATUS_CODE_NOT_FOUND)
    assert non_existing_repo.get_commits() is None


@pytest.mark.refactored
def test_get_commit_by_hash_on_real_repo(real_repo, mocker):
    mock_requests = _patch_requests(mocker, STATUS_CODE_OK, GET_COMMIT_BY_HASH_ON_REAL_REPO_RESPONSE_DICT)
    expected_commit = {
        'author': 'Ruslan Partsey',
        'date': 1530589045,
        'hash': '130eabe9061c46b5ec90676735be9a8bfd1fa064',
        'message': 'add README.md\n',
        'branches': ['master', 'feature-awesome']

    }
    assert real_repo.get_commit_by_hash(COMMIT_HASH) == expected_commit
    mock_requests.get.assert_called_with(COMMITS_BY_HASH_URL)


@pytest.mark.refactored
def test_get_commit_by_hash_on_real_repo_with_non_existing_commit(real_repo, mocker):
    _patch_requests(mocker, STATUS_CODE_NOT_FOUND)
    assert real_repo.get_commit_by_hash(NON_EXISTING_COMMIT_HASH) is None


@pytest.mark.refactored
def test_get_commit_by_hash_on_non_existing_repo(non_existing_repo, mocker):
    _patch_requests(mocker, STATUS_CODE_NOT_FOUND)
    assert non_existing_repo.get_commit_by_hash(COMMIT_HASH) is None


@pytest.mark.refactored
def test_get_commits_by_branch_on_real_repo(real_repo, mocker):
    mock_requests = _patch_requests(mocker, STATUS_CODE_OK, GET_COMMITS_BY_BRANCH_ON_REAL_REPO_RESPONSE_LIST)
    expected_commits_by_branch = [
        {
            'author': 'fake_user',
            'date': 1532318705,
            'hash': '85b5fddfa49036a0520d6791ef87121af2c11696',
            'message': 'addded temp_file.txt\n'
        },
        {
            'author': 'fake_user',
            'date': 1532318509,
            'hash': 'a01ed2932871a4bcbd7b3d872809e3651c5546f4',
            'message': 'created text_file.txt\n'
        },
        {
            'author': 'Ruslan Partsey',
            'date': 1530589045,
            'hash': '130eabe9061c46b5ec90676735be9a8bfd1fa064',
            'message': 'add README.md\n'
        }
    ]
    assert real_repo.get_commits_by_branch(BRANCH) == expected_commits_by_branch
    mock_requests.get.assert_called_with(COMMITS_BY_BRANCH_URL)


@pytest.mark.refactored
def test_get_commits_by_branch_on_real_repo_with_non_existing_branch(real_repo, mocker):
    _patch_requests(mocker, STATUS_CODE_NOT_FOUND)
    assert real_repo.get_commits_by_branch(NON_EXISTING_BRANCH) is None


@pytest.mark.refactored
def test_get_commits_by_branch_on_non_existing_repo(non_existing_repo, mocker):
    _patch_requests(mocker, STATUS_CODE_NOT_FOUND)
    assert non_existing_repo.get_commits_by_branch(BRANCH) is None


@pytest.mark.refactored
def test_get_contributors_on_real_repo(real_repo, mocker):
    mock_requests = _patch_requests(mocker, STATUS_CODE_OK, GET_CONTRIBUTORS_ON_REAL_REPO_RESPONSE_LIST)
    expected_contributors = [
        {
            'email': 'partsey2412@gmail.com',
            'name': 'Ruslan Partsey',
            'number_of_commits': 1,
            'url': 'https://gitlab.com/partsey'
        },
        {
            'email': 'user@example.com',
            'name': 'fake_user',
            'number_of_commits': 3,
            'url': None
        }
    ]
    assert real_repo.get_contributors() == expected_contributors
    mock_requests.get.assert_called_with(CONTRIBUTORS_URL)


@pytest.mark.refactored
def test_get_contributors_on_non_existing_repo(non_existing_repo, mocker):
    _patch_requests(mocker, STATUS_CODE_NOT_FOUND)
    assert non_existing_repo.get_contributors() is None
