import unittest
from saehaekkae import Record


class TestRecord(unittest.TestCase):
    def test_record_getters(self):
        record = Record(3, 20.0)
        self.assertEqual(3, record.get_time())
        self.assertEqual(20.0, record.get_energy_price())
