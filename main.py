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
    if user.get('name') == config.bot_name:
        slack_user_id = user.get('id')
        break

# Start connection
if slack_client.rtm_connect():
    print("Connected!")

    while True:
        for message in slack_client.rtm_read():
            if 'text' in message and message['text'].startswith("@covfefebot") and 'user' in message and message[
                'user'] != slack_user_id:
                slack_client.api_call(
                    'files.upload',
                    channels=message['channel'],
                    filename='covfefe.png',
                    file=open('resources/covfefe.png', 'rb'),
                    as_user=True
                )
                continue

            if 'text' in message and message['text'].startswith("<@%s>" % slack_user_id) and 'user' in message and \
                    message['user'] != slack_user_id:

                print("Message received: %s" % json.dumps(message, indent=2))

                if message['text'].find("hello") > -1:
                    slack_client.api_call(
                        "chat.postMessage",
                        channel=message['channel'],
                        text="I am coffeebot, what is my purpose?",
                        as_user=True
                    )
                    continue

                if message['text'].find("coffee") > -1:
                    slack_client.api_call(
                        'files.upload',
                        channels=message['channel'],
                        filename='ohmygod.gif',
                        file=open('resources/ohmygod.gif', 'rb'),
                        as_user=True
                    )
                    continue

                camera = PiCamera()

                try:
                    camera.resolution = (640, 480)
                    camera.capture('img.jpg')
                finally:
                    camera.close()

                slack_client.api_call(
                    'files.upload',
                    channels=message['channel'],
                    filename='coffee.jpg',
                    file=open('img.jpg', 'rb'),
                    as_user=True
                )

                os.remove('img.jpg')

        time.sleep(1)
