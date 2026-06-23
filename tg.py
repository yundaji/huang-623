from telethon.sync import TelegramClient
from config import API_ID, API_HASH

client = TelegramClient("session", API_ID, API_HASH)


# 📦 发送“完整媒体组”（图片+视频不拆）
def send_media_group(chat_id, message_ids):

    with client:

        client.send_file(
            chat_id,
            message_ids,
            grouped=True   # ⭐关键：自动合并成一个帖子
        )
