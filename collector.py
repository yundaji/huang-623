from telethon.sync import TelegramClient
import json
from config import CHANNELS, POOL_LIMIT

API_ID = 37199356   # 你去 https://my.telegram.org 获取
API_HASH = "d9156458a8520ad1d227f14c43ee19e7"

client = TelegramClient("session", API_ID, API_HASH)


def build_pool():

    data = {}

    with client:

        for channel in CHANNELS:

            print("抓取频道:", channel)

            msgs = []

            for msg in client.iter_messages(channel, limit=POOL_LIMIT):

                if not msg:
                    continue

                if not msg.message and not msg.media:
                    continue

                msgs.append({
                    "id": msg.id
                })

            data[channel] = msgs

    with open("data.json", "w") as f:
        json.dump(data, f)

    print("完成：data.json 已生成")


if __name__ == "__main__":
    build_pool()
