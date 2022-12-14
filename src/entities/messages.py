import json
import datetime
import requests

from google.oauth2.credentials import Credentials

# pylint: disable=E0401
from apiclient.discovery import build


class AbstractMessage:
    """Abstract message."""


class ShellyMessage(AbstractMessage):
    """ShellyMessage is a json message which is sent to Shelly device.

    The idea is that ShellyMessage is manipulating Shelly's cronjob in order
    to control relays. Shellys are known be a bit fragile for network connections,
    but with this approach is only required that Shelly is connected to wifi during
    sending the message.

    Typical usage example:

    >>> selection = Selection()
    >>> selection.add_timerange("2022-12-24 18:00", "2022-12-24 19:00")
    >>> relays = [1, 2]  # floor heating + water boiler
    >>> shelly_ip = "192.168.1.30"  # ip address of shelly in local network
    >>> msg = ShellyMessage(selection, relays)
    >>> msg.send(shelly_ip)
    {"status": true}

    Notes:

    Shelly API documentation for scheduler can be found from [1].

    References:

        [1]: https://shelly-api-docs.shelly.cloud/gen2/ComponentsAndServices/Schedule/
    """

    def __init__(self, selection, relays, shift=True, _io=None):
        self._selection = selection
        self._relays = relays
        self._shift = shift
        self._payloads = self.create_payloads()
        self._io = _io

    def maybe_print(self, *args, **kwargs):
        """Print a message if io is connected."""
        if self._io:
            self._io.print(*args, **kwargs)

    @staticmethod
    def get_timespec(time):
        """Return time in a format what Shelly understands.

        Args:
            time (datetime)

        Returns:
            timespec string
        """
        return time.astimezone().strftime("%-S %-M %-H %-d %-m %^a")

    def get_payloads(self):
        """Return payloads of this message."""
        return self._payloads

    def create_payloads(self):
        """Create jsonable payload which is then sent to Shelly."""
        payloads = []
        for selection in self._selection:
            for relay_id in self._relays:
                shift = datetime.timedelta(seconds=self._shift * 10 * relay_id)
                payloads.append(
                    {
                        "enable": True,
                        "timespec": self.get_timespec(selection.start + shift),
                        "calls": [
                            {
                                "method": "Switch.Set",
                                "params": {"id": relay_id, "on": True},
                            }
                        ],
                    }
                )
                payloads.append(
                    {
                        "enable": True,
                        "timespec": self.get_timespec(selection.end + shift),
                        "calls": [
                            {
                                "method": "Switch.Set",
                                "params": {"id": relay_id, "on": False},
                            }
                        ],
                    }
                )
        return payloads

    def send(self, shelly_ip):
        """Send payload to Shelly device.

        Args:
            shelly_ip (str): ip address or host name of shelly device.

        Returns:
            Dictionary {"status": True} if sending payload is succesfull.
        """
        url = f"http://{shelly_ip}/rpc/Schedule.Create"
        self.maybe_print(f"ShellyMessage: sending payload to {url}")
        status = True
        for payload in self._payloads:
            self.maybe_print(json.dumps(payload, indent=4))
            response = requests.post(url, json=payload, timeout=5)
            print(f"Response: {response.status_code}")
            if response.status_code != 200:
                self.maybe_print(f"Failed to send payload: {response.text}")
                status = False
                break
        return {"status": status}

    def __repr__(self):
        return json.dumps(self._payloads, indent=4)


class GoogleMessage(AbstractMessage):
    """GoogleMessage is a message with calendar event payload.

    This requires Google credentials file, and that is not the most trivial
    thing to get.

    Typical usage example:

    >>> selection = Selection()
    >>> selection.add_timerange("2022-12-24 18:00", "2022-12-24 19:00")
    >>> msg = GoogleMessage(selection, summary="Cheap energy, turn sauna on!")
    >>> credentials_file = "google_credentials.json"
    >>> calendar_id = "da...5eb@group.calendar.google.com"
    >>> msg.send(credentials_file, calendar_id)
    {"status": true}
    """

    def __init__(
        self, selection, timezone="Europe/Helsinki", summary="S??hk??h??lytys!", _io=None
    ):
        self._selection = selection
        self._timezone = timezone
        self._summary = summary
        self._payloads = self.create_payload()
        self._io = _io

    def get_payloads(self):
        """Return payloads."""
        return self._payloads

    def maybe_print(self, *args, **kwargs):
        """Print a message if io is connected."""
        if self._io:
            self._io.print(*args, **kwargs)

    def create_payload(self):
        """Create jsonable payload to send using Google service."""
        payloads = []
        for selection in self._selection:
            payloads.append(
                {
                    "summary": self._summary,
                    "start": {
                        "dateTime": selection.start.strftime("%Y-%m-%dT%H:%M:%S"),
                        "timeZone": self._timezone,
                    },
                    "end": {
                        "dateTime": selection.end.strftime("%Y-%m-%dT%H:%M:%S"),
                        "timeZone": self._timezone,
                    },
                    "reminders": {
                        "useDefault": False,
                        "overrides": [
                            {"method": "popup", "minutes": 5},
                        ],
                    },
                }
            )
        return payloads

    def __repr__(self):
        return json.dumps(self._payloads, indent=4)

    def send(self, credentials_file, calendar_id):
        """Send message using Google service. This requires Google credentials."""
        credentials = Credentials.from_authorized_user_file(credentials_file)
        service = build("calendar", "v3", credentials=credentials)
        for payload in self._payloads:
            self.maybe_print("google calendar payload:")
            self.maybe_print(json.dumps(payload, indent=4))
            event = service.events().insert(calendarId=calendar_id, body=payload)
            status = event.execute()
            self.maybe_print(f"response: {status}")
        return {"status": True}
