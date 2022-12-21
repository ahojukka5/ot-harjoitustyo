import json
import datetime
import requests


class ShellyMessage:
    """
    References:
        - https://shelly-api-docs.shelly.cloud/gen2/ComponentsAndServices/Schedule/
    """

    def __init__(self, selection, relays=[], shift=True):
        self._selection = selection
        self._relays = relays
        self._shift = shift
        self._payloads = self.create_payloads()

    @staticmethod
    def get_timespec(time):
        return time.astimezone().strftime("%-S %-M %-H %-d %-m %^a")

    def create_payloads(self):
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
        url = f"http://{shelly_ip}/rpc/Schedule.Create"
        print(f"ShellyMessage: sending payload to {url}")
        status = True
        for payload in self._payloads:
            print(json.dumps(payload, indent=4))
            response = requests.post(url, json=payload)
            print(f"Response: {response.status_code}")
            if response.status_code != 200:
                print(f"Failed to send payload: {response.text}")
                status = False
                break
        return {"status": status}

    def __repr__(self):
        return json.dumps(self._payloads, indent=4)


class MessageService:
    def __init__(self):
        self._targets = {"shelly": ShellyMessage}

    def create_message(self, selection, target, *args, **kwargs):
        if target not in self._targets:
            raise KeyError(f"Unable to send message to target {target}: unknown target")
        return self._targets[target](selection, *args, **kwargs)

    def send_message(self, message, *args, **kwargs):
        return message.send(*args, **kwargs)
