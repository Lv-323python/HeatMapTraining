"""
This module contains helper functions for data plotting structuring
"""

# import datetime
import pandas as pd


class CommitsHeatmap:
    """
    CommitsHeatmap class
    """
    def __init__(self, commits, start_date, end_date=pd.Timestamp.utcnow(), date_unit='D'):
        """
        Constructor

        :param commits: list
        :param start_date: pd.Timestamp
        :param date_unit: str
        :param time_delta: pd.Timestamp
        """
        self.commits = commits
        self.start_date = start_date
        self.date_unit = date_unit
        self.end_date = end_date

    def get_data_dict(self):
        """
        Returns dict with data for plotting

        :return: dict
        """

        print('---------repo creation date------------------')
        print('start date', self.start_date)
        print('---------------------------------------------')
        print('------Commits----------')
        print(self.commits)
        print('--------------------------------------------')

        df = pd.DataFrame.from_records(self.commits)
        df.date = pd.to_datetime(df.date, utc=True, unit='s')
        df.set_index('date', inplace=True)
        df.index = df.index.floor('D')

        date_range = pd.date_range(start=self.start_date, end=self.end_date, freq=self.date_unit)
        date_range = date_range.floor('D')

        grouped = df.groupby('author')
        new_df = pd.DataFrame(index=date_range)
        for name, group in grouped:
            new_df[name] = group.groupby('date').size()
        new_df.fillna(0, inplace=True)

        return {
            'x': new_df.index.strftime('%Y-%m-%d').tolist(),
            'y': new_df.columns.tolist(),
            'z': new_df.T.values.astype('int32').tolist()
        }

    @classmethod
    def from_repository_doc(cls, repository_document, date_unit='D'):
        """
        Create CommitsHeatmap instance from mongo document

        :param repository_document:
        :param date_unit:
        :return:
        """
        repository_info = repository_document['value']
        commits = repository_info['commits']['data']
        start_date_utc = min(repository_info['repo']['creation_date'], commits[-1]['date'])
        start_date = pd.to_datetime(start_date_utc, utc=True, unit='s')

        return cls(commits, start_date, date_unit=date_unit)
