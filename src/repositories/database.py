from collections import OrderedDict
import math
import csv
import dateutil.parser
from dateutil.tz import tzutc
import pandas as pd
from entities import Record


class Database:
    """Database to contain and manipulate records.

    The basic implementation of database adds functionality to manipulate a
    group of records. They can be added and exported to pandas DataFrame. Pandas
    can then be used to save/load database in various formats. This
    implementation uses csv file format for now, but basically it could also be
    easily replaced with SQL database or some other "real" data format.

    Typical usage example:

    >>> db = Database()
    >>> db.add_record(record1)
    >>> db.add_record(record2)
    >>> db.save("db.csv")

    Attributes:
        records: The list of records in database.
    """

    def __init__(self, records=None):
        """Construct a new Database object.

        Args:
            records (OrderedDict, optional): initial data

        Returns:
            A new Database object.
        """
        self._records = records or OrderedDict()

    def has_record(self, record):
        """Tests does record already exist in database.

        Args:
            record: a record object to test.

        Returns:
            boolean
        """
        return record.get_time() in self._records

    def add_record(self, record):
        """Add new record to database.

        Args:
            record: a Record object to add.

        Raises:
            KeyError, if a record with the same time already exists

        Returns:
            boolean tuple (has_price, has_amount)
        """
        if self.has_record(record):
            raise KeyError(f"Record {record.get_time()} already exists!")
        self._records[record.get_time()] = record
        return (record.has_price(), record.has_amount())

    def get_record(self, time):
        """Return a record from database.

        Args:
            time: string or datetime representing time.

        Raises:
            KeyError, if record not found.

        Returns:
            Record
        """
        if isinstance(time, str):
            time = dateutil.parser.parse(time)
        return self._records[time.replace(tzinfo=tzutc())]

    def update_record(self, record):
        """Update record to database.

        Args:
            record: a record to update.

        Raises:
            KeyError, if record with timestamp not found

        Returns:
            boolean tuple (price_updated, amount_updated)

        Notes:
            If record price/value contains float('nan'), it won't get updated.
        """
        if not self.has_record(record):
            raise KeyError(f"Record {record.get_time()} does not exist!")
        price = record.get_price()
        amount = record.get_amount()
        if math.isnan(price):
            price = None
        if math.isnan(amount):
            amount = None
        return self._records[record.get_time()].update(price=price, amount=amount)

    def add_or_update_record(self, record):
        """Add record to database. If exists, update.

        Args:
            record: a record to add or update.

        Returns:
            integer: 1 if data is updated, 0 otherwise
        """
        if self.has_record(record):
            return self.update_record(record)
        return self.add_record(record)

    def sort_records(self):
        """Sort records in-place.

        Args:
            Nothing.

        Returns:
            Nothing.
        """
        self._records = OrderedDict(sorted(self._records.items()))

    def get_records(self):
        """Get all records from the database as a sorted ordered dictionary.

        Args:
            Nothing.

        Returns:
            A list of records.
        """
        self.sort_records()
        return self._records

    def filter_by_time(self, start, end=None):
        """Filter records by time.

        Args:
            start (string or datetime)
            end (string or datetime, optional)

        Returns:
            A new database s.t. start <= records <= end
        """
        if isinstance(start, str):
            start = dateutil.parser.parse(start)
        if not start.tzinfo:
            start = start.replace(tzinfo=tzutc())
        if end is not None:
            if isinstance(end, str):
                end = dateutil.parser.parse(end)
            if not end.tzinfo:
                end = end.replace(tzinfo=tzutc())
        new_records = OrderedDict()
        for time in self._records:
            if (end is not None and start <= time <= end) or (start <= time):
                new_records[time] = self._records[time]
        return Database(new_records)

    def clear(self):
        """Removes all records from a database."""
        self._records = OrderedDict()

    def to_dataframe(self):
        """Export database to pandas Dataframe.

        Args:
            Nothing.

        Returns:
            Pandas DataFrame object.
        """
        index = []
        price = []
        amount = []
        for record in self.get_records().values():
            index.append(record.get_time())
            price.append(record.get_price())
            amount.append(record.get_amount())
        dataframe = pd.DataFrame({"price": price, "amount": amount}, index=index)
        dataframe.index.name = "time"
        return dataframe

    def from_dataframe(self, dataframe):
        """Import database from pandas Dataframe.

        Args:
            dataframe: Pandas DataFrame object.

        Returns:
            Nothing.
        """
        self.clear()
        for (time, (price, amount)) in dataframe.iterrows():
            self.add_record(Record(time, price=price, amount=amount))

    def read_csv(self, input_):
        """Import database from csv format.

        Args:
            input: stream (file, iostream etc.)

        Returns:
            Nothing.
        """
        reader = csv.DictReader(input_)
        self.clear()
        for row in reader:
            record = Record(
                row["time"], price=float(row["price"]), amount=float(row["amount"])
            )
            self.add_record(record)

    def write_csv(self, out, utc=True):
        """Export database in csv format.

        Args:
            out: stream
            utc (bool): convert to UTC time

        Returns:
            Nothing.

        Notes:

            CSV file format spesification:

            - header row "time,price,amount"
            - comma separated file
            - time in ISO8601 standard (prefer UTC)
            - price and amount with 4 decimals
            - missing values as 'nan'

            Example:

            ```text
            time,price,amount
            2022-12-01T00:00:00+00:00,0.2845,0.2000
            2022-12-01T01:00:00+00:00,0.2779,0.3000
            2022-12-01T02:00:00+00:00,0.2682,nan
            ```

        """
        writer = csv.DictWriter(
            out, fieldnames=["time", "price", "amount"], lineterminator="\n"
        )
        writer.writeheader()
        for record in self.get_records().values():
            writer.writerow(
                {
                    "time": record.get_time(utc).isoformat(),
                    "price": f"{record.get_price():0.4f}",
                    "amount": f"{record.get_amount():0.4f}",
                }
            )
