"""
Contains RequestSender class that provides interface for sending API requests
to web-based hosting services for version control using Git
"""


class RequestSender:
    """
    Base class that provides interface for sending API requests
    to web-based hosting services for version control using Git
    """

    def __init__(self, base_url, owner, name):
        self.base_url = base_url
        self.owner = owner
        self.name = name

    def get_repo(self):
        """
        Takes repository name and owner as parameters and
        returns repository info in JSON format
        Example:
        {
            "id": "unique id",
            "repo_name": "repository name",
            "creation_date": "date",
            "owner": "repository owner",
            "url": "repository url"
        }

        :return: string - JSON formatted response
        """


    def get_branches(self):
        """
        Takes repository name and owner as parameters and returns
        information about branches in JSON format
        Example:
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

    def get_commits(self, name, owner):
        """
        Takes repository name and owner as parameters and
        returns information about commits in JSON format
        Example:
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
