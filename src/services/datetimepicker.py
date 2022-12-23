import datetime
import dateutil.parser
from entities import Selection


class DateTimePicker:
    """DateTimePicker is a service to pick and select time ranges from ui.

    Typical usage example:

    >>> picker = DateTimePicker()
    >>> picker.pick("2022-12-24 18:00").pick_between("2022-12-24 20:00", "2022-12-24 22:00")
    >>> print(picker.to_selection())
    2022-12-24 18:00 - 2022-12-24 19:00
    2022-12-24 20:00 - 2022-12-24 22:00

    Like shown above, methods can be chained.
    """

    def __init__(self):
        self._selection = Selection()

    def clear(self):
        """Clear selection."""
        self._selection = Selection()

    def pick(self, start):
        """Pick based on start time.

        Args:
            start (str or datetime): pick starting time

        Returns:
            self

        Notes:
            It is assumed that end time is one hour from start time.
        """
        if isinstance(start, str):
            start = dateutil.parser.parse(start).astimezone()
        end = start + datetime.timedelta(hours=1)
        self._selection.add_timerange(start, end)
        return self

    def pick_between(self, start, end):
        """Pick between start time and end time.

        Args:
            start (str or datetime)
            end (str or datetime)

        Returns:
            self
        """
        if isinstance(start, str):
            start = dateutil.parser.parse(start).astimezone()
        if isinstance(end, str):
            end = dateutil.parser.parse(end).astimezone()
        self._selection.add_timerange(start, end)
        return self

    def to_selection(self):
        """Convert DateTimePicker to Selection."""
        return self._selection
