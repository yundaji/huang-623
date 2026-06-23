from telethon.sync import TelegramClient
import json
import os
from collections import defaultdict

from config import CHANNELS, POOL_LIMIT, API_ID, API_HASH

client = TelegramClient("session", API_ID, API_HASH)


def build_pool():

    # =========================
    # 🚀 强制清理旧数据（关键）
    # =========================
    if os.path.exists("data.json"):
        os.remove("data.json")
        print("🧹 已删除旧 data.json")

    data = {}

    with client:

        for channel in CHANNELS:

            print(f"\n抓取频道: {channel}")

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
            # 🚀 结构重建（single + album）
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

            print(f"📦 已生成: {len(final_pool)} 条结构化内容")

    # =========================
    # 🚀 写入全新 data.json
    # =========================
    with open("data.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print("\n✅ data.json 已全量重建完成（无旧结构污染）")


if __name__ == "__main__":
    build_pool()
