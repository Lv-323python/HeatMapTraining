"""
Contains RequestSender class that provides interface for sending API requests
to web-based hosting services for version control using Git
"""


class RequestSender:
    """
    Base class that provides interface for sending API requests
    to web-based hosting services for version control using Git
    """

    def __init__(self, base_url, owner, repo):
        self.base_url = base_url
        self.owner = owner
        self.repo = repo

    def get_repo(self):
        """
        Gets repository info in JSON format
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

    def get_branches(self):
        """
        Gets information about branches in JSON format
        ex:
        [
            {
                "name": "branch name"
            },
            ...
        ]

        :return: string - JSON formatted response
        """

    def get_commits(self):
        """
        Gets information about commits in JSON format
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

        :return: string - JSON formatted response
        """
