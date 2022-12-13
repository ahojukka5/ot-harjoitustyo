"""Record class is the atomic unit containing information about energy price.

The minimum implementation contains time and energy price.

Typical usage example:

    record = Record(time, energy_price)
    record.to_dict()
"""


class Record:
    """A Record class to contain atomic information about energy price.

    Attributes:
        time: Time of the energy price.
        energy_price: The price of the energy at the time.
    """

    def __init__(self, time, energy_price):
        """Constructor of Record.

        Args:
            time: Python datetime object
            energy_price (float): energy price

        Returns:
            A new Record object
        """
        self.time = time
        self.energy_price = energy_price

    def get_time(self):
        """Get time of record.

        Args:
            Nothing.

        Returns:
            Python datetime object.
        """
        return self.time

    def get_energy_price(self):
        """Get energy price of record.

        Args:
            Nothing.

        Returns:
            float describing the price.
        """
        return self.energy_price

    def to_dict(self):
        """Convert record to dictionary

        Args:
            Nothing.

        Returns:
            A python dictionary object
        """
        return {"time": self.get_time(), "energy_price": self.get_energy_price()}
