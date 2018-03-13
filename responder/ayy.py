from responder.responder import Responder


class Ayy(Responder):
    """
    Responds to messages that start with @covfefebot with a joke picture
    """
    def can_handle(self, message):
        return message['text'].find("<@%s>" % self.config.bot_id) > -1 and \
               message['text'].find('ayy') > -1

    def handle(self, message):
        self.slack.api_call(
            'files.upload',
            channels=message['channel'],
            filename='ayy.png',
            file=open('resources/ayy.png', 'rb'),
            as_user=True
        )
