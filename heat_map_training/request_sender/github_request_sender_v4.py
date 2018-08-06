import json
from collections import namedtuple
import graphene
import requests
from heat_map_training.request_sender.github_request_sender_base import \
    GithubRequestSenderBase
from gql import Client, gql
from gql.transport.requests import RequestsHTTPTransport


def request_post(param, base_url, headers):
    query_body = {'query': param}
    response = requests.post(url=base_url,
                             json=query_body,
                             headers=headers)
    return response.json()


def request_get(url):
    response = requests.get(url=url, headers={'Authorization': 'token ...'}) # pass a token here
    return response.json()


def _json_object_hook(d):
    return namedtuple('X', d.keys())(*d.values())


def json2obj(data):
    return json.loads(data, object_hook=_json_object_hook)


class GithubRequestSenderV4(GithubRequestSenderBase):
    def __init__(self, owner, repo, token, base_url='https://api.github.com/graphql'):
        """
        Github api requests class based on GraphQl

        :rtype: object
        :param token: github api token string
        """
        GithubRequestSenderBase.__init__(self,
                                         base_url=base_url,
                                         owner=owner,
                                         repo=repo,
                                         token=token)
        self.base_url = base_url


class Repository(graphene.ObjectType):
    name = graphene.String(required=True)
    created_at = graphene.DateTime(required=True)
    owner = graphene.String(required=True)
    url = graphene.String(required=True)


class Commit(graphene.ObjectType):
    hash = graphene.String(required=True)


def get_repo(name):
    return Repository(name=name)


class Query(graphene.ObjectType):
    repository = graphene.Field(
        Repository,
        id=graphene.ID(),
        name=graphene.String(),
        owner=graphene.String(),
    )

    # here we pass the resource from which graphene will get raw information about repository, using Rest API:
    def resolve_repo(_, info, args):
        repo_info = requests.get(f'https://api.github.com/repos/{args("owner")}/{args("name")}')
        return json2obj(repo_info)


# This is what I would do to execute a query using graphene without passing url:
schema = graphene.Schema(query=Query)
# This will give me no result because I don't make a request to a server:
res = schema.execute('{ repository { name } }', context_value={"name": "Lv-323python", "owner": "learnRepo"})
print(res.data, res.errors)

# I need to pass a url and token, so I use gql:
client = Client(transport=RequestsHTTPTransport(url='https://api.github.com/graphql',
                                                headers={
                                                    'Authorization': 'token ...'}, use_json=True), schema=schema)  # pass your token here
# Testing a simple query:
query = gql(
    """
   { repository(owner: \"Lv-323python\", name: \"learnRepo\") { name } }
    """)
client.execute(query)



# Pleace check out if this is a right way to use graphene and gql while geting data from githubapi (Graphql)
# This is a working query I send to Postman, as it is:
postman_query = {
    "query": "query { repository(owner: \"Lv-323python\", name: \"learnRepo\") { repo_name:name creation_date:createdAt owner{login} url: url} }"}
