import time
import json
import os
from time import sleep
from slackclient import SlackClient
from picamera import PiCamera

slack_client = SlackClient()

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

                print "Is file readable? " + "true" if os.access('img.jpg', os.R_OK) else "false"

                slack_client.api_call(
                    "chat.postMessage",
                    channel=message['channel'],
                    text="Sure thing, let me check on that",
                    as_user=True
                )

                camera = PiCamera()

                camera.resolution(320, 240)
                camera.start_preview()
                sleep(2)
                camera.capture('img.jpg')

                slack_client.api_call(
                    'files.upload',
                    channels=message['channel'],
                    filename='test.jpg',
                    file=open('img.jpg', 'rb'),
                    as_user=True
                )

        time.sleep(1)
