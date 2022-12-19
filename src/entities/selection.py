import datetime
import dateutil.parser
from collections import OrderedDict, namedtuple


class Selection:

    TimeRange = namedtuple("TimeRange", ["start", "end"])

    def __init__(self):
        self._timeranges = OrderedDict()

    def __getitem__(self, time):
        if isinstance(time, str):
            time = dateutil.parser.parse(time)
        return self._timeranges[time]

    def add_timerange(self, start, end):
        if isinstance(start, str):
            start = dateutil.parser.parse(start)
        if isinstance(end, str):
            end = dateutil.parser.parse(end)
        assert isinstance(start, datetime.datetime)
        assert isinstance(end, datetime.datetime)
        self._timeranges[start] = Selection.TimeRange(start, end)
