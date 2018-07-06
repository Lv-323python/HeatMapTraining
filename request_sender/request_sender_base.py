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
        example:
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
        example:
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
        example:
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

    def get_commits_by_branch(self, branch_name):
        """
                Gets information about commits (in branch specified) in JSON format
        example:
        [
            {
                "hash": "commit hash",
                "author": "commit author",
                "message": "commit message",
                "date": "date when committed"

            },
            ...
        ]

        :param branch_name: string
        :return: string - JSON formatted response
        """

    def get_commit_by_hash(self, hash_of_commit):
        """
        Gets information about the commit by hash in JSON format
        example:
        {
            "hash": "commit hash",
            "author": "commit author",
            "message": "commit message",
            "date": "date when committed"

        }

        :param hash_of_commit: string
        :return: string - JSON formatted response
        """

    def get_contributors(self):
        """
         Gets information about contributors
           example:
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
