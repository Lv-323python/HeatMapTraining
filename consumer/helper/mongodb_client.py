"""
    Provides class MongoDBRequestSender
"""
from pymongo.errors import ConnectionFailure

from pymongo import MongoClient
from helper.mongo_client_config import MONGO_HOST, MONGO_PORT


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

        return self._collection.find_one({"key": key})


    def set_entry(self, key, entry):
        """
        Adds hash of the request to MongoDB database
        :param body:
        :param response:
        :return:
        """
        assert isinstance(key, str), 'MongoDBClient.set_entry(key, entry): key is not of type str'
        assert isinstance(entry, dict), 'MongoDBClient.set_entry(key, entry): entry is not of type dict'
        print()
        print('inserting into collections with key :')
        print(key)
        print()

        print("Inserted successfully with id:")
        print(
            self._collection.insert_one(
                {
                    "key": key,
                    "value": entry
                }
            ).inserted_id
        )
