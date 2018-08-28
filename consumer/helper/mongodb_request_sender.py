"""
    Provides class MongoDBRequestSender
"""
import time
import datetime
import pymongo
import pymongo.errors

from pymongo import MongoClient

MONGO_HOST = 'heatmaptraining_mongo_1'
MONGO_PORT = 27017


class MongoDBRequestSender:
    """
    Provides interface for hashing and sending requests
    to MongoDB database
    """

    def __init__(self):
        retries = 30
        while True:
            try:
                # declare connection
                self.client = MongoClient(MONGO_HOST, MONGO_PORT)
                print(self.client.server_info())
                break
            except pymongo.errors.ServerSelectionTimeoutError as err:
                if retries == 0:
                    print('Failed to connect MongoDB!')
                    raise err
                retries -= 1
                time.sleep(1)
        print('Successfully connected MongoDB!')
        self.database = self.client.project_database
        self.hash_collection = self.database.hash_collection
        # self.hash_collection.drop()
        self.hash_collection.ensure_index("date", expireAfterSeconds=3600)

    def get_entry(self, body):
        """
        Tries to find response in hash collection in Redis database
        :param body:
        :return:
        """
        assert isinstance(body, dict), 'MongoDBRequestSender: Inputted "body" type is not dict'
        key = '-'.join(body.values())
        try:
            print("MongoDBRequestSender.get_entry: Trying to find in Mongo : " + str(key))
            mongo_response = self.hash_collection.find_one({"key": key})
            print(mongo_response)
            return pymongo.get('value')
        except AttributeError:
            print("Can't find this entry in Mongo or maybe you have problems with MongoDB")
            return None
        except pymongo.errors.PyMongoError as err:
            print(
                "MongoDBRequestSender.get_entry: problems with MongoDB")
            print(err)
            return None

    def set_entry(self, body, response):
        """
        Adds hash of the request to MongoDB database
        :param body:
        :param response:
        :return:
        """
        assert isinstance(body, dict), 'Inputted "body" type is not dict'
        key = '-'.join(body.values())
        utc_timestamp = datetime.datetime.utcnow()
        try:
            print("MongoDBRequestSender.set_entry: Inserted into MongoDB hash_id:")
            print(self.hash_collection.insert_one({"key": key,
                                                   "value": response,
                                                   "date": utc_timestamp}).inserted_id)
        except pymongo.errors.PyMongoError as err:
            print("MongoDBRequestSender.set_entry: Problems with MongoDB")
            print(err)
