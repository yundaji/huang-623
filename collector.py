from telethon.sync import TelegramClient
import json
from collections import defaultdict

from config import CHANNELS, POOL_LIMIT, API_ID, API_HASH

client = TelegramClient("session", API_ID, API_HASH)


def build_pool():

    data = {}

    with client:

        for channel in CHANNELS:

            print(f"抓取频道: {channel}")

            msgs = []

            # ✔ 先按时间顺序抓取（旧 → 新）
            for msg in client.iter_messages(channel, limit=POOL_LIMIT, reverse=True):

                if not msg:
                    continue

                # ❌ 完全空消息过滤
                if not msg.message and not msg.media:
                    continue

                msgs.append({
                    "id": msg.id,

                    # ⭐ 关键：用于判断是否属于同一图集/视频组
                    "group": str(msg.grouped_id) if msg.grouped_id else None,

                    # 时间（备用）
                    "date": msg.date.timestamp(),

                    # ⭐ 可选：标记是否有媒体（方便你后面扩展）
                    "has_media": bool(msg.media),

                    # ⭐ 可选：文本
                    "text": msg.message if msg.message else ""
                })

            # ✔ 重新整理：保证 group 结构稳定
            grouped = defaultdict(list)
            normal = []

            for m in msgs:
                if m["group"]:
                    grouped[m["group"]].append(m)
                else:
                    normal.append(m)

            # ✔ 合并回结构（保证稳定顺序）
            final_pool = []

            # 先加普通消息
            for m in normal:
                final_pool.append(m)

            # 再加图集（按 group）
            for g in grouped.values():
                g_sorted = sorted(g, key=lambda x: x["id"])
                final_pool.append({
                    "group": g_sorted[0]["group"],
                    "id": g_sorted[0]["id"],
                    "date": g_sorted[0]["date"],
                    "type": "album",
                    "items": [x["id"] for x in g_sorted]
                })

            data[channel] = final_pool

    with open("data.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print("✅ data.json 已生成（已支持图集分组）")


if __name__ == "__main__":
    build_pool()
