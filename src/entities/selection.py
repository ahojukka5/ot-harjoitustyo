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

    def __iter__(self):
        return self.get_timeranges().values().__iter__()

    def is_selected(self, time):
        for tr in self._timeranges.values():
            if tr.start <= time < tr.end:
                return True
        return False

    def add_timerange(self, start, end):
        if isinstance(start, str):
            start = dateutil.parser.parse(start)
        if isinstance(end, str):
            end = dateutil.parser.parse(end)
        assert isinstance(start, datetime.datetime)
        assert isinstance(end, datetime.datetime)
        self._timeranges[start] = Selection.TimeRange(start, end)

    def pack(self):
        """'Pack' timeranges by combining adjacent time ranges."""
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
        if pack:
            self.pack()
        return self._timeranges
