import os
import csv
import warnings
import json
import datetime
import requests
import dateutil.parser

from repositories import Database
from entities import Record, Selection


class AbstractSource:
    """Abstract Source class."""

    def update(self):
        """Update prices or consumptions from source X."""
        raise NotImplementedError("Implement this method.")


class PriceSource(AbstractSource):
    """Update price data from spot-hinta.fi"""

    url = "https://api.spot-hinta.fi/TodayAndDayForward"

    def __init__(self, database):
        self._db = database
        self.price_updated = 0
        self.consumption_updated = 0

    def update(self):
        """Update price data."""
        rows = requests.get(PriceSource.url, timeout=10).json()
        for row in rows:
            time = dateutil.parser.parse(row["DateTime"])
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
            "spot-hinta.fi": PriceSource,
            "datahub": ConsumptionSource,
            "json": GenericSource,
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

    def add_source(self, source, source_class):
        """Add new source to update database.

        Args:
            source (str): name of the source
            source_class: a class that inherits AbstractSource and implements `update`

        Returns:
            Nothing.
        """
        self._sources[source] = source_class

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
        source = self._sources[source](self._db, *args, **kwargs)
        return source.update()

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
