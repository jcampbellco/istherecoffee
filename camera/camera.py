from .mock_camera import MockCamera
from exception.notdefined import NotDefined
import importlib


class Camera(object):
    def get(self):
        # Check and see if we have a picamera module
        if importlib.find_loader('picamera'):
            # ...and if we do, load it...
            picam = importlib.import_module('picamera')
            # ...then return an instance of the PiCamera object
            return picam.PiCamera()
        else:
            # Otherwise, just return a "mock" camera for testing purposes
            return MockCamera()

    def get_image(self):
        raise NotDefined('Camera.get_image')
