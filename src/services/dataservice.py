import os
import csv
import warnings
import json
import datetime
import requests
import dateutil.parser

from repositories import Database
from entities import Record, Selection


def update_from_spot_hinta(database):
    price_updated, amount_updated = (0, 0)
    rows = requests.get(
        "https://api.spot-hinta.fi/TodayAndDayForward", timeout=10
    ).json()
    for row in rows:
        time = dateutil.parser.parse(row["DateTime"])
        price = row["PriceNoTax"]
        record = Record(time, price=price)
        price, amount = database.add_or_update_record(record)
        price_updated += price
        amount_updated += amount
    return (price_updated, amount_updated)


def update_from_datahub(database, local_file="data/consumption.csv"):
    price_updated, amount_updated = (0, 0)
    if not os.path.exists(local_file):
        warnings.warn(f"consumption file {local_file} not found, unable to update!")
    else:
        with open(local_file, "r", encoding="utf8") as csvfile:
            reader = csv.DictReader(csvfile, delimiter=";")
            for row in reader:
                time = dateutil.parser.parse(row["Alkuaika"])
                amount = float(row["Määrä"])
                record = Record(time, amount=amount)
                price, amount = database.add_or_update_record(record)
                price_updated += price
                amount_updated += amount
    return (price_updated, amount_updated)


def update_from_json(database, local_file="data/generic_json.json"):
    price_updated, amount_updated = (0, 0)
    if not os.path.exists(local_file):
        warnings.warn(f"json file {local_file} not found, unable to update!")
    else:
        with open(local_file, "r", encoding="utf-8") as file:
            rows = json.load(file)
            for row in rows:
                record = Record(row["time"], price=row["price"], amount=row["amount"])
                price, amount = database.add_or_update_record(record)
                price_updated += price
                amount_updated += amount
    return (price_updated, amount_updated)


class DataService:
    def __init__(self, db=None, config=config):
        self._db = db or Database()
        self._config = config
        self._sources = {
            "spot-hinta.fi": update_from_spot_hinta,
            "datahub": update_from_datahub,
            "json": update_from_json,
        }

    def save_db(self, dbfile=None):
        """Save database to disk in a csv file format.

        Args:
            dbfile, optional: file name of database

        Returns:
            Nothing.
        """
        with open(dbfile or config.DB_FILE, "w", encoding="utf-8") as out:
            self._db.write_csv(out)

    def load_db(self, dbfile=None):
        """Read database from disk.

        Args:
            dbfile, optional: file name of the database

        Return:
            Nothing.

        Notes:
            Removes all existing data before loading.
        """
        self._db.clear()
        with open(dbfile or config.DB_FILE, "r", encoding="utf-8") as input:
            self._db.read_csv(input)

    def add_source(self, source, source_func):
        """Add new source to update database."""
        self._sources[source] = source_func

    def update_db(self, source, *args, **kwargs):
        """Update database from a source.

        Args:
            source: a string identifying source.

        Raises:
            KeyError, if source is not "registered".

        Notes:
            This method passes any extra arguments and keywords to a function
            which is identified by `source`.
        """
        if source not in self._sources:
            raise KeyError(f"Unable to update using source {source}: unknown source")
        return self._sources[source](self._db, *args, **kwargs)

    def get_data_as_dataframe(self):
        return self._db.to_dataframe()

    def get_future_prices(self):
        now = datetime.datetime.utcnow()
        records = self._db.filter_by_time(start=now).get_records()
        return list(filter(lambda r: r.has_price(), records.values()))

    def find_cheapest_hours(self, hours=3, order="time"):
        """Find N cheapest hours from future prices.

        Args:
            order (str): 'time' or 'price'
        """
        now = datetime.datetime.utcnow()
        records = self._db.filter_by_time(start=now, end=None).get_records()
        # sorted by price
        keys = sorted(records, key=lambda r: records[r].get_price())
        keys = keys[0:hours]
        if order == "time":
            # sorted by time
            keys = sorted(keys)
        selection = Selection()
        for start in keys:
            end = start + datetime.timedelta(hours=1)
            selection.add_timerange(start, end)
        return selection

    def get_record(self, time):
        """Return a record from database."""
        return self._db.get_record(time)
