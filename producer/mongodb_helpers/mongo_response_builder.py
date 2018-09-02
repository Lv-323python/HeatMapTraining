"""
    Provides class MongoResponseBuilder
"""
import time
import datetime
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
            if git_info['form_of_date'] == HEAT_CHOICES[0]:  # pylint: disable=R1705
                grouped = dataf.groupby(['author', 'date']) \
                    .size().reset_index(name='counts').groupby('author')['date', 'counts'] \
                    .apply(lambda x: x.to_dict('records')).to_dict()
                return self.build_heat_with_hours(grouped)
            elif git_info['form_of_date'] == HEAT_CHOICES[1]:
                dataf['date'] = pd.to_datetime(dataf['date'], unit='s') \
                    .apply(lambda x: str(x.weekday()))
                grouped = dataf.groupby(['author', 'date']) \
                    .size().reset_index(name='counts').groupby('author')['date', 'counts'] \
                    .apply(lambda x: x.to_dict('records')).to_dict()
                return self.build_heat_with_weekdays(grouped)
            dataf['date'] = pd.to_datetime(dataf['date'], unit='s') \
                .apply(lambda x: str(x.hour))
            dataf['date'] = pd.to_datetime(dataf['date'], unit='s') \
                .apply(lambda x: x.date())
            grouped = dataf.groupby(['author', 'date']) \
                .size().reset_index(name='counts').groupby('author')['date', 'counts'] \
                .apply(lambda x: x.to_dict('records')).to_dict()
            return self.build_heat_with_dates(grouped)
        return None

    def build_heat_with_hours(self, grouped):
        """

        :param grouped:
        :return:
        """
        names = list(grouped.keys())
        dates = list(range(0, 24))
        counts = []
        for name in names:
            data_set = grouped[name]
            list_of_counts = [0] * 24
            for entry in data_set:
                list_of_counts[int(entry['date'])] = entry['counts']
            print(list_of_counts)
            counts.append(list_of_counts)
        print(dates)
        print(self)
        return {'x': dates, 'y': names, 'z': counts}

    def build_heat_with_weekdays(self, grouped):
        """

        :param grouped:
        :return:
        """
        names = list(grouped.keys())
        dates = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sanday']
        counts = []
        for name in names:
            data_set = grouped[name]
            list_of_counts = [0] * 7
            for entry in data_set:
                list_of_counts[int(entry['date'])] = entry['counts']
            print(list_of_counts)
            counts.append(list_of_counts)
        print(counts)
        print(self)
        return {'x': dates, 'y': names, 'z': counts}

    def build_heat_with_dates(self, grouped):
        """

        :param grouped:
        :return:
        """
        names = list(grouped.keys())
        seq = [x['date'] for name in grouped.keys() for x in grouped[name]]
        dates = list()

        def daterange(date1, date2):
            """

            :param date1:
            :param date2:
            :return:
            """
            for number_of_days in range(int((date2 - date1).days) + 1):
                yield date1 + datetime.timedelta(number_of_days)

        for date in daterange(min(seq), max(seq)):
            dates.append(date.strftime("%Y-%m-%d"))

        print(dates)
        counts = []
        for name in names:
            data_set = grouped[name]
            list_of_counts = [0] * len(dates)
            for entry in data_set:
                list_of_counts[dates.index(entry['date'].strftime("%Y-%m-%d"))] = entry['counts']
            print(list_of_counts)
            counts.append(list_of_counts)
        print(counts)
        print(self)
        return {'x': dates, 'y': names, 'z': counts}
