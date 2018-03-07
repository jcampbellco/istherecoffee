from responder.responder import Responder


class Hello(Responder):
    def can_handle(self, message):
        return message['text'].find("<@%s>" % self.config.bot_id) > -1 \
                and message['text'].find('hello') > -1

    def handle(self, message):
        self.slack.api_call(
            "chat.postMessage",
            channel=message['channel'],
            text="I am {0}, what is my purpose?".format(self.config.bot_name),
            as_user=True
        )
