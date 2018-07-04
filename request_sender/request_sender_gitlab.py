from request_sender_base import RequestSender
import requests


class RequestSenderGitLab(RequestSender):
    def get_repo(self):
        """
        Takes repository name on GitLab and owner as parameters and
        returns repository info in JSON format
        ex:
        {
            "id": "unique id",
            "repo_name": "repository name",
            "creation_date": "date",
            "owner": "repository owner",
            "url": "repository url"
        }

        :return: string - JSON formatted response
        """
        # get url of remote repository given as input
        url_repo = self.base_url + self.owner + "%2F" + self.name

        # get JSON with repository info
        repo_info = requests.get(url_repo).json()

        # retrieve only info about repository
        repo = [{"id": repo_info['id'],
                 "repo_name": repo_info['name'],
                 "creation_date": repo_info['created_at'],
                 "url": repo_info['web_url']}]

        return repo

    def get_branches(self):
        """
        get branches of given repository on GitLab
        ex:
        [
            {
                "name": "branch name"
            },
            ...
        ]

        :return: list of dicts
        """

        # get url of remote repository given as input
        url_branches = self.base_url + self.owner + "%2F" + self.name + "/repository/branches"

        # get JSON about branches
        branches_info = requests.get(url_branches).json()

        # retrieve only info about name of the branches
        branches = [{"name": branches_info[i]['name']} for i in range(len(branches_info))]

        return branches

    def get_commits(self):
        """
        Takes repository name and owner as parameters and
        returns information about commits in list of dictionaries
        ex
        [
            {
                "hash": "commit hash",
                "author": "commit author",
                "message": "commit message",
                "date": "date when committed"

            },
            ...
        ]

        :return: string - list of dictionaries
        """
        # get url of remote repository given as input
        url_commits = self.base_url + self.owner + "%2F" + self.name + "/repository/commits"

        # get JSON about commits
        commits_info = requests.get(url_commits).json()

        # retrieve only info about commits
        commits = [{'hash': commits_info[i]['id'],
                    'author': commits_info[i]['committer_name'],
                    'message': commits_info[i]['message'],
                    'date': commits_info[i]['created_at']} for i in range(len(commits_info))]

        return commits

    def get_contributors(self):
        """
        Takes repository name and owner as parameters and returns
        information about contributors in JSON format
        ex
        [
            {
                "name": "contributor name",
                "number_of_commits": "number of commits",
                "email": "contributor email",
                "url": "contributor url"
            },
            ...
        ]

        :return: string - JSON formatted response
        """
        # get url of remote repository given as input
        url_contributors = self.base_url + self.owner + "%2F" + self.name + "/repository/contributors"

        # get JSON about contributors
        contributors_info = requests.get(url_contributors).json()

        # retrieve only info about contributors
        contributors = [{'name': contributors_info[i]['name'],
                         'number_of_commits': contributors_info[i]['commits'],
                         'email': contributors_info[i]['email'],
                         'url': 'https://gitlab.com/' + str(contributors_info[i]['name'])}
                        for i in range(len(contributors_info))]

        return contributors
