import requests
from config import BOT_TOKEN


# ✔ 单条消息（文字 / 图片 / 视频）
def send_single(chat_id, from_chat_id, message_id):

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/copyMessage"

    r = requests.post(url, data={
        "chat_id": chat_id,
        "from_chat_id": from_chat_id,
        "message_id": message_id
    })

    try:
        return r.json().get("ok", False)
    except:
        return False


# ✔ 图集 / 视频组（核心）
def send_group(chat_id, from_chat_id, message_ids):

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/forwardMessages"

    r = requests.post(url, data={
        "chat_id": chat_id,
        "from_chat_id": from_chat_id,
        "message_ids": message_ids
    })

    try:
        return r.json().get("ok", False)
    except:
        return False
