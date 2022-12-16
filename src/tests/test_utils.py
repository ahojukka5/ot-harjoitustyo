import unittest
from dateutil import parser
from saehaekkae import Record, Database, get_cheapest_hour


class TestUtils(unittest.TestCase):
    def setUp(self):
        self.database = Database()
        time1 = parser.parse("2022-12-16T20:00:00")
        time2 = parser.parse("2022-12-16T21:00:00")
        self.record1 = record1 = Record(time1, price=10.0, amount=3.0)
        self.record2 = record2 = Record(time2, price=20.0, amount=1.0)
        self.database.add_record(record1)
        self.database.add_record(record2)

    def test_get_cheapest_hour(self):
        cheapest = get_cheapest_hour(self.database)
        assert cheapest is not None
        self.assertEqual(cheapest, self.record1)
