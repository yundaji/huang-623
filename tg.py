import requests
from config import BOT_TOKEN


# ✔ 原样复制帖子（不显示转发，不拆图，不拆视频）
def copy_post(chat_id, from_chat_id, message_id):

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/copyMessage"

    payload = {
        "chat_id": chat_id,
        "from_chat_id": from_chat_id,
        "message_id": message_id
    }

    requests.post(url, data=payload)
