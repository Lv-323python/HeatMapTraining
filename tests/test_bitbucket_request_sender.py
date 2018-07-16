from heat_map_training.request_sender.bitbucket_request_sender import BitbucketRequestSender

REPO = "publicbitbucketrepo"
USER = "partsey"
BRANCH = "awesome-feature"
COMMIT_HASH = "35a363addc596e1f3a0580d3dec1b78689be991d"
FALSE_USER = "false_user"
FALSE_REPO = "false_repo"
FALSE_BRANCH = "false_branch"
FALSE_COMMIT_HASH = "0" * len(COMMIT_HASH)


def create_repo_data():
    return BitbucketRequestSender(USER, REPO)


def create_non_existing_repo_data():
    return BitbucketRequestSender("false_user", "false_repo")


def test_get_repo_success():
    expected_result = {
        'id': '{bd061b16-a281-4368-bc45-c2f78f8eb63c}',
        'repo_name': 'PublicBitbucketRepo',
        'creation_date': '1530188954',
        'owner': 'partsey',
        'url': 'https://api.bitbucket.org/2.0/repositories/partsey/publicbitbucketrepo'
    }

    assert create_repo_data().get_repo() == expected_result, "Received data does not match the expected result"


def test_get_repo_fail():
    assert create_non_existing_repo_data().get_repo() is None, "Bad data request"


def test_get_branches_success():
    expected_result = [
        {'name': 'awesome-feature'},
        {'name': 'beautiful-feature'},
        {'name': 'master'}
    ]
    assert create_repo_data().get_branches() == expected_result, "Received data does not match the expected result"


def test_get_branches_fail():
    assert create_non_existing_repo_data().get_branches() is None, "Bad data request"


def test_get_commits_success():
    expected_result = [
        {
            'hash': '35a363addc596e1f3a0580d3dec1b78689be991d',
            'author': 'partsey',
            'message': "Merge branch 'beautiful-feature'\n",
            'date': '1531728161'},
        {
            'hash': '8b4a937ad98639fa3231cfa4b29dd0e8b25a6dd6',
            'author': 'partsey',
            'message': 'created temp2.txt\n',
            'date': '1531728062'
        },
        {
            'hash': '967449717d302d6f20d3c800f9964fc467aa8dc5',
            'author': 'partsey',
            'message': 'created temp1.txt\n',
            'date': '1531727950'
        },
        {
            'hash': '992572f32da2743ad8e86ad1cc7338284c3792c6',
            'author': 'partsey',
            'message': 'created temp.txt\n',
            'date': '1531727775'},
        {
            'hash': '8333878971e78108e3a3fff76bd44ed308a5fada',
            'author': 'partsey',
            'message': 'initial commit + created  README.md\n',
            'date': '1530189123'}]

    assert create_repo_data().get_commits() == expected_result, "Received data does not match the expected result"


def test_get_commits_fail():
    assert create_non_existing_repo_data().get_commits() is None, "Bad data request"
