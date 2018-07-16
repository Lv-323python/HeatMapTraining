"""
Contains functions for testing GitlabRequestSender class functionality
from gitlab_request_sender.py
"""

import pytest
from heat_map_training.request_sender.gitlab_request_sender import RequestSenderGitLab

GITLAB_API_BASE_URL = 'https://gitlab.com/api/v4/projects/' or 'https://gitlab.com/api/v4'
COMMIT_HASH = '130eabe9061c46b5ec90676735be9a8bfd1fa064'
BRANCH = 'master'
NON_EXISTING_BRANCH = '_'
NON_EXISTING_COMMIT_HASH = '0'*len(COMMIT_HASH)


@pytest.fixture(scope='module')
def real_repo():
    return RequestSenderGitLab('partsey', 'my-awesome-project',GITLAB_API_BASE_URL)


@pytest.fixture(scope='module')
def non_existing_repo():
    return RequestSenderGitLab(owner='_', repo='_', base_url=GITLAB_API_BASE_URL)


def test_get_repo_on_real_repo(real_repo):
    expected_repo = {
        'creation_date': 1530588761,
        'id': 7335647,
        'owner': 'partsey',
        'repo_name': 'my-awesome-project',
        'url': 'https://gitlab.com/partsey/my-awesome-project'
    }
    assert real_repo.get_repo() == expected_repo


def test_get_repo_on_non_existing_repo(non_existing_repo):
    assert non_existing_repo.get_repo() is None


def test_get_branches_on_real_repo(real_repo):
    expected_branches = [
        {
            'name': 'master'
        }
    ]
    assert real_repo.get_branches() == expected_branches


def test_get_branches_on_non_existing_repo(non_existing_repo):
    assert non_existing_repo.get_branches() is None


def test_get_commits_on_real_repo(real_repo):
    expected_commits = [
        {
            'author': 'Ruslan Partsey',
            'branch': 'master',
            'date': 1530589045,
            'hash': '130eabe9061c46b5ec90676735be9a8bfd1fa064',
            'message': 'add README.md\n'
        }
    ]
    assert real_repo.get_commits() == expected_commits


def test_get_commits_on_non_existing_repo(non_existing_repo):
    assert non_existing_repo.get_commits() is None


def test_get_commit_by_hash_on_real_repo(real_repo):
    expected_commit = {
        'author': 'Ruslan Partsey',
        'branch': 'master',
        'date': 1530589045,
        'hash': '130eabe9061c46b5ec90676735be9a8bfd1fa064',
        'message': 'add README.md\n'
    }
    assert real_repo.get_commit_by_hash(COMMIT_HASH) == expected_commit


def test_get_commit_by_hash_on_real_repo_with_non_existing_commit(real_repo):
    assert real_repo.get_commit_by_hash(NON_EXISTING_COMMIT_HASH) is None


def test_get_commit_by_hash_on_non_existing_repo(non_existing_repo):
    assert non_existing_repo.get_commit_by_hash(COMMIT_HASH) is None


def test_get_commits_by_branch_on_real_repo(real_repo):
    expected_commits_by_branch = [
        {
            'author': 'Ruslan Partsey',
            'date': 1530589045,
            'hash': '130eabe9061c46b5ec90676735be9a8bfd1fa064',
            'message': 'add README.md\n'
        }
    ]
    assert real_repo.get_commits_by_branch(BRANCH) == expected_commits_by_branch


def test_get_commits_by_branch_on_real_repo_with_non_existing_branch(real_repo):
    assert real_repo.get_commits_by_branch(NON_EXISTING_BRANCH) is None


def test_get_commits_by_branch_on_non_existing_repo(non_existing_repo):
    assert non_existing_repo.get_commits_by_branch(BRANCH) is None


def test_get_contributors_on_real_repo(real_repo):
    expected_contributors = [
        {
            'email': 'partsey2412@gmail.com',
            'name': 'Ruslan Partsey',
            'number_of_commits': 1,
            'url': 'https://gitlab.com/partsey'
        }
    ]
    assert real_repo.get_contributors() == expected_contributors


def test_get_contributors_on_non_existing_repo(non_existing_repo):
    assert non_existing_repo.get_contributors() is None
