import time
import json
import os
import config
from slackclient import SlackClient
from picamera import PiCamera

slack_client = SlackClient(config.slack_key)

# Fetch your Bot's User ID
user_list = slack_client.api_call("users.list")
for user in user_list.get('members'):
    if user.get('name') == "coffeebot":
        slack_user_id = user.get('id')
        break

# Start connection
if slack_client.rtm_connect():
    print "Connected!"

    while True:
        for message in slack_client.rtm_read():
            if 'text' in message and message['text'].startswith("<@%s>" % slack_user_id) and 'user' in message and message['user'] != slack_user_id:

                print "Message received: %s" % json.dumps(message, indent=2)

                slack_client.api_call(
                    "chat.postMessage",
                    channel=message['channel'],
                    text="Sure thing, let me check on that",
                    as_user=True
                )

                camera = PiCamera()

                try:
                    camera.resolution = (640, 480)
                    camera.capture('img.jpg')
                finally:
                    camera.close()

                slack_client.api_call(
                    'files.upload',
                    channels=message['channel'],
                    filename='test.jpg',
                    file=open('img.jpg', 'rb'),
                    as_user=True
                )

                os.remove('img.jpg')

        time.sleep(1)