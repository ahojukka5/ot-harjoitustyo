import datetime

from repositories import Database
from entities import Selection, PriceSource, ConsumptionSource, GenericSource


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
