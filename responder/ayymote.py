from responder.responder import Responder


class Ayymote(Responder):
    """
    The simplest responder, just asks
    """
    def can_handle(self, message):
        return message['text'].find("<@%s>" % self.config.bot_id) > -1 \
                and message['text'].find('ayymote') > -1

    def handle(self, message):
        self.slack.api_call(
            "chat.postMessage",
            channel=message['channel'],
            text="{0} {1} {0}".format(':point_right:', ':sunglasses:'),
            as_user=True
        )
