import requests
from config import BOT_TOKEN

def send_message(chat_id, message_id, from_chat):

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/copyMessage"

    data = {
        "chat_id": chat_id,
        "from_chat_id": from_chat,
        "message_id": message_id
    }

    requests.post(url, data=data)
