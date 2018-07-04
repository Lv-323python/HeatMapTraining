from request_sender_base import RequestSender
import requests

class GitLab(RequestSender):
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
        :param name: string - repository name
        :param owner: string - repository owner
        :return: list of dicts
        """

        # get url of remote repository given as input
        url_branches = self.base_url + self.owner + "%2F" + self.name + "/repository/branches"

        # get JSON about branches
        branches_info = requests.get(url_branches).json()

        # retrieve only info about name of the branches
        branches = [{"name": branches_info[i]['name']} for i in range(len(branches_info))]

        return branches
