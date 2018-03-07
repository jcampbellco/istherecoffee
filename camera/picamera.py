from .camera import Camera
from picamera import PiCamera as PiCam


class PiCamera(Camera):
    def get_image(self):
        camera = PiCam()

        try:
            camera.resolution = (640, 480)
            camera.capture('img.jpg')
        finally:
            camera.close()

        return 'img.jpg'
