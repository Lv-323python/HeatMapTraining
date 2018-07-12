'''
Contains RequestSenderGitLab class that provides realisation for sending API requests
to web-based hosting services for version control using Git
'''

from datetime import datetime
import requests
from request_sender_base import RequestSender  # pylint: disable=import-error


def _timestamp(date):
    '''
    Converts datetime string to timestamp
    :param date_time_str: string - datetime string
    :return: int - timestamp
    '''
    return int(datetime.strptime(date[:-5], '%Y-%m-%dT%H:%M:%S').timestamp())


class RequestSenderGitLab(RequestSender):
    '''
    GitLab class that provides realisation for sending API requests
    to web-based hosting services for version control using Git
    '''

    def get_repo(self):
        '''
        Takes repository name on GitLab and owner as parameters and
        returns repository info in dictionary

        :return: string - JSON formatted response

        example of output:
        {
            'id': 'unique id',
            'repo_name': 'repository name',
            'creation_date': 'date',
            'owner': 'repository owner',
            'url': 'repository url'
        }

        '''
        # get url of remote repository given as input
        url_repo = self.base_url + self.owner + '%2F' + self.repo

        # get JSON with repository info
        repo_info = requests.get(url_repo).json()

        # retrieve only info about repository
        repo = {
            'id': repo_info['id'],
            'repo_name': repo_info['name'],
            'creation_date': _timestamp(repo_info['created_at']),
            'owner': repo_info['path_with_namespace'].split('/')[0],
            'url': repo_info['web_url']
        }

        return repo

    def get_branches(self):
        '''
        get branches of given repository on GitLab

        :return: list of dicts

        example of output:
        [
            {
                'name': 'branch name'
            },
            ...
        ]
        '''

        # get url of remote repository given as input
        url_branches = self.base_url + self.owner + '%2F' + self.repo + '/repository/branches'

        # get JSON about branches
        branches_info = requests.get(url_branches).json()

        # retrieve only info about name of the branches
        branches = [{'name': branch['name']} for branch in branches_info]

        return branches

    def get_commits(self):
        '''
        Takes repository name and owner as parameters and
        returns information about commits in list of dictionaries

        :return: list of dictionaries

        example
        [
            {
                'hash': 'commit hash',
                'author': 'commit author',
                'message': 'commit message',
                'date': 'date when committed'

            },
            ...
        ]
        '''
        # get url of remote repository given as input
        url_commits = self.base_url + self.owner + '%2F' + self.repo + '/repository/commits'

        # get JSON about commits
        commits_info = requests.get(url_commits).json()

        # retrieve only info about commits
        commits = [{
            'hash': commit['id'],
            'author': commit['committer_name'],
            'message': commit['message'],
            'date': _timestamp(commit['created_at'])
        } for commit in commits_info]

        return commits

    def get_contributors(self):
        '''
        Takes repository name and owner as parameters and returns
        information about contributors in list of dictionaries

        :return: list of dictionaries

        example of output
        [
            {
                'name': 'contributor name',
                'number_of_commits': 'number of commits',
                'email': 'contributor email',
                'url': 'contributor url'
            },
            ...
        ]
        '''
        # get url of remote repository given as input
        url_contributors = (self.base_url + self.owner + '%2F' + self.repo +
                            '/repository/contributors')

        # get JSON about contributors
        contributors_info = requests.get(url_contributors).json()

        # retrieve only info about contributors
        contributors = [{
            'name': contributors_info[i]['name'],
            'number_of_commits': contributors_info[i]['commits'],
            'email': contributors_info[i]['email'],
            'url': 'https://gitlab.com/' + str(contributors_info[i]['name'])
        } for i in range(len(contributors_info))]

        return contributors

    def get_commit_by_hash(self, hash_of_commit):
        '''
        Takes hash of the commit and returns info about it in dictionary:

        :param hash_of_commit: string
        :return: dictionary

        example of output:
        {
            'hash': 'commit hash',
            'author': 'commit author',
            'message': 'commit message',
            'date': 'date when committed'

        }
        '''
        # get url of remote repository given as input
        url_commit = self.base_url + self.owner + '%2F' + self.repo + \
                     '/repository/commits/' + hash_of_commit

        # get JSON about one commit
        commit_info = requests.get(url_commit).json()

        # retrieve only info about one commit
        commit = {
            'hash': commit_info['id'],
            'author': commit_info['author_name'],
            'message': commit_info['message'],
            'date': _timestamp(commit_info['committed_date'])
        }

        return commit

    def get_commits_by_branch(self, branch_name):
        '''
        Takes repository branches as parameters and
        returns information about last 20 commits per branch
        in list of dictionries


        :return: dictionary

        example of output:
        [{

            'hash': 'commit hash',
            'author': 'commit author',
            'message': 'commit message',
            'date': 'date when committed'

        },
        ...]
        '''

        api_commits_by_branch = self.base_url + self.owner + '%2F' + self.repo + \
                                '/repository/commits?ref_name=' + branch_name

        commits_json = requests.get(api_commits_by_branch).json()
        # make a list of dicts concerning commits per branch
        commits = [{
            'hash': commit['id'],
            'author': commit['committer_name'],
            'message': commit['message'],
            'date': _timestamp(commit['created_at'])
        } for commit in commits_json]

        return commits
