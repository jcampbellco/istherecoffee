from exception.notdefined import NotDefined


class Camera(object):
    def get_image(self):
        raise NotDefined('Camera.get_image')
