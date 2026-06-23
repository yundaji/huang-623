import json
from config import CHANNELS, DAILY_COUNT
from tg import send_media_group


def load(file, default):
    try:
        with open(file, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return default


def save(file, data):
    with open(file, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False)


def main():

    data = load("data.json", {})
    sent = load("sent.json", {})

    for channel in CHANNELS:

        pool = data.get(channel, [])

        sent_ids = set(sent.get(channel, []))

        # ✔ 去重
        unsent = [m for m in pool if str(m["id"]) not in sent_ids]

        # ✔ 不够就重置循环
        if len(unsent) < DAILY_COUNT:
            sent[channel] = []
            unsent = pool

        # ✔ 顺序发布
        selected = unsent[:DAILY_COUNT]

        # 📦 关键：按 grouped_id 合并媒体组
        albums = {}
        singles = []

        for m in selected:

            gid = m.get("group")

            if gid:
                albums.setdefault(gid, []).append(m["id"])
            else:
                singles.append(m["id"])

        # 📤 先发“相册/视频组”（不会拆）
        for gid, ids in albums.items():

            ids = sorted(ids)

            send_media_group(channel, ids)

            for i in ids:
                sent.setdefault(channel, []).append(str(i))

        # 📤 单条消息（如果有）
        for mid in singles:

            send_media_group(channel, [mid])

            sent.setdefault(channel, []).append(str(mid))

        save("sent.json", sent)


if __name__ == "__main__":
    main()
