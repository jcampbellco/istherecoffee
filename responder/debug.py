from responder.responder import Responder
from slackclient import SlackClient


class Debug(Responder):
    """
    A debug helper response, expects one of two messages: `@coffeebot debug enable|disable`

    If debug mode is enabled, coffeebot will send an IM to the last user to say `debug enable`, it will contain
        the entire message body, wrapped in a codeblock for readability

    Keep in mind Debug should probably be the very first response handler, since other handlers can potentially stop
        the response chain
    """
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
