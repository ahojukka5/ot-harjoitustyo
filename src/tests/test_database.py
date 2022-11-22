import unittest
from saehaekkae import Database, Record


class TestDatabase(unittest.TestCase):
    def test_database(self):
        db = Database()
        record = Record(0, 20.0)
        db.add_record(record)
        records = db.get_records()
        first_record = records[0]
        self.assertEqual(record, first_record)
