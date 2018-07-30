import json
from collections import namedtuple
import graphene
import requests
from heat_map_training.request_sender.github_request_sender_base import \
    GithubRequestSenderBase


def request_post(param, base_url, headers):
    query_body = {'query': param}
    response = requests.post(url=base_url,
                             json=query_body,
                             headers=headers)
    return response.json()


def request_get(url):
    response = requests.get(url=url, headers={'Authorization': '97f896b3656a56ab6f8c647d6c63ee53279ff1e1'})
    return response.json()


def _json_object_hook(d):
    return namedtuple('X', d.keys())(*d.values())


def json2obj(data):
    return json.loads(data, object_hook=_json_object_hook)


class GithubRequestSenderV4(GithubRequestSenderBase):
    def __init__(self, owner, repo, token, query=True, base_url='https://api.github.com/graphql'):
        """
        Github api requests class based on GraphQl

        :rtype: object
        :param token: github api token string
        """
        GithubRequestSenderBase.__init__(self,
                                         base_url=base_url,
                                         owner=owner,
                                         repo=repo,
                                         query=query,
                                         token=token)
        self.base_url = base_url


class Repository(graphene.ObjectType):
    name = graphene.String(required=True)
    created_at = graphene.DateTime(required=True)
    owner = graphene.String(required=True)
    url = graphene.String(required=True)


def get_repo(name):
    return Repository(name=name)


class Query(graphene.ObjectType):
    repository = graphene.Field(
        Repository,
        id=graphene.ID(),
        name=graphene.String(),
        owner=graphene.String(),
    )

    def resolve_repo(_, info, args):
        repo_info = request_get(f'https://api.github.com/repos/{args("owner")}/{args("name")}')
        return json2obj(repo_info)


SCHEMA = graphene.Schema(query=Query)
RES = SCHEMA.execute("{ repository { name } }", variable_values={"owner": "Lv-323python", "name": "learnRepo"})

print(RES.data)
print(RES.errors)
