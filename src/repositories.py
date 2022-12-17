import pandas as pd
from entities import Record
import collections
import math


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

    def __init__(self):
        """Construct a new Database object.

        Args:
            Nothing.

        Returns:
            A new Database object.
        """
        self._records = collections.OrderedDict()

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
            Nothing.
        """
        if self.has_record(record):
            raise KeyError("Record %s already exists!" % record.get_time())
        self._records[record.get_time()] = record

    def update_record(self, record):
        """Update record to database.

        Args:
            record: a record to update.

        Raises:
            KeyError, if record with timestamp not found

        Returns:
            Nothing.

        Notes:
            If record price/value contains float('nan'), it won't get updated.
        """
        if not self.has_record(record):
            raise KeyError("Record %d does not exist!" % record.get_time())
        price = record.get_price()
        amount = record.get_amount()
        if math.isnan(price):
            price = None
        if math.isnan(amount):
            amount = None
        self._records[record.get_time()].update(price=price, amount=amount)

    def add_or_update_record(self, record):
        """Add record to database. If exists, update.

        Args:
            record: a record to add or update.

        Returns:
            Nothing.
        """
        if self.has_record(record):
            self.update_record(record)
        else:
            self.add_record(record)

    def get_records(self):
        """Get all records from the database as a sorted list.

        Args:
            Nothing.

        Returns:
            A list of records.
        """
        self._records = collections.OrderedDict(sorted(self._records.items()))
        return list(self._records.values())

    def get_cheapest_hour(self):
        """Return the cheapest hour from the database.

        Args:
            Nothing.

        Returns:
            A Record where energy price is cheapest.
        """
        cheapest_record = None
        cheapest_price = 2**32
        records = self.get_records()
        assert len(records) > 0
        for record in records:
            if record.get_price() < cheapest_price:
                cheapest_record = record
                cheapest_price = record.get_price()
        return cheapest_record

    def to_dataframe(self):
        """Export database to pandas Dataframe.

        Args:
            Nothing.

        Returns:
            Pandas DataFrame objet.
        """
        index = []
        price = []
        amount = []
        for record in self.get_records():
            index.append(record.get_time())
            price.append(record.get_price())
            amount.append(record.get_amount())
        dataframe = pd.DataFrame({"price": price, "amount": amount}, index=index)
        dataframe.index.name = "time"
        return dataframe

    @staticmethod
    def from_dataframe(df):
        """Import database from pandas Dataframe.

        Args:
            dataframe: Pandas Dataframe

        Returns:
            Database object.
        """
        db = Database()
        for (time, (price, amount)) in df.iterrows():
            db.add_record(Record(time, price=price, amount=amount))
        return db

    def save(self, filename):
        """Save database to disk in csv file format.

        Args:
            filename

        Returns:
            Nothing.

        Notes:

            CSV file format spesification:

            - header row "Time,Price,Amount"
            - comma separated file
            - time in ISO8601 standard (prefer UTC)
            - price and amount with 4 decimals
            - missing values as 'nan'

            Example:

            ```text
            time,price,amount
            2022-12-01T00:00:00Z,0.2845,0.2
            2022-12-01T01:00:00Z,0.2779,0.3
            2022-12-01T02:00:00Z,0.2682,nan
            ```

        """
        df = self.to_dataframe()
        df.to_csv(
            filename,
            float_format="%0.4f",
            date_format="%Y-%m-%dT%H:%M:%SZ",
            na_rep="nan",
        )

    @staticmethod
    def load(filename):
        """Read database from disk.

        Args:
            filename

        Return:
            Database object
        """
        df = pd.read_csv(filename, parse_dates=True, index_col=0)
        return Database.from_dataframe(df)
