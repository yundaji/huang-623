from telethon.sync import TelegramClient
import json
from collections import defaultdict

from config import CHANNELS, POOL_LIMIT, API_ID, API_HASH

client = TelegramClient("session", API_ID, API_HASH)


def build_pool():

    data = {}

    with client:

        for channel in CHANNELS:

            print("抓取频道:", channel)

            msgs = []

            for msg in client.iter_messages(channel, limit=POOL_LIMIT, reverse=True):

                if not msg:
                    continue

                if not msg.message and not msg.media:
                    continue

                msgs.append({
                    "id": msg.id,
                    "group": str(msg.grouped_id) if msg.grouped_id else None
                })

            # =========================
            # ⭐⭐⭐ 核心改造就在这里
            # =========================

            grouped = defaultdict(list)
            singles = []

            for m in msgs:
                if m["group"]:
                    grouped[m["group"]].append(m)
                else:
                    singles.append(m)

            final_pool = []

            # ✔ 单条消息
            for m in singles:
                final_pool.append({
                    "type": "single",
                    "message_id": m["id"]
                })

            # ✔ 图集 / 视频组
            for g in grouped.values():
                g_sorted = sorted(g, key=lambda x: x["id"])

                final_pool.append({
                    "type": "album",
                    "message_ids": [x["id"] for x in g_sorted]
                })

            data[channel] = final_pool

    with open("data.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print("✅ data.json 已生成（已结构化 single + album）")


if __name__ == "__main__":
    build_pool()
