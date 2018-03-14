from .camera import Camera


class MockCamera(Camera):
    def get_image(self):
        return 'resources/coffee.jpg'
