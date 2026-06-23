from telethon.sync import TelegramClient
from config import API_ID, API_HASH

client = TelegramClient("session", API_ID, API_HASH)


def send_album(chat_id, message_ids):

    # 🔥 关键：grouped=True 才是相册
    with client:

        client.send_file(
            chat_id,
            message_ids,
            grouped=True
        )


def send_single(chat_id, message_id):

    with client:

        client.send_message(chat_id, message_id)
