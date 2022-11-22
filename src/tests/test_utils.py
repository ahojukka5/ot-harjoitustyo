import unittest
from saehaekkae import Record, Database, get_cheapest_hour


class TestUtils(unittest.TestCase):
    def setUp(self):
        self.database = Database()
        self.database.add_record(Record(0, 10.0))
        self.database.add_record(Record(1, 9.0))
        self.database.add_record(Record(2, 11.0))

    def test_get_cheapest_hour(self):
        cheapest = get_cheapest_hour(self.database)
        assert cheapest is not None
        self.assertEqual(cheapest.get_time(), 1)
        self.assertEqual(cheapest.get_energy_price(), 9.0)
