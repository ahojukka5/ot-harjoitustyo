from entities import ShellyMessage, GoogleMessage


class MessageService:
    """Message service is used to create and send messages."""

    def __init__(self):
        self._targets = {"shelly": ShellyMessage, "google-calendar": GoogleMessage}

    def add_target(self, target, target_class):
        """Add new target where to send message

        Args:
            target (str): name of the target
            target_class: a class that inherits AbstractMessage and implements `send`

        Returns:
            Nothing.
        """
        self._targets[target] = target_class

    def create_message(self, selection, target, *args, **kwargs):
        """Create a new message.

        Args:
            selection (Selection)
            target (str): name of the message used in mapping ('shelly' or 'google-calendar')

        Rest of the arguments are passed to message constructor

        Returns:
            Message
        """
        if target not in self._targets:
            raise KeyError(f"Unable to send message to target {target}: unknown target")
        return self._targets[target](selection, *args, **kwargs)

    def send_message(self, message, *args, **kwargs):
        """Send message.

        Args:
            message (Message)

        Rest of the arguments are passed to Message.send function.

        Returns:
            Dictionary having the status
        """
        return message.send(*args, **kwargs)
