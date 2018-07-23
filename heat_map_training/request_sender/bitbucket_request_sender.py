"""
Contains BitbucketRequestSender class that provides methods for sending API requests
to web-based hosting service Bitbucket for version control using Git and
BitbucketServerRequestSender class hat provides the same methods for sending API requests
to Bitbucket Server.
"""

import requests

from heat_map_training.request_sender.request_sender_base import RequestSender  # pylint: disable=import-error
from heat_map_training.utils.bitbucket_helper import to_timestamp, get_gitname, get_email
from heat_map_training.utils.request_status_codes import STATUS_CODE_OK


class BitbucketRequestSender(RequestSender):
    """
    Provides methods for sending API requests to web-based hosting service Bitbucket
    for version control using Git
    """

    def __init__(self, owner, repo, base_url='https://api.bitbucket.org/2.0'):
        super().__init__(base_url=base_url, owner=owner, repo=repo)

    def _get_request(self, endpoint, params=None, **kwargs):
        """
        Sends GET request to URL
        :param endpoint: string - endpoint url
        :param params: dict - of request parameters
        :param kwargs: - other optional parameters
        :return: json - response object
        """
        return requests.get(self.base_url + endpoint, params, **kwargs)

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
            return None
        # deserialize
        repo = response.json()

        return {
            'id': repo['uuid'][1:-1],
            'repo_name': repo['name'],
            'creation_date': str(to_timestamp(repo['created_on'])),
            'owner': repo['owner']['username'],
            'url': repo['links']['self']['href']
        }

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
            return None
        # deserialize
        branches_page = response.json()

        return [
            {
                'name': branch['name']
            } for branch in branches_page['values']
            ]

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
            return None
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
            return None
        # deserialize commit
        commit = response.json()

        # gets "branches" from the repository to check each branch
        # for the existence of "commit" found above
        branches = self.get_branches()
        branches_names = [branch['name'] for branch in branches]

        # gets 'hash' field for every commit in every branch in repo
        for branch in branches_names:
            branch_commits_endpoint = f'/repositories/{self.owner}/{self.repo}/commits/{branch}'
            filter_param = {'fields': 'values.hash'}
            response = self._get_request(branch_commits_endpoint, filter_param)
            # guard condition
            if response.status_code != STATUS_CODE_OK:
                return None
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
            return None
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


class BitbucketServerRequestSender(RequestSender):
    """
    Provides methods for sending API requests to Bitbucket Server
    for version control using Git
    """

    def __init__(self, owner, repo, project='',
                 base_url='http://192.168.0.104:7990/rest/api/1.0/projects', ):

        assert isinstance(project, str), 'Inputted "project" type is not str'

        super().__init__(base_url=base_url, owner=owner, repo=repo)

        self.base_url = base_url + '/' + (project or f'~{owner}')
        self.project = project

    def _get_request(self, endpoint, params=None, **kwargs):
        """
        Sends GET request to URL
        :param endpoint: string - endpoint url
        :param params: dict - of request parameters
        :param kwargs: - other optional parameters
        :return: json - response object
        """

        return requests.get(self.base_url + endpoint, params, **kwargs)

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
