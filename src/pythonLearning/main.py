import configparser
import json
from datetime import date, datetime

from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.errors import SessionPasswordNeededError
from telethon.tl.functions.messages import (GetHistoryRequest)
from telethon.tl.types import (
    PeerChannel, InputPeerEmpty
)

# Reading Configs
config = configparser.ConfigParser()
config.read("config.ini")

# Setting configuration values
api_id = config['Telegram']['api_id']
api_hash = config['Telegram']['api_hash']

api_hash = str(api_hash)

phone = config['Telegram']['phone']
username = config['Telegram']['username']

# Create the client and connect
client = TelegramClient(username, api_id, api_hash)
client.start()
print("Client Created")
# Ensure you're authorized
if not client.is_user_authorized():
    client.send_code_request(phone)
    try:
        client.sign_in(phone, input('Enter the code: '))
    except SessionPasswordNeededError:
        client.sign_in(password=input('Password: '))


    # some functions to parse json date
class DateTimeEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime):
            return o.isoformat()

        if isinstance(o, bytes):
            return list(o)

        return json.JSONEncoder.default(self, o)


me = client.get_me()


async def dump_all_messages(channel):
    offset_msg = 0
    limit_msg = 1
    all_messages = []
    total_messages = 1
    total_count_limit = 1

    while True:
        history = await client(GetHistoryRequest(
            peer=channel,
            offset_id=offset_msg,
            offset_date=None, add_offset=0,
            limit=limit_msg, max_id=0, min_id=0,
            hash=0
        ))

        print(history.messages)
        if not history.messages:
            break
        messages = history.messages
        for message in messages:
            print("===", message)
            all_messages.append(message.to_dict())
        offset_msg = messages[len(messages) - 1].id
        total_messages - len(all_messages)
        if total_count_limit != 0 and total_messages >= total_count_limit:
            break
    with open('channel_messages.json', 'w') as outfile:
        json.dump(all_messages, outfile, ensure_ascii=False, cls=DateTimeEncoder)


async def main():
    user_input_channel = input("enter entity(telegram URL or entity id): ")
    if user_input_channel.isdigit():
        entity = PeerChannel(int(user_input_channel))
    else:
        entity = user_input_channel
    channel = await client.get_entity(entity)

    await dump_all_messages(channel)


with client:
    client.loop.run_until_complete(main())
