import unittest
from datetime import datetime
import pytz
from entities import Record
from entities import Selection
from entities import ShellyMessage
from entities import GoogleMessage


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


class TestSelection(unittest.TestCase):
    def test_constructor(self):
        s = Selection()
        s.add_timerange("2022-12-19 15:00", "2022-12-19 16:00")
        s.add_timerange("2022-12-19 17:00", "2022-12-19 18:00")
        end2 = datetime(2022, 12, 19, 18, 0, 0).astimezone()
        self.assertEqual(end2, s["2022-12-19 17:00"].end)

    def test_pack(self):
        s = Selection()
        s.add_timerange("2022-12-24 12:00", "2022-12-24 13:00")
        s.add_timerange("2022-12-24 13:00", "2022-12-24 14:00")
        timeranges = s.get_timeranges(pack=True)
        start = datetime(2022, 12, 24, 12, 0, 0).astimezone()
        end = datetime(2022, 12, 24, 14, 0, 0).astimezone()
        self.assertEqual(end, timeranges[start].end)

    def test_is_selected(self):
        selection = Selection()
        selection.add_timerange("2022-12-24 12:00", "2022-12-24 13:00")
        self.assertTrue("2022-12-24 12:30" in selection)
        self.assertFalse("2022-12-24 13:30" in selection)


class TestShellyMessage(unittest.TestCase):
    def test_message(self):
        selection = Selection()
        selection.add_timerange("2022-12-24 18:00", "2022-12-24 19:00")
        selection.add_timerange("2022-12-24 20:00", "2022-12-24 21:00")
        relays = [1]
        msg = ShellyMessage(selection, relays)
        expected = [
            {
                "enable": True,
                "timespec": "10 0 18 24 12 SAT",
                "calls": [{"method": "Switch.Set", "params": {"id": 1, "on": True}}],
            },
            {
                "enable": True,
                "timespec": "10 0 19 24 12 SAT",
                "calls": [{"method": "Switch.Set", "params": {"id": 1, "on": False}}],
            },
            {
                "enable": True,
                "timespec": "10 0 20 24 12 SAT",
                "calls": [{"method": "Switch.Set", "params": {"id": 1, "on": True}}],
            },
            {
                "enable": True,
                "timespec": "10 0 21 24 12 SAT",
                "calls": [{"method": "Switch.Set", "params": {"id": 1, "on": False}}],
            },
        ]
        self.assertEqual(expected, msg.get_payloads())


class TestGoogleMessage(unittest.TestCase):
    def test_message(self):
        selection = Selection()
        selection.add_timerange("2022-12-24 18:00", "2022-12-24 19:00")
        msg = GoogleMessage(selection, summary="testing")
        expected = [
            {
                "summary": "testing",
                "start": {
                    "dateTime": "2022-12-24T18:00:00",
                    "timeZone": "Europe/Helsinki",
                },
                "end": {
                    "dateTime": "2022-12-24T19:00:00",
                    "timeZone": "Europe/Helsinki",
                },
                "reminders": {
                    "useDefault": False,
                    "overrides": [{"method": "popup", "minutes": 5}],
                },
            }
        ]
        print(msg)
        self.assertEqual(expected, msg.get_payloads())
