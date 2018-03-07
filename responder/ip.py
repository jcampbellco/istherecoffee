from .responder import Responder
import socket


class Ip(Responder):
    """
    Responds with the local IP address for the Pi (in case I forget the IP and need to SSH in)
    Looks for a message like `@coffeebot ip`
    """
    def can_handle(self, message):
        return message['text'].find("<@%s>" % self.config.bot_id) and \
                message['text'].find("ip") > -1

    def handle(self, message):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
        s.close()

        self.slack.api_call(
            "chat.postMessage",
            channel=message['channel'],
            text="My IP is `%s`" % ip,
            as_user=True
        )


