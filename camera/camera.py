from .mock_camera import MockCamera
from exception.notdefined import NotDefined
import importlib


class Camera(object):
    def get(self):
        if importlib.find_loader('picamera'):
            picam = importlib.import_module('picamera')
            print(picam)
            return picam.PiCamera()
        else:
            return MockCamera()

    def get_image(self):
        raise NotDefined('Camera.get_image')
