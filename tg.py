import requests
from config import BOT_TOKEN


def copy_post(chat_id, from_chat_id, message_id):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/copyMessage"

    payload = {
        "chat_id": chat_id,
        "from_chat_id": from_chat_id,
        "message_id": message_id
    }

    r = requests.post(url, data=payload)

    # ✅ 加调试（非常关键）
    try:
        result = r.json()
        print("COPY RESULT:", result)
    except Exception:
        print("COPY FAILED:", r.text)

    return r
