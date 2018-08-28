"""
    Provides class MongoResponseBuilder
"""
import time
import pandas as pd
import pymongo
import pymongo.errors

from pymongo import MongoClient

from mongodb_helpers.mongo_config import MONGO_PORT, MONGO_HOST, HEAT_CHOICES


class MongoResponseBuilder:
    """
    Provides forming data from MongoDB database
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
        # print all in database
        # cursor = self.hash_collection.find({}, {"key": 1, "_id": 0})
        # for document in cursor: print(document)

    def build_heat_dict(self, git_info):
        """
        Method used to build heat dict
        :param git_info:
        :return:
        """
        pattern = F"{git_info['git_client']}-{git_info['token']}-" \
                  F".*-{git_info['repo']}-{git_info['owner']}-.*-.*-get_commits"
        try:
            print("ROUTES.getheatdict():Trying to find " + pattern)
            mongo_response = self.hash_collection \
                .find_one({"key": {'$regex': pattern, '$options': 's'}}).get('value')
            print(mongo_response)
        except AttributeError:
            print("MongoResponseBuilder.build_heat_dict:"
                  "Can't find this entry in Mongo or maybe you have problems with MongoDB")
            return None
        except pymongo.errors.PyMongoError as err:
            print("MongoResponseBuilder.build_heat_dict: problems with MongoDB")
            print(err)
            return None
        if mongo_response:
            dataf = pd.DataFrame(mongo_response)
            if git_info['form_of_date'] == HEAT_CHOICES[0]:
                dataf['date'] = pd.to_datetime(dataf['date'], unit='s') \
                    .apply(lambda x: str(x.hour))
            elif git_info['form_of_date'] == HEAT_CHOICES[1]:
                dataf['date'] = pd.to_datetime(dataf['date'], unit='s') \
                    .apply(lambda x: str(x.weekday()))
            else:
                dataf['date'] = pd.to_datetime(dataf['date'], unit='s') \
                    .apply(lambda x: x.date())
            grouped = dataf.groupby(['author', 'date']).size().reset_index(name='counts').groupby(
                'author')['date', 'counts'].apply(lambda x: x.to_dict('records')).to_dict()
            return grouped
        return None
