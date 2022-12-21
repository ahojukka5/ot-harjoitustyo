class MessageService:
    def __init__(self):
        self._targets = {"shelly": ShellyMessage}

    def create_message(self, selection, target, *args, **kwargs):
        if target not in self._targets:
            raise KeyError(f"Unable to send message to target {target}: unknown target")
        return self._targets[target](selection, *args, **kwargs)

    def send_message(self, message, *args, **kwargs):
        return message.send(*args, **kwargs)
