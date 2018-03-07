from responder.responder import Responder


class Covfefe(Responder):
    def can_handle(self, message):
        return message['text'].startswith("@covfefebot")

    def handle(self, message):
        self.slack.api_call(
            'files.upload',
            channels=message['channel'],
            filename='covfefe.png',
            file=open('resources/covfefe.png', 'rb'),
            as_user=True
        )
