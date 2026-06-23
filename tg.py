import requests
from config import BOT_TOKEN


# 单条消息
def send_single(chat_id, message_id, from_chat):

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/copyMessage"

    requests.post(url, data={
        "chat_id": chat_id,
        "from_chat_id": from_chat,
        "message_id": message_id
    })


# 相册（重点：不拆图）
def send_album(chat_id, message_ids, from_chat):

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/copyMessages"

    requests.post(url, data={
        "chat_id": chat_id,
        "from_chat_id": from_chat,
        "message_ids": message_ids
    })
