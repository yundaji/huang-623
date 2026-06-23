import requests
from config import BOT_TOKEN


def copy_posts(chat_id, from_chat_id, message_ids):
    """
    ✔ 原样复制（支持相册/视频组，不拆分）
    """

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/copyMessages"

    payload = {
        "chat_id": chat_id,
        "from_chat_id": from_chat_id,
        "message_ids": message_ids
    }

    r = requests.post(url, json=payload)

    try:
        result = r.json()
        print("📦 COPY RESULT:", result)

        if not result.get("ok"):
            print("❌ COPY FAILED:", result)

    except Exception as e:
        print("❌ REQUEST ERROR:", str(e), r.text)

    return r
