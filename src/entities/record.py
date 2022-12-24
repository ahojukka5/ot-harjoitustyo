from datetime import datetime
import json
import math
from dateutil.tz import tzutc
from dateutil import parser


class Record:
    """A Record class to contain information about energy price and usage.

    The implementation contains time (unix time stamp), energy price in eur and
    energy usage in kWh. When updating energy prices and/or consumption, very
    likely scenario is that one of those is unknown. This record gives some
    flexibility so that it supports missing values as well as updating values
    later on. Internally, record stores time as a datetime object, but
    constructor also supports unix timestamps and different kind of string
    formats which are passed to `dateutil.parser`, like ISO 8601 format.

    Timestamp is timezone-aware. If no timezone is given, it's expected to be
    UTC.

    Typical usage example:

        >>> record("2022-12-16 12:00:00", price=12.34)
        >>> record.to_json()

        >>> record.update(amount=3.0)
        >>> record.to_json()

    Attributes:
        time: Time of the energy price as Python datetime object
        price: The price of the energy at the time as float
        amount: The amount of energy used at the time as float
    """

    def __init__(self, time, price=float("nan"), amount=float("nan")):
        """Constructor of Record.

        Args:
            time: Python datetime object
            price: energy price (EUR) as float
            amount: the amount of energy (kWh) as float

        Returns:
            A new Record object

        Notes:
            Time can also be given as integer (unix timestamp) or any string what dateutil.parser
            understand, and it will be converted to datetime. Datetime without time zone will be
            made timezone-aware by assuming utc.
        """
        if isinstance(time, int):
            self._time = datetime.utcfromtimestamp(time)
        elif isinstance(time, str):
            self._time = parser.parse(time)
        else:
            assert isinstance(time, datetime)
            self._time = time
        if not self._time.tzinfo:
            self._time = self._time.replace(tzinfo=tzutc())
        self._time = self._time.astimezone(tzutc())
        self._price = float(price)
        self._amount = float(amount)

    def __eq__(self, other):
        """Overrides the default implementation"""
        if isinstance(other, Record):
            return (
                (self._time == other._time)
                and (self._price == other._price)
                and (self._amount == other._amount)
            )
        return False

    def get_time(self, utc=False):
        """Get time of record.

        Args:
            utc: bool, convert time to UTC time

        Returns:
            Python datetime object.
        """
        if utc:
            return self._time.astimezone(tzutc())
        return self._time

    def get_price(self):
        """Get energy price.

        Args:
            Nothing.

        Returns:
            float describing the price.
        """
        return self._price

    def get_amount(self):
        """Get energy amount.

        Args:
            Nothing.

        Returns:
            float describing the price.
        """
        return self._amount

    def has_price(self):
        """Check does record have a finite price.

        Args:
            Nothing.

        Returns:
            Boolean
        """
        return math.isfinite(self.get_price())

    def has_amount(self):
        """Check does record have a finite amount.

        Args:
            Nothing.

        Returns:
            Boolean
        """
        return math.isfinite(self.get_amount())

    def update(self, price=None, amount=None):
        """Update record.

        Args:
            price (float): optional
            amount (float): optional

        Returns:
            Boolean tuple (price_updated, amount_updated)
        """
        price_updated = False
        amount_updated = False
        if price:
            price = float(price)
            price_updated = self._price != price
            if price_updated:
                self._price = price
        if amount:
            amount = float(amount)
            amount_updated = self._amount != amount
            if amount_updated:
                self._amount = float(amount)
        return (price_updated, amount_updated)

    def __repr__(self):
        time = self.get_time().isoformat()
        price = self.get_price()
        amount = self.get_amount()
        return f"{time},{price:5.4f},{amount:5.4f}"

    def to_dict(self):
        """Convert record to dictionary.

        Time is converted to iso format."""
        return {
            "time": self.get_time().isoformat(),
            "price": self.get_price(),
            "amount": self.get_amount(),
        }

    def to_json(self):
        """Convert record to json string

        Args:
            Nothing.

        Returns:
            A python dictionary object
        """
        return json.dumps(self.to_dict())
