"""
Contains RequestSender class that provides interface for sending API requests
to web-based hosting services for version control using Git
"""


class RequestSender:
    """
    Base class that provides interface for sending API requests
    to web-based hosting services for version control using Git
    """

    def __init__(self, base_url):
        self.base_url = base_url

    def get_repo(self, name, owner):
        """
        Takes repository name and owner as parameters and
        returns repository info in JSON format
        ex:
        {
            "id": "unique id",
            "repo_name": "repository name",
            "creation_date": "date",
            "owner": "repository owner",
            "url": "repository url"
        }

        :param name: string - repository name
        :param owner: string - repository owner
        :return: string - JSON formatted response
        """
        pass

    def get_branches(self, name, owner):
        """
        Takes repository name and owner as parameters and returns
        information about branches in JSON format
        ex:
        [
            {
                "name": "branch name"
            },
            ...
        ]

        :param name: string - repository name
        :param owner: string - repository owner
        :return: string - JSON formatted response
        """
        pass

    def get_commits(self, name, owner):
        """
        Takes repository name and owner as parameters and
        returns information about commits in JSON format
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

        :param name: string - repository name
        :param owner: string - repository owner
        :return: string - JSON formatted response
        """
        pass

    def get_contributors(self, name, owner):
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

        :param name: string - repository name
        :param owner: string - repository owner
        :return: string - JSON formatted response
        """
        pass

