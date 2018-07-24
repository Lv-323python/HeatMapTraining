import json
import requests
from heat_map_training.request_sender.github_request_sender_base import \
    GithubRequestSenderBase
from heat_map_training.utils.request_status_codes import STATUS_CODE_OK


class GithubRequestSenderV4(GithubRequestSenderBase):
    def __init__(self, owner, repo, token='', base_url='https://api.github.com/graphql'):
        """
        Github api requests class

        :rtype: object
        :param token: github api token string
        """
        GithubRequestSenderBase.__init__(self,
                                         base_url=base_url,
                                         owner=owner,
                                         repo=repo)
        self.base_url = base_url
        self.token = token
        self.headers = {
            'Authorization': 'token {token}'.format(token=token),
        }

    def query(self, query):
        """
        General query

        :param query: dict
        :return: dict
        """
        query = {'query': query.query_to_json(first=True)}
        print(query)
        response = requests.post(url=self.base_url,
                                 json=query,
                                 headers=self.headers)
        if response.status_code != STATUS_CODE_OK:
            return None
        return json.dumps(response.json(), sort_keys=True, indent=4, separators=(',', ': '))

    def get_all_repos(self):
        """
        Query all repositories of owner

        :return: name list
        """
        needed_fields = ['oid', 'repo_name: name', 'creation_date: createdAt']
        query = Query('repositories', attributes={'first': 30}, query=Query('nodes', query=needed_fields.reverse()))
        root = Query('viewer', query=query)
        response = self.query(root)
        return response

    def get_repo(self):
        """
        Query a repository

        :return: dict
        """
        needed_fields = ['object(oid)', 'repo_name: name', 'creation_date: createdAt']
        query = Query('repository', attributes={'owner': self.owner, 'name': self.repo},
                      query=needed_fields)
        response = self.query(query)
        return response

    def get_commits(self):
        pass


class Query:
    """
    Generates query string
    """

    def __init__(self, name, query=None, attributes=None):
        if attributes is None:
            attributes = {}
        self.query = []
        self.add_query(query)
        self.name = name
        self.attributes = attributes

    def add_attributes(self, key, values):
        self.attributes[key] = values

    def add_query(self, query):
        if query is None:
            return
        if isinstance(query, list):
            for row in query:
                self.query.append(Query(name=row))
        elif isinstance(query, str):
            self.query.append(Query(name=query))
        else:
            self.query.append(query)

    def query_to_json(self, first=False):
        if not self.query:
            return self.name
        if self.attributes:
            for key, value in self.attributes.items():
                if isinstance(value, str) and not value.isdigit():
                    self.attributes[key] = '"' + value + '"'
            attribute = ', '.join(
                ['{key}: {values}'.format(key=key, values=values)
                 for key, values in self.attributes.items()]
            )
            query = """%s(%s){ %s }""" % (
                self.name, attribute, ' '.join([query.query_to_json() for query in self.query if
                                                query is not None]))
        else:
            query = """ %s { %s } """ % (
                self.name, ' '.join([query.query_to_json() for query in self.query if query is not None]))
        if first:
            query = "{ %s }" % query
        return query
