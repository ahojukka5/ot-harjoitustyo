import os
import csv
import json
from warnings import warn
import requests
import dateutil.parser
from entities import Record


class AbstractSource:
    """Abstract Source class."""

    def update(self):
        """Update prices or consumptions from source X."""
        raise NotImplementedError("Implement this method.")


class PriceSource(AbstractSource):
    """Update price data from spot-hinta.fi"""

    url = "https://api.spot-hinta.fi/TodayAndDayForward"

    def __init__(self, database, data=None):
        self._rows = data
        self._db = database
        self.price_updated = 0
        self.consumption_updated = 0

    def get_rows(self):
        if self._rows:
            return self._rows
        response = requests.get(PriceSource.url, timeout=10)
        if response.status_code != 200:
            warn("Unable to fetch prices from {url}: code {response.status_code}")
            return (self.price_updated, self.consumption_updated)
        return response.json()

    def update(self):
        """Update price data."""
        for row in self.get_rows():
            time = dateutil.parser.parse(row["DateTime"]).astimezone()
            price = row["PriceNoTax"]
            record = Record(time, price=price)
            price, amount = self._db.add_or_update_record(record)
            self.price_updated += price
            self.consumption_updated += amount
        return (self.price_updated, self.consumption_updated)


class ConsumptionSource(AbstractSource):
    """Update consumption data from a csv file downloaded from oma.datahub.fi."""

    def __init__(self, database, local_file):
        if not os.path.exists(local_file):
            warnings.warn(f"consumption file {local_file} not found, unable to update!")
            local_file = None
        self._db = database
        self._local_file = local_file
        self.price_updated = 0
        self.consumption_updated = 0

    def update(self):
        """Update consumption data."""
        if self._local_file is None:
            return (self.price_updated, self.consumption_updated)
        with open(self._local_file, "r", encoding="utf8") as csvfile:
            reader = csv.DictReader(csvfile, delimiter=";")
            for row in reader:
                time = dateutil.parser.parse(row["Alkuaika"])
                amount = float(row["Määrä"])
                record = Record(time, amount=amount)
                price, amount = self._db.add_or_update_record(record)
                self.price_updated += price
                self.consumption_updated += amount
        return (self.price_updated, self.consumption_updated)


class GenericSource(AbstractSource):
    """Update price/consumption data from generic json file."""

    def __init__(self, database, local_file):
        if not os.path.exists(local_file):
            warnings.warn(f"json file {local_file} not found, unable to update!")
            local_file = None
        self._db = database
        self._local_file = local_file
        self.price_updated = 0
        self.consumption_updated = 0

    def update(self):
        """Update price/consumption data."""
        if self._local_file is None:
            return (self.price_updated, self.consumption_updated)
        with open(self._local_file, "r", encoding="utf-8") as file:
            rows = json.load(file)
            for row in rows:
                record = Record(row["time"], price=row["price"], amount=row["amount"])
                price, amount = self._db.add_or_update_record(record)
                self.price_updated += price
                self.consumption_updated += amount
        return (self.price_updated, self.consumption_updated)
