import tempfile
import unittest
import json
from entities.sources import PriceSource
from entities.sources import GenericSource
from repositories import Database


class TestPriceSource(unittest.TestCase):
    def test_source(self):
        data = [
            {
                "Rank": 23,
                "DateTime": "2022-12-26T19:00:00+02:00",
                "PriceNoTax": 1.0,
                "PriceWithTax": 1.22,
            }
        ]
        db = Database()
        source = PriceSource(db, data=data)
        source.update()
        print(db.get_records())
        self.assertEqual(1.0, db.get_record("2022-12-26 17:00:00").get_price())


class TestGenericSource(unittest.TestCase):
    def test_source(self):
        db = Database()
        data = [
            {"time": "2022-12-21 22:00:00", "price": 1.0, "amount": 2.0},
        ]
        tf = tempfile.TemporaryFile()
        tf.write(json.dumps(data).encode("utf-8"))
        tf.seek(0)
        source = GenericSource(db, local_file=tf.name)
        source.update()
        self.assertEqual(1.0, db.get_record("2022-12-21 22:00:00").get_price())
