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
    """Update price data from api.spot-hinta.fi."""
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
    """Update consumption data from a csv file downloaded from oma.datahub.fi."""
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
    """Update price/consumption data from generic json file."""
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
    """DataService allows access to price and consumption data.

    Data is collected from various of sources and stores in a csv database to
    disk.

    Typical usage example
    >>> ds = DataService()
    >>> ds.load_db("db.csv")
    >>> ds.update_db(source="spot-hinta.fi")
    >>> ds.save_db("db.csv")
    >>> selection1 = ds.find_cheapest_hours(hours=3, order="time")
    >>> print(selection)
    ...

    """

    def __init__(self, database=None):
        self._db = database or Database()
        self._sources = {
            "spot-hinta.fi": update_from_spot_hinta,
            "datahub": update_from_datahub,
            "json": update_from_json,
        }

    def save_db(self, dbfile):
        """Save database to disk in a csv file format.

        Args:
            dbfile: file name of database

        Returns:
            Nothing.
        """
        with open(dbfile, "w", encoding="utf-8") as out:
            self._db.write_csv(out)

    def load_db(self, dbfile):
        """Read database from disk.

        Args:
            dbfile: file name of the database

        Return:
            Nothing.

        Notes:
            Removes all existing data before loading.
        """
        self._db.clear()
        with open(dbfile, "r", encoding="utf-8") as file:
            self._db.read_csv(file)

    def add_source(self, source, source_func):
        """Add new source to update database.

        Args:
            source (str): name of the source
            source_func: a function that takes a database instance as a first argument

        Returns:
            Nothing.
        """
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
        """Return the whole database as a Pandas DataFrame for a serious data analysis."""
        return self._db.to_dataframe()

    def get_future_prices(self):
        """Return all records from a database which are newer than current time.

        Args:
            Nothing.

        Returns:
            A list of Record objects.
        """
        now = datetime.datetime.utcnow()
        records = self._db.filter_by_time(start=now).get_records()
        return list(filter(lambda r: r.has_price(), records.values()))

    def find_cheapest_hours(self, hours=3, order="time"):
        """Find N cheapest hours from future prices.

        Args:
            order (str): 'time' or 'price'

        Returns:
            A Selection object containing N cheapest hours.
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
