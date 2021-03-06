"""
Contains BitbucketRequestSender class that provides methods for sending API requests
to web-based hosting service Bitbucket for version control using Git and
BitbucketServerRequestSender class hat provides the same methods for sending API requests
to Bitbucket Server.
"""

import time
import requests
from requests.exceptions import RequestException

from heat_map.request_sender.request_sender_base import RequestSender
from heat_map.utils.bitbucket_helper import to_timestamp, get_gitname, get_email
from heat_map.utils.request_status_codes import STATUS_CODE_OK

from general_helper.logger.log_error_decorators import try_except_decor
from general_helper.logger.log_config import LOG


class BitbucketRequestSenderExc(Exception):
    """
        Exception class for BitbucketRequestSender
    """
    pass


class BitbucketServerRequestSenderExc(Exception):
    """
        Exception class for BitbucketServerRequestSender
    """
    pass


class BitbucketRequestSender(RequestSender):
    """
    Provides methods for sending API requests to web-based hosting service Bitbucket
    for version control using Git
    """

    @try_except_decor
    def __init__(self, owner, repo, base_url='https://api.bitbucket.org/2.0'):
        super().__init__(base_url=base_url, owner=owner, repo=repo)

    @try_except_decor
    def _get_request(self, endpoint, params=None, **kwargs):
        """
        Sends GET request to URL
        :param endpoint: string - endpoint url
        :param params: dict - of request parameters
        :param kwargs: - other optional parameters
        :return: json - response object
        """

        retries = 30
        while True:
            try:
                LOG.debug('Try to connect to BitBucket Cloud!')
                response = requests.get(self.base_url + endpoint, params, **kwargs)
                LOG.debug('Successfully connected BitBucket Cloud!')
                return response

            except RequestException as exc:
                if retries == 0:
                    LOG.error('Failed to connect to BitBucket Cloud...', exc_info=exc)
                    raise RequestException
                retries -= 1
                time.sleep(1)

    @try_except_decor
    def _get_page_of_commits_by_branch(self, branch_name='master', page=1):
        """
            Gets deserialize list of not parsed commits by page and branch name.

        :param branch_name: str
        :param page: int - page number
        :return: list - list of not parsed commits
        """

        assert isinstance(branch_name, str), 'Inputted "branch_name" type is not str'
        assert isinstance(page, int), 'Inputted "page" type is not int'
        branch_commits_endpoint = \
            f'/repositories/{self.owner}/{self.repo}/commits/{branch_name}'

        filter_param = \
            {'fields': 'values.hash,values.author,values.message,values.date,next',
             'page': page}

        response = self._get_request(branch_commits_endpoint, filter_param)

        # guard condition
        if response.status_code != STATUS_CODE_OK:
            assert False, \
                f'Invalid parameter(s) in: owner: {self.owner},' \
                f' repo: {self.repo}, branch name: {branch_name}, page: {page}'

        # deserialize commit
        commits_page = response.json()

        return commits_page

    @try_except_decor
    def get_repo(self):
        """
        Gets information about repository
        in dict format with response body and status code

        :return: dict
        :Example:
        {
            "id": "unique id",
            "repo_name": "repository name",
            "creation_date": "date",
            "owner": "repository owner",
            "url": "repository url"
        }
        """

        # gets information about repository
        repo_endpoint = f'/repositories/{self.owner}/{self.repo}'
        filter_param = {'fields': 'name,uuid,created_on,owner.username,links.self.href'}
        response = self._get_request(repo_endpoint, filter_param)
        # guard condition
        if response.status_code != STATUS_CODE_OK:
            raise BitbucketRequestSenderExc(
                f'Invalid parameter(s) in: owner: {self.owner},'
                f' repo: {self.repo}')
        # deserialize
        repo = response.json()

        return {
            'id': repo['uuid'][1:-1],
            'repo_name': repo['name'],
            'creation_date': str(to_timestamp(repo['created_on'])),
            'owner': repo['owner']['username'],
            'url': repo['links']['self']['href']
        }

    # needs to get all pages
    @try_except_decor
    def get_branches(self):
        """
        Gets list of branches in a repository
        in dict format with response body and status code

        :return: list of dicts
        :Example:
        [
            {
                "name": "branch name"
            },
            ...
        ]
        """

        # gets all branches in repository
        branches_endpoint = f'/repositories/{self.owner}/{self.repo}/refs/branches'
        filter_param = {'fields': 'values.name'}
        response = self._get_request(branches_endpoint, filter_param)
        # guard condition
        if response.status_code != STATUS_CODE_OK:
            raise BitbucketRequestSenderExc(
                f'Invalid parameter(s) in: owner: {self.owner},'
                f' repo: {self.repo}')
        # deserialize
        branches_page = response.json()

        return [
            {
                'name': branch['name']
            } for branch in branches_page['values']
            ]

    @try_except_decor
    def get_commits(self):
        """
        Gets information about all commits in repository
        in dict format with response body and status code

        :return: list of dicts
        :Example:
        [
            {
                "hash": "commit hash",
                "author": "commit author",
                "message": "commit message",
                "date": "date when committed converted to int",
                "branches": [branches names]
            },
            ...
        ]
        """

        repo_commits = {}

        # gets all branches in repository
        branches = self.get_branches()
        if branches is None:
            raise BitbucketRequestSenderExc('Can\'t get branches for get_commits method')

        # get list of commits pages from all branches in repository
        for branch in branches:
            list_of_branch_commits = self.get_commits_by_branch(branch['name'])
            if list_of_branch_commits is None:
                raise BitbucketRequestSenderExc(
                    'Can\'t get commits by branch for get_commits method')

            # adds key 'branches' with branch name in list to every commit in branch,
            #  or if key 'branches' is existing add branch name to existing branches list
            for commit_in_branch in list_of_branch_commits:
                commit = repo_commits.get(commit_in_branch['hash'])
                if commit:
                    commit['branches'].append(branch['name'])
                else:
                    commit_in_branch['branches'] = [branch['name']]
                    repo_commits[commit_in_branch['hash']] = commit_in_branch
            list_of_branch_commits.clear()

        # sorts all commits in repository by date in reverse order
        sorted_commits = sorted(list(repo_commits.values()), key=lambda x: x['date'], reverse=True)

        # forms a list of commits as an 'get commits API' response
        commits_amount = 30 if len(sorted_commits) >= 30 else len(sorted_commits)
        result_list = sorted_commits[:commits_amount]

        return result_list

    @try_except_decor
    def get_commits_by_branch(self, branch_name):
        """
        Gets information about commits of a specific branch
        in dict format with response body and status code

        :param branch_name: string
        :return: list of dicts
        :Example:
        [
            {
                "hash": "commit hash",
                "author": "commit author",
                "message": "commit message",
                "date": "date when committed converted to int"
            },
            ...
        ]
        """

        # gets commit by hash
        assert isinstance(branch_name, str), 'Inputted "branch_name" type is not str'
        branch_commits_endpoint = f'/repositories/{self.owner}/{self.repo}/commits/{branch_name}'
        filter_param = {'fields': 'values.hash,values.author,values.message,values.date'}
        response = self._get_request(branch_commits_endpoint, filter_param)
        # guard condition
        if response.status_code != STATUS_CODE_OK:
            raise BitbucketRequestSenderExc(
                f'Invalid parameter(s) in: owner: {self.owner},'
                f' repo: {self.repo}, branch name: {branch_name}')
        # deserialize commit
        commits_page = response.json()

        return [
            {
                'hash': commit['hash'],
                'author': get_gitname(commit),
                'message': commit['message'],
                'date': str(to_timestamp(commit['date']))
            } for commit in commits_page['values']
            ]

    @try_except_decor
    def get_commit_by_hash(self, hash_of_commit):
        """
        Gets information about the commit by hash
        in dict format with response body

        :param hash_of_commit: string
        :return: dict
        :Example:
        {
            "hash": "commit hash",
            "author": "commit author",
            "message": "commit message",
            "date": "date when committed converted to int",
            "branches": [branches names]
        }
        """

        result = {}

        # gets commit by 'hash'
        assert isinstance(hash_of_commit, str), 'Inputted "hash_of_commit" type is not str'
        commit_endpoint = f'/repositories/{self.owner}/{self.repo}/commit/{hash_of_commit}'
        response = self._get_request(commit_endpoint)
        # guard condition
        if response.status_code != STATUS_CODE_OK:
            raise BitbucketRequestSenderExc(
                f'Invalid parameter(s) in: owner: {self.owner},'
                f' repo: {self.repo}, hash of commit: {hash_of_commit}')
        # deserialize commit
        commit = response.json()

        # gets "branches" from the repository to check each branch
        # for the existence of "commit" found above
        branches = self.get_branches()
        if branches is None:
            raise BitbucketRequestSenderExc('Can\'t get branches for get_commit_by_hash method')
        branches_names = [branch['name'] for branch in branches]

        # gets 'hash' field for every commit in every branch in repo
        for branch in branches_names:
            branch_commits_endpoint = f'/repositories/{self.owner}/{self.repo}/commits/{branch}'
            filter_param = {'fields': 'values.hash'}
            response = self._get_request(branch_commits_endpoint, filter_param)
            # guard condition
            if response.status_code != STATUS_CODE_OK:
                raise BitbucketRequestSenderExc(
                    f'Invalid parameter(s) in: owner: {self.owner},'
                    f' repo: {self.repo}, branch name: {branch}')
            # deserialize commit
            response = response.json()

            for commit_hash in response['values']:
                # compares the hash of each commit in the branch
                # to match to the given commit hash
                if commit_hash['hash'] == hash_of_commit:
                    # forms key 'branches' with branch name in list for commit
                    # or add to exist 'branches' list
                    if 'branches' in result:
                        result['branches'].append(branch)
                    else:
                        result['branches'] = [branch]

        # forms dict of commit describe
        result['hash'] = commit['hash']
        result['author'] = get_gitname(commit)
        result['message'] = commit['message']
        result['date'] = str(to_timestamp(commit['date']))

        return result

    # ! ! ! needs check for duplicate
    @try_except_decor
    def get_contributors(self):
        """
        Gets information about all contributors to repository
        in dict format with response body

        :return: list of dicts
        :Example:
        [
             {
                 "name": "contributor name",
                 "number_of_commits": "number of commits",
                 "email": "contributor email",
                 "url": "contributor url"
             },
             ...
        ]
        """

        contributors = {}

        # gets all commits in repo to find all contributors
        commits_endpoint = f'/repositories/{self.owner}/{self.repo}/commits'
        response = self._get_request(commits_endpoint)
        # guard condition
        if response.status_code != STATUS_CODE_OK:
            raise BitbucketRequestSenderExc(
                f'Invalid parameter(s) in: owner: {self.owner}, repo: {self.repo}')
        # deserialize commits
        commits_page = response.json()

        # for each commit
        for commit in commits_page['values']:

            # commit['author']['raw'] - unique string 'user_gitname <user_email>'
            # if we haven't tracked commit author yet
            if commit['author']['raw'] not in contributors:
                # check if author has key 'user' means check if author has bitbucket account,
                #  if doesn't return  None
                user = commit['author'].get('user')

                # start tracking commit author
                contributors[commit['author']['raw']] = {
                    # if has account assign account's username else author's gitname
                    'name': get_gitname(commit),
                    'number_of_commits': 1,  # count number of commits
                    'email': get_email(commit['author']['raw']),
                    'url': user['links']['html']['href'] if user else None
                }
            else:
                # if author is already being tracked increment number of commits by one
                contributors[commit['author']['raw']]['number_of_commits'] += 1

        return list(contributors.values())

    ########################################################################################

    # test mode
    @try_except_decor
    def get_all_commits_by_branch(self, branch_name):
        """
            Gets list of all commits by given branch.

        :param branch_name: str
        :return: list - list of all commits
        """

        full_response = []
        # declare response dict with kay 'next' to enable first iteration
        response = {'next': 'eny text'}
        page = 1

        while 'next' in response.keys():
            response = self._get_page_of_commits_by_branch(branch_name, page)
            full_response.extend(response['values'])
            page += 1

        # parser
        parsed_full_response = [
            {
                'hash': commit['hash'],
                'author': get_gitname(commit),
                'message': commit['message'],
                'date': str(to_timestamp(commit['date']))
            } for commit in full_response
            ]

        return parsed_full_response

    # test mode
    @try_except_decor
    def get_by_branch_since_hash(self, branch_name, hash_of_commit=None):
        """
            Gets list of all commits by branch name since given hash of commit

        :param branch_name: str
        :param hash_of_commit: str - stop iterations in case
            all commits newer than given are received
        :return: list - list of since given hash
        """

        full_response = []
        # declare response dict with kay 'next' to enable first iteration
        response = {'next': 'eny text'}
        page = 1
        go_on = True

        # gets all pages of commits and stops when given commit is found
        while 'next' in response.keys() and go_on:
            # gets commits by page and by branch)
            response = self._get_page_of_commits_by_branch(branch_name, page)

            # checks for needed commit, and stops getting commits pages
            if hash_of_commit:
                for count_commit in range(len(response['values'])):
                    # makes a partial result of _get_page_of_commits_by_branch to avoid duplicates
                    if response['values'][count_commit]['hash'] == hash_of_commit:
                        response['values'] = response['values'][:count_commit]
                        go_on = False
                        break

            # adds the result of the current page to the overall result
            full_response.extend(response['values'])
            page += 1

        # parser
        parsed_full_response = [
            {
                'hash': commit['hash'],
                'author': get_gitname(commit),
                'message': commit['message'],
                'date': str(to_timestamp(commit['date']))
            } for commit in full_response
            ]

        return parsed_full_response

    # test mode
    @try_except_decor
    def get_updated_commits_by_branch(self, branch_name, old_commits, only_new=False):
        """
            Updates given list of commits by branch,
            returns list of given commits and all newer
            commits since last commit in given list of commits

        :param branch_name: str
        :param old_commits: list - list of commits to update
        :param only_new: bool - get commits without adding old ones if True
        :return:list - updated list of commits
        """

        # get last commit hash ( to get commits since given hash)
        # or set None (to get all commits).For updating all commits, when updating
        #   gives new branch that don't have last commit.
        hash_of_commit = old_commits[0]['hash'] if old_commits else None

        result = self.get_by_branch_since_hash(branch_name=branch_name,
                                               hash_of_commit=hash_of_commit)

        # do not add old commits if 'only_new=True' for updating all commits
        #   where is used mapping by branch,
        # or add if 'only_new=False'
        result += old_commits if old_commits and not only_new else []

        return result

    # test mode
    # has different response format
    @try_except_decor
    def get_all_commits(self):
        """
        Gets information about all commits in repository
        in dict format with response body and status code

        :return: dict of list of commits and metadata
        :Example:
        {
            'data':[
                        {
                            "hash": "commit hash",
                            "author": "commit author",
                            "message": "commit message",
                            "date": "date when committed converted to int",
                            "branches": [branches names]
                        },
                        ...
                    ],

            'metadata':
                        {
                            "branch_name": "newest commit"
                            ...
                        }
        }
        """

        repo_commits = {}
        metadata = {}

        # gets all branches in repository
        branches = self.get_branches()
        if branches is None:
            return None

        # get list of commits pages from all branches in repository
        for branch in branches:
            list_of_branch_commits = self.get_all_commits_by_branch(branch['name'])

            if list_of_branch_commits is None:
                return None

            # adds key 'branches' with branch name in list to every commit in branch,
            #  or if key 'branches' is existing add branch name to existing branches list
            for commit_in_branch in list_of_branch_commits:
                commit = repo_commits.get(commit_in_branch['hash'])
                if commit:
                    commit['branches'].append(branch['name'])
                else:
                    commit_in_branch['branches'] = [branch['name']]
                    repo_commits[commit_in_branch['hash']] = commit_in_branch

            # add metadata to method response for further updates by get_updated_all_commits
            metadata[branch['name']] = list_of_branch_commits[0]

            list_of_branch_commits.clear()

        # sorts all commits in repository by date in reverse order
        sorted_commits = sorted(list(repo_commits.values()), key=lambda x: x['date'], reverse=True)

        return {'data': sorted_commits, 'metadata': metadata}

    # test mode
    # has different response format
    @try_except_decor
    def get_updated_all_commits(self, old_commits):  # pylint: disable=too-many-locals
        """
            Updates given list of commits by newer list of branches,
            returns list of given commits and all newer
            commits since last commit in given list of commits

        :param old_commits: dict - list of commits to update and metadata
        :return:dict - updated list of commits and metadata
        """

        # get new list of branches
        newest_branches_names = [branch_info['name'] for branch_info in self.get_branches()]

        # get old list of branches from old metadata
        old_branches_names = list(old_commits['metadata'].keys())

        # get old metadata
        old_commits_metadata = old_commits['metadata']
        result = {}

        # delete all items in old metadata where branch name is not exist in new list of branches
        for old_branch_name in old_branches_names:
            if not newest_branches_names.count(old_branch_name):
                old_commits_metadata.pop(old_branch_name)

        checked_commits_metadata = old_commits_metadata
        # add to checked_commits_metadata all metadata that is not exist in old_commits_metadata
        for branch in newest_branches_names:
            if not old_branches_names.count(branch):
                checked_commits_metadata[branch] = None

        # get dict of old commits with key - hash of commit for further mapping by branch
        repo_commits = {commit['hash']: commit for commit in old_commits['data']}

        # get list of new commits from all branches in repository
        for branch_name, newest_commit in checked_commits_metadata.copy().items():
            updated_list_of_branch_commits = \
                self.get_updated_commits_by_branch(branch_name, newest_commit, only_new=True)
            if updated_list_of_branch_commits is None:
                return None

            # adds key 'branches' with branch name in list to every commit in branch,
            #  or if key 'branches' is existing add branch name to existing branches list
            for commit_in_branch in updated_list_of_branch_commits:
                commit = repo_commits.get(commit_in_branch['hash'])
                if commit:
                    commit['branches'].append(branch_name)
                else:
                    commit_in_branch['branches'] = [branch_name]
                    repo_commits[commit_in_branch['hash']] = commit_in_branch

            # add new metadata to method response for further updates by get_updated_all_commits
            if updated_list_of_branch_commits:
                checked_commits_metadata[branch_name] = updated_list_of_branch_commits[0]
            else:
                # if given old commit is the newest - add it to new metadata. P.S unnecessary ???
                checked_commits_metadata[branch_name] = newest_commit[0]

            updated_list_of_branch_commits.clear()

        # sorts all commits in repository by date in reverse order
        updated_sorted_commits = sorted(list(repo_commits.values()), key=lambda x: x['date'],
                                        reverse=True)

        result['data'] = updated_sorted_commits
        result['metadata'] = checked_commits_metadata

        return result


