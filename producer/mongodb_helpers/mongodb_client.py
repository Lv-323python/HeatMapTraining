"""
    Provides class MongoResponseBuilder
"""

from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

from mongodb_helpers.mongodb_client_config import MONGO_PORT, MONGO_HOST


class MongoDBClient:
    """
    Provides interface for hashing and sending requests
    to MongoDB database
    """

    def __init__(self, base_client=MongoClient, host=MONGO_HOST, port=MONGO_PORT):

        # declare connection
        self._client = base_client(host, port)
        print('connecting to mongo')
        # connects to mongo for 30 seconds
        try:
            # The ismaster command is cheap and does not require auth.
            self._client.admin.command('ismaster')
        except ConnectionFailure:
            print("Server not available")

        print('Successfully connected MongoDB!')

        self._database = self._client.heatmap_db
        self._collection = self._database.repos_collection

    def get_entry(self, key):
        """
        Tries to find response in repos collection

        :param key: str
        :return: None or document from mongo
        """
        assert isinstance(key, str), 'MongoDBClient.get_entry(key): key is not of type str'
        print('Looking for document with key: ', key)

        return self._collection.find_one({"key": key})

