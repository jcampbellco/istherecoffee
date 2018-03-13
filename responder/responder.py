from exception.notdefined import NotDefined
from slackclient import SlackClient


class Responder(object):
    def __init__(self, slackclient: SlackClient, config=[]):
        self.slack = slackclient
        self.halt_on_match = False
        self.config = config

    def can_handle(self, message):
        raise NotDefined

    def handle(self, message):
        raise NotDefined
