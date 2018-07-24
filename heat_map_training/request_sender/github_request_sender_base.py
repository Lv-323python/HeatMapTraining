"""
Contains RequestSender class that provides interface for sending API requests
to web-based hosting services for version control using Git
"""

from heat_map_training.request_sender.request_sender_base \
    import RequestSender


class GithubRequestSenderBase(RequestSender):
    """
    Base class that provides interface for sending API requests
    to web-based hosting services for version control using Git
    """

    def __init__(self, base_url, owner, repo):
        super().__init__(base_url, owner, repo)
        self.base_url = base_url
        self.owner = owner
        self.repo = repo

    def get_repo(self):
        """
        Gets information about repository
        in dict format with response body and status code

        :return: dict
        :raise NotImplementedError
        :Example:
        {
            "id": "unique id",
            "repo_name": "repository name",
            "creation_date": "date",
            "owner": "repository owner",
            "url": "repository url"
        }
        """
        pass

    def get_branches(self):
        """
        Gets list of branches in a repository
        in dict format with response body and status code

        :return: list of dicts
        :raise NotImplementedError
        :Example:
        [
            {
                "name": "branch name"
            },
            ...
        ]
        """
        pass

    def get_commits(self):
        """
        Gets information about all commits in repository
        in dict format with response body and status code

        :return: list of dicts
        :raise NotImplementedError
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
        pass

    def get_commits_by_branch(self, branch_name):
        """
        Gets information about commits of a specific branch
        in dict format with response body and status code

        :param branch_name: string
        :return: list of dicts
        :raise NotImplementedError
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

        pass

    def get_commit_by_hash(self, hash_of_commit):
        """
        Gets information about the commit by hash
        in dict format with response body

        :param hash_of_commit: string
        :return: dict
        :raise NotImplementedError
        :Example:
        {
            "hash": "commit hash",
            "author": "commit author",
            "message": "commit message",
            "date": "date when committed converted to int"

        }
        """

        pass

    def get_contributors(self):
        """
        Gets information about all contributors to repository
        in dict format with response body

        :return: list of dicts
        :raise NotImplementedError
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
        pass
