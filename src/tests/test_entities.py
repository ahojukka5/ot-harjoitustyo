import unittest
import pytz
from datetime import datetime
from saehaekkae import Record


class TestRecord(unittest.TestCase):
    def setUp(self):
        self.record = Record("2022-12-16T21:00:00Z", price=10.0, amount=3.0)

    def test_record_constructor(self):
        record1 = Record(1671224400, price=10.0, amount=3.0)
        record2 = Record("2022-12-16T21:00:00Z", price=10.0, amount=3.0)
        record3 = Record(datetime(2022, 12, 16, 21, 0, 0), price=10.0, amount=3.0)
        print(record1)
        print(record2)
        print(record3)
        self.assertEqual(record1, record2)
        self.assertEqual(record2, record3)

    def test_record_getters(self):
        record = self.record
        self.assertEqual(
            datetime(2022, 12, 16, 21, 0, 0, tzinfo=pytz.UTC), record.get_time()
        )
        self.assertEqual(10.0, record.get_price())
        self.assertEqual(3.0, record.get_amount())

    def test_update(self):
        record = self.record
        record.update(price=5.0)
        self.assertEqual(5.0, record.get_price())

    def test_to_json(self):
        expected = (
            """{"time": "2022-12-16T21:00:00+00:00", "price": 10.0, "amount": 3.0}"""
        )
        json = self.record.to_json()
        self.assertEqual(expected, json)