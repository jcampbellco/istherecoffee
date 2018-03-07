import os
from .responder import Responder
from slackclient import SlackClient
from camera import Camera


class Img(Responder):
    def __init__(self, slackclient: SlackClient, config, camera: Camera):
        self.camera = camera
        super().__init__(slackclient, config)

    def can_handle(self, message):
        return message['text'].find("<@%s>" % self.config.bot_id) > -1 and \
                message['text'].find('is there coffee') > -1

    def handle(self, message):
        print('Taking image...')

        path = self.camera.get_image()

        print('Image saved to `{0}`'.format(path))

        self.slack.api_call(
            'files.upload',
            channels=message['channel'],
            filename='coffee.jpg',
            file=open(path, 'rb'),
            as_user=True
        )

        print('Image uploaded, removing')

        os.remove(path)

        print('Image removed from `{0}`'.format(path))
