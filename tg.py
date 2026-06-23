from telethon.sync import TelegramClient
from config import API_ID, API_HASH

client = TelegramClient("session", API_ID, API_HASH)


# 📦 媒体组（图片+视频一起，不拆）
def send_media_group(chat_id, message_ids):

    with client:

        client.send_file(
            chat_id,
            message_ids,
            grouped=True   # ⭐关键：保持原帖结构
        )


# 📤 单条
def send_single(chat_id, message_id, from_chat):

    with client:

        client.forward_messages(
            chat_id,
            message_id,
            from_chat
        )
