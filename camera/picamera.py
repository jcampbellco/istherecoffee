# Bad dependency? Not sure
# from .camera import Camera
from picamera import PiCamera as PiCam


class PiCamera(object):
    def get_image(self):
        camera = PiCam()

        try:
            camera.resolution = (640, 480)
            camera.capture('img.jpg')
        finally:
            camera.close()

        return 'img.jpg'
