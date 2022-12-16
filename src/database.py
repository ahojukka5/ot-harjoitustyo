"""Implementation of database class.

The basic implementation of database adds functionality to manipulate a group of
records. They can be added and exported to pandas DataFrame.

Typical usage example:

  db = Database()
  db.add_record(record1)
  db.add_record(record2)
  df = db.to_dataframe()

"""

import pandas as pd
from record import Record


class Database:
    """Database to contain and manipulate records.

    The main functionality of the database class is to contain
    necessary functionality to handle records.

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
        self.records = []

    def add_record(self, record):
        """Add new record to database.

        Args:
            record: A Record object to add.

        Returns:
            Nothing.
        """
        self.records.append(record)

    def get_records(self):
        """Get all records from the database.

        Args:
            Nothing.

        Returns:
            A list of records.
        """
        return self.records

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
