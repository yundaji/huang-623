from telethon.sync import TelegramClient
from config import API_ID, API_HASH

client = TelegramClient("session", API_ID, API_HASH)


# 📦 相册（图 + 视频不拆）
def send_album(chat_id, message_ids):

    with client:

        client.send_file(
            chat_id,
            message_ids,
            grouped=True   # ⭐关键：保持原帖结构
        )


