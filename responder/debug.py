from responder.responder import Responder
from slackclient import SlackClient


class Debug(Responder):
    def __init__(self, slackclient: SlackClient, config):
        super().__init__(slackclient, config)
        self.debug_enabled = False
        self.debug_user = ""

    def can_handle(self, message):
        return message['text'].find('<@%s>' % self.config.bot_id) > -1 and \
                message['text'].find('debug') > -1 or self.debug_enabled is True

    def handle(self, message):
        if message['text'].find('enable') > -1:
            self.slack.api_call(
                'chat.postMessage',
                channel=message['user'],
                text="Debug mode enabled",
                as_user=True
            )
            self.debug_enabled = True
            self.debug_user = message['user']
        elif message['text'].find('disable') > -1:
            self.slack.api_call(
                'chat.postMessage',
                channel=message['user'],
                text="Debug mode disabled",
                as_user=True
            )
            self.debug_enabled = False
            self.debug_user = ""
        else:
            if self.debug_enabled and self.debug_user:
                self.slack.api_call(
                    'chat.postMessage',
                    channel=self.debug_user,
                    text="```%s```" % message,
                    as_user=True
                )
