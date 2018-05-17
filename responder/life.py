from responder.responder import Responder


class Life(Responder):

    def can_handle(self, message):
        return message['text'].find("<@%s>" % self.config.bot_id) > -1 and \
               message['text'].find('life') > -1

    def handle(self, message):
        self.slack.api_call(
            'files.upload',
            channels=message['channel'],
            filename='life.png',
            file=open('resources/life.png', 'rb'),
            as_user=True
        )
