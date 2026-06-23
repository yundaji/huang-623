from telethon.sync import TelegramClient
import json
from config import CHANNELS, POOL_LIMIT, API_ID, API_HASH

client = TelegramClient("session", API_ID, API_HASH)


def build_pool():

    data = {}

    with client:

        for channel in CHANNELS:

            print("抓取频道:", channel)

            msgs = []

            # ✔ 按时间顺序（旧 → 新）
            for msg in client.iter_messages(channel, limit=POOL_LIMIT, reverse=True):

                if not msg:
                    continue

                if not msg.message and not msg.media:
                    continue

                msgs.append({
                    "id": msg.id,
                    "group": str(msg.grouped_id) if msg.grouped_id else None,
                    "date": msg.date.timestamp()
                })

            data[channel] = msgs

    with open("data.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False)

    print("✅ data.json 已生成")


if __name__ == "__main__":
    build_pool()
