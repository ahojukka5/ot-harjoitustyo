import pandas as pd


class Database:
    def __init__(self):
        self.records = []

    def add_record(self, record):
        self.records.append(record)

    def get_records(self):
        return self.records

    def to_dataframe(self):
        data = [record.to_dict() for record in self.get_records()]
        dataframe = pd.DataFrame(data)
        dataframe.index = dataframe["time"]
        del dataframe["time"]
        return dataframe
