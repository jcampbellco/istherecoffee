from .responder import Responder


class OhMyGod(Responder):
    def can_handle(self, message):
        return message['text'].find("<@%s>" % self.config.bot_id) > -1 \
               and message['text'].find('you take pictures of coffee') > -1

    def handle(self, message):
        self.slack.api_call(
            'files.upload',
            channels=message['channel'],
            filename='ohmygod.gif',
            file=open('resources/ohmygod.gif', 'rb'),
            as_user=True
        )
