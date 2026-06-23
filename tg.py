from telethon.sync import TelegramClient
from config import API_ID, API_HASH

client = TelegramClient("session", API_ID, API_HASH)


# 📦 发送完整“相册/视频组”（不会拆）
def send_media_group(chat_id, message_ids, from_chat):

    with client:

        # ✔ 关键：先把 message_id 转成 Telegram Message 对象
        msgs = client.get_messages(from_chat, ids=message_ids)

        # 单个转 list
        if not isinstance(msgs, list):
            msgs = [msgs]

        # 过滤空值
        msgs = [m for m in msgs if m]

        # ✔ 发送媒体组（核心）
        client.send_file(
            chat_id,
            msgs,
            grouped=True
        )
