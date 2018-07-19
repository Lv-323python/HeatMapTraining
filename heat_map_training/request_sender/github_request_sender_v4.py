import requests
import json


class GithubRequestSenderV4:

    def __init__(self, token):
        self.token = token
        self.endpoint = 'https://api.github.com/graphql'
        self.headers = {'Authorization': f'Bearer {token}'}

    def query(self, query):
        assert isinstance(query, str)
        data = {'query': query}
        return requests.post(url=self.endpoint, data=json.dumps(data), headers=self.headers).json()


client = GithubRequestSenderV4("97f896b3656a56ab6f8c647d6c63ee53279ff1e1")
query1 = """
   {
        repository(owner:"octocat", name:"Hello-World") {
            issue(number:349) {
                id
             }
        }
  }"""

print(client.query(query1))
