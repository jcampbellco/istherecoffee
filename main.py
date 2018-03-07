import time
import config
from slackclient import SlackClient
from responder import Covfefe, Debug, Hello, Img, Ip, OhMyGod
from camera import Camera


# Initialize the Slack client
slack_client = SlackClient(config.slack_key)

# Initialize the camera
camera = Camera().get()

# "Register" our responders
responders = [
    Covfefe(slack_client, config),
    Debug(slack_client, config),
    Hello(slack_client, config),
    Img(slack_client, config, camera),
    Ip(slack_client, config),
    OhMyGod(slack_client, config),
]

# Start connection
if slack_client.rtm_connect():
    print("Connected to Slack server!")

    # If the bot (user) ID isn't set in the config, try to find it based on name
    if not config.bot_id:
        print("No bot ID set, fetch user list...")
        # Fetch your Bot's User ID
        user_list = slack_client.api_call("users.list")
        print("Found {0} users".format(len(user_list.get('members'))))

        for user in user_list.get('members'):
            if user.get('name') == config.bot_name:
                config.bot_id = user.get('id')
                break

    # If it still isn't set (ie: the above method failed to find a suitable user ID) then raise an exception
    if not config.bot_id:
        raise Exception('A `bot_id` value was not set in the config, either set it explicitly or set the bot name')

    print("Using user ID of `{0}`".format(config.bot_id))

    # Now get the channel ID if it's not set explicitly in the config
    if not config.channel_id:
        print("No channel ID set, fetching channel list...")

        channels = slack_client.api_call('channels.list', exclude_archived=1)

        print("Found {0} channels".format(len(channels['channels'])))

        if not config.channel_id or config.channel_id == "":
            for channel in channels['channels']:
                if channel['name'] == config.channel_name:
                    config.channel_id = channel['id']
                    print("Found channel `{0}` as ID `{1}`, joining...".format(channel['name'], channel['id']))
                    break

    # If it still isn't set (the channel ID) then raise an exception
    if not config.channel_id:
        raise Exception('Channel ID for `{0}` could not be found, does the channel exist?'.format(config.channel_name))

    print("Joining channel with ID `{0}`".format(config.channel_id))

    slack_client.api_call(
        'channels.join',
        channel=config.channel_id
    )

    while True:
        for message in slack_client.rtm_read():

            # Skip this message if we don't have a `text` field
            if 'text' not in message:
                continue

            # Skip this message if it's from the bot
            if 'user' not in message or message['user'] == config.bot_id:
                continue

            print("Found message, attempting to locate responder using `{0}`".format(message))

            # Now loop over the responders and find any that match - including multiple responses
            for responder in responders:
                if responder.can_handle(message):
                    responder.handle(message)

                    # If the responder should halt after matching (to prevent multiple responses) then break
                    if responder.halt_on_match:
                        break

        time.sleep(1)
