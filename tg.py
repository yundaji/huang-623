from telethon.sync import TelegramClient
from config import API_ID, API_HASH

client = TelegramClient("session", API_ID, API_HASH)


# 📦 相册（不会拆）
def send_album(chat_id, message_ids):

    with client:
        client.send_file(
            chat_id,
            message_ids,
            grouped=True
        )


# 📤 单条消息（修复：不再用 send_message）
def send_single(chat_id, message_id, from_chat):

    with client:

        client.forward_messages(
            chat_id,
            message_id,
            from_chat
        )