class BitbucketServerRequestSender(RequestSender):
    """
    Provides methods for sending API requests to Bitbucket Server
    for version control using Git
    """

    @try_except_decor
    def __init__(self, owner, repo, project='',
                 base_url='http://192.168.0.104:7990/rest/api/1.0/projects', ):

        assert isinstance(project, str), 'Inputted "project" type is not str'

        super().__init__(base_url=base_url, owner=owner, repo=repo)

        self.base_url = base_url + '/' + (project or f'~{owner}')
        self.project = project

    @try_except_decor
    def _get_request(self, endpoint, params=None, **kwargs):
        """
        Sends GET request to URL
        :param endpoint: string - endpoint url
        :param params: dict - of request parameters
        :param kwargs: - other optional parameters
        :return: json - response object
        """

        return requests.get(self.base_url + endpoint, params, **kwargs)

    @try_except_decor
    def get_repo(self):
        """
        Gets information about repository
        in dict format with response body and status code

        :return: dict
        :Example:
        {
            "id": "unique id",
            "repo_name": "repository name",
            "creation_date": "date",
            "owner": "repository owner",
            "url": "repository url"
        }
        """

        # gets information about repository
        repo_endpoint = f'/repos/{self.repo}'
        response = self._get_request(repo_endpoint)
        # guard condition
        if response.status_code != STATUS_CODE_OK:
            return None
        # deserialize
        repo = response.json()

        return {
            'id': repo['id'],
            'repo_name': repo['name'],
            'creation_date': None,
            'owner': None,
            'url': repo['links']['self'][0]['href']
        }

    @try_except_decor
    def get_branches(self):
        """
        Gets list of branches in a repository
        in dict format with response body and status code

        :return: list of dicts
        :Example:
        [
            {
                "name": "branch name"
            },
            ...
        ]
        """

        # gets all branches in repository
        branches_endpoint = f'/repos/{self.repo}/branches'
        response = self._get_request(branches_endpoint)
        # guard condition
        if response.status_code != STATUS_CODE_OK:
            return None
        # deserialize
        branches_page = response.json()

        return [
            {
                'name': branch['displayId']
            } for branch in branches_page['values']
            ]

    @try_except_decor
    def get_commits(self):
        """
        Gets information about all commits in repository
        in dict format with response body and status code

        :return: list of dicts
        :Example:
        [
            {
                "hash": "commit hash",
                "author": "commit author",
                "message": "commit message",
                "date": "date when committed converted to int",
                "branches": [branches names]
            },
            ...
        ]
        """

        repo_commits = {}

        # gets all branches in repository
        branches = self.get_branches()
        if branches is None:
            return None

        # get list of commits pages from all branches in repository
        for branch in branches:
            list_of_branch_commits = self.get_commits_by_branch(branch['name'])
            if list_of_branch_commits is None:
                return None

            # adds key 'branches' with branch name in list to every commit in branch,
            #  or if key 'branches' is existing add branch name to existing branches list
            for commit_in_branch in list_of_branch_commits:
                commit = repo_commits.get(commit_in_branch['hash'])
                if commit:
                    commit['branches'].append(branch['name'])
                else:
                    commit_in_branch['branches'] = [branch['name']]
                    repo_commits[commit_in_branch['hash']] = commit_in_branch
            list_of_branch_commits.clear()

        # sorts all commits in repository by date in reverse order
        sorted_commits = sorted(list(repo_commits.values()), key=lambda x: x['date'], reverse=True)

        # forms a list of commits as an 'get commits API' response
        commits_amount = 30 if len(sorted_commits) >= 30 else len(sorted_commits)
        result_list = sorted_commits[:commits_amount]

        return result_list

    @try_except_decor
    def get_commits_by_branch(self, branch_name):
        """
        Gets information about commits of a specific branch
        in dict format with response body and status code

        :param branch_name: string
        :return: list of dicts
        :Example:
        [
            {
                "hash": "commit hash",
                "author": "commit author",
                "message": "commit message",
                "date": "date when committed converted to int"
            },
            ...
        ]
        """

        assert isinstance(branch_name, str), 'Inputted "branch_name" type is not str'

        branch_commits_endpoint = f'/repos/{self.repo}/commits'
        params = {'until': branch_name}
        response = self._get_request(branch_commits_endpoint, params)

        # guard condition
        if response.status_code != STATUS_CODE_OK:
            return None

        commits_page = response.json()
        return [
            {
                'hash': commit['id'],
                'author': (
                    commit['author']['name'] if 'name' in commit['author'] else None),
                'message': commit['message'],
                'date': commit['authorTimestamp']
            } for commit in commits_page['values']
            ]

    @try_except_decor
    def get_commit_by_hash(self, hash_of_commit):
        """
        Gets information about the commit by hash
        in dict format with response body

        :param hash_of_commit: string
        :return: dict
        :Example:
        {
            "hash": "commit hash",
            "author": "commit author",
            "message": "commit message",
            "date": "date when committed converted to int",
            "branches_name": [branches_name names]
        }
        """

        result = {}

        # gets commit by 'hash'
        assert isinstance(hash_of_commit, str), 'Inputted "hash_of_commit" type is not str'
        commit_endpoint = f'/repos/{self.repo}/commits/{hash_of_commit}'
        response = self._get_request(commit_endpoint)
        # guard condition
        if response.status_code != STATUS_CODE_OK:
            return None
        # deserialize commit
        commit = response.json()

        # gets "branches_name" from the repository to check each branch
        # for the existence of found "commit"
        branches_name = [branch['name'] for branch in self.get_branches()]
        for branch_name in branches_name:
            commits_by_branch = self.get_commits_by_branch(branch_name)
            # guard condition
            if commits_by_branch is None:
                return None

            for commit_by_branch in commits_by_branch:
                # compares the hash of each commit in the branch
                # to match to the given commit hash
                if commit_by_branch['hash'] == hash_of_commit:
                    # forms key 'branches' with branch name in list for commit
                    # or add to exist 'branches' list
                    if 'branches_name' in result:
                        result['branches_name'].append(branch_name)
                    else:
                        result['branches_name'] = [branch_name]

        # forms dict of commit describe
        result['hash'] = commit['id']
        result['author'] = commit['author']['name']
        result['message'] = commit['message']
        result['date'] = commit['authorTimestamp']

        return result

    # ! ! ! needs another contributor for test
    # ! ! ! needs check for duplicate
    @try_except_decor
    def get_contributors(self):
        """
        Gets information about all contributors to repository
        in dict format with response body

        :return: list of dicts
        :Example:
        [
             {
                 "name": "contributor name",
                 "number_of_commits": "number of commits",
                 "email": "contributor email",
                 "url": "contributor url"
             },
             ...
        ]
        """

        commits_page = []
        contributors = {}

        branches = self.get_branches()

        for branch in branches:
            branch_name = branch['name']
            branch_commits_endpoint = f'/repos/{self.repo}/commits'
            params = {'until': branch_name}
            response = self._get_request(branch_commits_endpoint, params)
            if response.status_code != STATUS_CODE_OK:
                return None
            # deserialize
            response = response.json()
            commits_page.extend(response['values'])

        # for each commit
        for commit in commits_page:
            author = commit['author']  # dict with author's properties
            links = author.get('links')

            # if we haven't tracked commit author yet
            if author['name'] not in contributors:

                # check if author has key 'user' means check if author has bitbucket account,
                #  if doesn't return  None
                user = author['name']

                # start tracking commit author
                contributors[author['name']] = {
                    # if has account assign account's username else author's gitname
                    'name': user,
                    'number_of_commits': 1,  # count number of commits
                    'email': commit['author']['emailAddress'],
                    'url': links['self'][0]['href'] if links else None
                }
            else:
                # if author is already being tracked increment number of commits by one
                contributors[commit['author']['name']]['number_of_commits'] += 1
                if links is not None:
                    contributors[author['name']]['url'] = links['self'][0]['href']
        return list(contributors.values())
