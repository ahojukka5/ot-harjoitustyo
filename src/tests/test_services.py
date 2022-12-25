import unittest
from services import DateTimePicker
from services import DataService
from repositories import Database
from entities import Record


class TestDateTimePicker(unittest.TestCase):
    def test_pick(self):
        p = DateTimePicker()
        p.pick("2022-12-18 13:00")
        p.pick_between("2022-12-18 18:00", "2022-12-18 18:45")
        selection = p.to_selection()
        self.assertTrue("2022-12-18 13:00" in selection)
        self.assertTrue("2022-12-18 14:00" not in selection)
        self.assertTrue("2022-12-18 18:30" in selection)
        self.assertTrue("2022-12-18 19:00" not in selection)


class TestDataService(unittest.TestCase):
    def test_find_cheapest_hours(self):
        r1 = Record("2022-12-25 20:00", price=1.0)
        r2 = Record("2022-12-25 21:00", price=1.0)
        r3 = Record("2022-12-25 22:00", price=2.0)
        db = Database()
        db.add_record(r1)
        db.add_record(r2)
        db.add_record(r3)
        ds = DataService(database=db)
        selection = ds.find_cheapest_hours(2)
        self.assertEqual(
            "2022-12-25T20:00:00+00:00 - 2022-12-25T22:00:00+00:00", str(selection)
        )
