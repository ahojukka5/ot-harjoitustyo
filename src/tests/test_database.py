import unittest
from dateutil import parser
from saehaekkae import Database, Record

import pandas as pd


class TestDatabase(unittest.TestCase):
    def test_database(self):
        db = Database()
        record = Record("2022-12-16 21:00:00", 20.0, 3.0)
        db.add_record(record)
        records = db.get_records()
        first_record = records[0]
        self.assertEqual(record, first_record)

    def test_to_dataframe(self):
        db = Database()
        db.add_record(Record("2022-11-28T00:00:00", 10.0))
        db.add_record(Record("2022-11-28T01:00:00", 20.0))
        df = db.to_dataframe()
        print(df)
        row1 = df.iloc[0]
        row2 = df.iloc[1]
        self.assertEqual(2, len(df))
        self.assertEqual(10.0, row1["price"])
        print("type of row2.name is ", type(row2.name))
        self.assertEqual(pd.Timestamp("2022-11-28T01:00:00Z"), row2.name)
