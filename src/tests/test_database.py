import unittest
from saehaekkae import Database, Record

import pandas as pd


class TestDatabase(unittest.TestCase):
    def test_database(self):
        db = Database()
        record = Record(0, 20.0)
        db.add_record(record)
        records = db.get_records()
        first_record = records[0]
        self.assertEqual(record, first_record)

    def test_to_dataframe(self):
        db = Database()
        db.add_record(Record(pd.to_datetime("2022-11-28T00:00:00"), 10.0))
        db.add_record(Record(pd.to_datetime("2022-11-28T01:00:00"), 20.0))
        df = db.to_dataframe()
        print(df)
        row1 = df.iloc[0]
        row2 = df.iloc[1]
        self.assertEqual(2, len(df))
        self.assertEqual(10.0, row1["energy_price"])
        self.assertEqual(pd.to_datetime("2022-11-28T01:00:00"), row2.name)
