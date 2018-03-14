import os
from .responder import Responder
from slackclient import SlackClient
from camera import Camera


class Img(Responder):
    """
    The "main" responder, if asked `is there coffee`, coffeebot will respond with a picture of the coffee pot

    For testing purpose, see the generic Camera class. It will check if the `picamera` module is available, if it is, it
        will load up the module, take a picture, save it, then pass back the filepath to be uploaded to Slack.

    If the `picamera` module is not available (ie: we're developing locally and don't have a `picamera` module) it will
        just return the path to a test image to be uploaded

    The key point is that this code will _not_ error out if PiCamera isn't installed. So don't be confused when you keep
        asking if there's coffee and coffeebot is just uploading a random picture of a cup of coffee!
    """
    def __init__(self, slackclient: SlackClient, config, camera: Camera):
        self.camera = camera
        super().__init__(slackclient, config)

    def can_handle(self, message):
        return message['text'].find("<@%s>" % self.config.bot_id) > -1 and \
                message['text'].find('is there coffee') > -1 or \
                message['text'].strip() == "<@%s>".format(self.config.bot_id)

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
