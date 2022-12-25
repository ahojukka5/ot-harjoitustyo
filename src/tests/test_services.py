import unittest
from dateutil import parser
from services import DateTimePicker


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
