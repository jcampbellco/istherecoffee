from .camera import Camera
from picamera import PiCamera


class RealCamera(Camera):
    def get_image(self):
        camera = PiCamera()

        try:
            camera.resolution = (640, 480)
            camera.capture('img.jpg')
        finally:
            camera.close()

        return 'img.jpg'
