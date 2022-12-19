from repositories import Database
from entities import Record

import os
import csv
import config
import requests
import dateutil.parser
import warnings
import json


def update_from_spot_hinta(db):
    rows = requests.get("https://api.spot-hinta.fi/TodayAndDayForward").json()
    for row in rows:
        time = dateutil.parser.parse(row["DateTime"])
        price = row["PriceNoTax"]
        record = Record(time, price=price)
        db.add_or_update_record(record)


def update_from_datahub(db, local_file="data/consumption.csv"):
    if os.path.exists(local_file):
        with open(local_file, "r") as csvfile:
            reader = csv.DictReader(csvfile, delimiter=";")
            for row in reader:
                time = dateutil.parser.parse(row["Alkuaika"])
                amount = float(row["Määrä"])
                record = Record(time, amount=amount)
                db.add_or_update_record(record)
    else:
        warnings.warn(f"consumption file {local_file} not found, unable to update!")


def update_from_json(db, local_file="data/generic_json.json"):
    if os.path.exists(local_file):
        rows = json.load(open(local_file, "r", encoding="utf-8"))
        for row in rows:
            record = Record(row["time"], price=row["price"], amount=row["amount"])
            db.add_or_update_record(record)
    else:
        warnings.warn(f"json file {local_file} not found, unable to update!")


class Saehaekkae:
    """Saehaekkae is a program to help reduce user's energy bill.

    In a variable-price electricity contract, the user can save on the total price
    of energy by scheduling the use of electricity for favorable periods. Saehaekkae
    tackles this problem basically from two different starting points.

    1) by scheduling the use of the devices either automatically (for example with
    various wifi relays) or by receiving a message about the favorable usage time
    to a smart device

    2) by understanding your own electricity consumption over time by visually
    looking at graphs and calculating certain key figures (how well did I manage
    to optimize?)
    """

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
        self._sources[source](self._db, *args, **kwargs)

    def get_data_as_dataframe(self):
        return self._db.to_dataframe()
