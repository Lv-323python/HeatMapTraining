"""
    Provides class MongoResponseBuilder
"""
import datetime
import pandas as pd


from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

from mongodb_helpers.mongo_config import MONGO_PORT, MONGO_HOST, HEAT_CHOICES


class MongoResponseBuilder:
    """
    Provides forming data from MongoDB database
    """

    def __init__(self):
        # declare connection
        self._client = MongoClient(MONGO_HOST, MONGO_PORT)
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

    def build_heat_dict(self, git_info):
        """
        Method used to build heat dict
        :param git_info:
        :return:
        """

        # pop date unit for plotting from git info
        date_unit = git_info.pop('date_unit')

        key = '-'.join(git_info.values())
        print("ROUTES.getheatdict():Trying to find " + key)

        # Returns a single document, or None if no matching document is found

        # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        response= self._collection.find_one({"key": key})
        mongo_response = None
        start_date_utc = None
        if response:
            mongo_response = response['value']['commits']
            start_date_utc = response['value']['repo']['creation_date']
        print('---------repo creation date------------------')
        print(start_date_utc)
        print('---------------------------------------------')
        # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!


        print('------Response received from mongo----------')
        print(mongo_response)
        print('--------------------------------------------')



        if mongo_response:
            df = pd.DataFrame.from_records(mongo_response)
            df.date = pd.to_datetime(df.date, utc=True, unit='s')
            df.set_index('date', inplace=True)
            df.index = df.index.floor('D')
            start_date = pd.to_datetime(start_date_utc, utc=True, unit='s')  #  1530620138
            end_date = pd.Timestamp.utcnow()

            date_range = pd.date_range(start=start_date, end=end_date, freq='D')
            date_range = date_range.floor('D')
            new_df = pd.DataFrame(index=date_range)
            # generate date range in days from repo creation date till now
            # (including repo creation day and today)
            grouped = df.groupby('author')
            for name, group in grouped:
                new_df[name] = group.groupby('date').size()
            new_df.fillna(0, inplace=True)

            return {
                'x': new_df.index.strftime('%Y-%m-%d').tolist(),
                'y': new_df.columns.tolist(),
                'z': new_df.T.values.astype('int32').tolist()
            }
        # generate date range in days from repo creation date till now
        # (including repo creation day and today)



        # if mongo_response:
        #     dataf = pd.DataFrame(mongo_response)
        #     if git_info['form_of_date'] == HEAT_CHOICES[0]:  # pylint: disable=R1705
        #         grouped = dataf.groupby(['author', 'date']) \
        #             .size().reset_index(name='counts').groupby('author')['date', 'counts'] \
        #             .apply(lambda x: x.to_dict('records')).to_dict()
        #         return self.build_heat_with_hours(grouped)
        #     elif git_info['form_of_date'] == HEAT_CHOICES[1]:
        #         dataf['date'] = pd.to_datetime(dataf['date'], unit='s') \
        #             .apply(lambda x: str(x.weekday()))
        #         grouped = dataf.groupby(['author', 'date']) \
        #             .size().reset_index(name='counts').groupby('author')['date', 'counts'] \
        #             .apply(lambda x: x.to_dict('records')).to_dict()
        #         return self.build_heat_with_weekdays(grouped)
        #     dataf['date'] = pd.to_datetime(dataf['date'], unit='s') \
        #         .apply(lambda x: str(x.hour))
        #     dataf['date'] = pd.to_datetime(dataf['date'], unit='s') \
        #         .apply(lambda x: x.date())
        #     grouped = dataf.groupby(['author', 'date']) \
        #         .size().reset_index(name='counts').groupby('author')['date', 'counts'] \
        #         .apply(lambda x: x.to_dict('records')).to_dict()
        #     return self.build_heat_with_dates(grouped)
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
