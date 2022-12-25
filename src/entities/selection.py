import datetime
from collections import OrderedDict, namedtuple
import dateutil.parser


class Selection:
    """Selection is a container for time ranges.

    Typical usage example:

    >>> selection = Selection()
    >>> selection.add_timerange("2022-12-24 12:00", "2022-12-24 13:00")
    >>> selection.add_timerange("2022-12-24 13:00", "2022-12-24 14:00")

    After that, one can, for example, test, whether time is inside a selection:

    >>> selection.is_selected("2022-12-24 12:30")
    True

    >>> "2022-12-24 12:30" in selection
    True

    There is a function 'pack', which allows to merge several time ranges to one,
    if they are adjacent to each other:

    >>> print(selection.pack())
    2022-12-24 12:00 - 2022-12-24 14:00

    Notes

    Time range is defined such that `start <= time < end`, i.e. time range does not
    contain the endpoint.
    """

    TimeRange = namedtuple("TimeRange", ["start", "end"])

    def __init__(self):
        self._timeranges = OrderedDict()

    def __getitem__(self, time):
        if isinstance(time, str):
            time = dateutil.parser.parse(time).astimezone()
        return self._timeranges[time]

    def __iter__(self):
        return self.get_timeranges().values().__iter__()

    def __repr__(self):
        strings = []
        for timerange in self.get_timeranges().values():
            start = timerange.start.isoformat()
            end = timerange.end.isoformat()
            strings.append(f"{start} - {end}")
        return ", ".join(strings)

    def __contains__(self, time):
        return self.is_selected(time)

    def is_selected(self, time):
        """Return whether time is inside some of the timeranges.

        Args:
            time (str or datetime)

        Returns:
            True if time is inside, false otherwise.
        """
        if isinstance(time, str):
            time = dateutil.parser.parse(time).astimezone()
        for timerange in self._timeranges.values():
            if timerange.start <= time < timerange.end:
                return True
        return False

    def add_timerange(self, start, end):
        """Add new timerange to selection.

        Args:
            start (str or datetime)
            end (str or datetime)

        Return
            Nothing.
        """
        if isinstance(start, str):
            start = dateutil.parser.parse(start).astimezone()
        if isinstance(end, str):
            end = dateutil.parser.parse(end).astimezone()
        assert isinstance(start, datetime.datetime)
        assert isinstance(end, datetime.datetime)
        self._timeranges[start] = Selection.TimeRange(start, end)

    def pack(self):
        """'Pack' timeranges by combining adjacent time ranges.

        As a result of packing, time ranges e.g. 13-14 and 14-15 are merged such
        that there is only one timerange between 13-15.
        """
        done = False
        trs = self._timeranges = OrderedDict(sorted(self._timeranges.items()))
        while not done:
            done = True
            keys = list(self._timeranges.keys())
            for i in range(len(keys) - 1):
                tri = trs[keys[i]]
                trj = trs[keys[i + 1]]
                if tri.end == trj.start:
                    del trs[trj.start]
                    trs[tri.start] = Selection.TimeRange(tri.start, trj.end)
                    done = False
                    break
        return self

    def get_timeranges(self, pack=True):
        """Return all timeranges.

        Args:
            pack (bool, optional). Whether pack the timeranges before return or not.
        """
        if pack:
            self.pack()
        return self._timeranges
