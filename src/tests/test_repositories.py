import unittest
import math
import io
from dateutil import parser
from entities import Record
from repositories import Database

import pandas as pd


class TestDatabase(unittest.TestCase):
    def test_database(self):
        db = Database()
        record = Record("2022-12-16 21:00:00", 20.0, 3.0)
        db.add_record(record)
        records = list(db.get_records().values())
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

    def test_from_dataframe(self):
        t1 = parser.parse("2022-12-16T15:00:00")
        t2 = parser.parse("2022-12-16T16:00:00")
        df = pd.DataFrame({"price": [1, 2], "amount": [3, 4]}, index=[t1, t2])
        db = Database()
        db.from_dataframe(df)
        recs = list(db.get_records().values())
        self.assertEqual(1.0, recs[0].get_price())

    def test_add_or_update_record(self):
        db = Database()
        record = Record("2022-12-16 21:00:00", price=20.0, amount=3.0)
        db.add_record(record)
        record = Record("2022-12-16 21:00:00", amount=4.0)
        with self.assertRaises(KeyError):
            db.add_record(record)
        db.add_or_update_record(record)
        records = list(db.get_records().values())
        self.assertEqual(1, len(records))
        self.assertEqual(20.0, records[0].get_price())
        self.assertEqual(4.0, records[0].get_amount())

    def test_read_db(self):
        data = (
            "time,price,amount\n"
            "2022-12-16T21:00:00+00:00,20.0000,3.0000\n"
            "2022-12-16T22:00:00+00:00,nan,4.0000\n"
        )
        db = Database()
        db.read_csv(io.StringIO(data))
        records = list(db.get_records().values())
        self.assertEqual(2, len(records))
        self.assertEqual(20.0, records[0].get_price())
        self.assertEqual(3.0, records[0].get_amount())
        print(type(records[1].get_price()))
        self.assertTrue(math.isnan(records[1].get_price()))
        self.assertEqual(4.0, records[1].get_amount())

    def test_write_db(self):
        db = Database()
        record = Record("2022-12-16 22:00:00", amount=4.0)
        db.add_record(record)
        record = Record("2022-12-16 21:00:00", price=20.0, amount=3.0)
        db.add_record(record)
        out = io.StringIO()
        db.write_csv(out)
        out.seek(0)
        print(out.read())
        out.seek(0)
        expected = (
            "time,price,amount\n"
            "2022-12-16T21:00:00+00:00,20.0000,3.0000\n"
            "2022-12-16T22:00:00+00:00,nan,4.0000\n"
        )
        self.assertEqual(expected, out.read())

    def test_filter_by_time(self):
        db = Database()
        db.add_record(Record("2022-12-19 10:00:00"))
        db.add_record(Record("2022-12-19 11:00:00"))
        db.add_record(Record("2022-12-19 12:00:00"))
        records = db.filter_by_time(start="2022-12-19 10:30:00").get_records()
        self.assertEqual(2, len(records))
