import datetime
import dateutil.parser


class Selection:
    def __init__(self, start: datetime.datetime, end=None):
        if isinstance(start, str):
            self._start = dateutil.parser.parse(start)
        else:
            self._start = start
        if end is None:
            self._end = self._start + datetime.timedelta(hours=1)
        else:
            if isinstance(end, str):
                self._end = dateutil.parser.parse(end)
            else:
                self._end = end
        assert isinstance(self._start, datetime.datetime)
        assert isinstance(self._end, datetime.datetime)

    def get_start(self):
        return self._start

    def get_end(self):
        return self._end
