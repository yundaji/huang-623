import json
from config import CHANNELS, DAILY_COUNT
from tg import send_single, send_album


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

        # 已发送ID
        sent_ids = set(sent.get(channel, []))

        # 未发送内容（去重）
        unsent = [m for m in pool if str(m["id"]) not in sent_ids]

        # 如果不够 → 重置循环
        if len(unsent) < DAILY_COUNT:
            sent[channel] = []
            sent_ids = set()
            unsent = pool

        # ✅ 顺序发布（关键修改点）
        selected = unsent[:DAILY_COUNT]

        albums = {}
        singles = []

        # 分类：相册 / 单条
        for m in selected:

            gid = m.get("group")

            if gid:
                albums.setdefault(gid, []).append(m["id"])
            else:
                singles.append(m["id"])

        # 📤 先发相册（保持顺序）
        for gid, ids in albums.items():

            # 保证相册内部顺序
            ids = sorted(ids)

            send_album(channel, ids, channel)

            for i in ids:
                sent.setdefault(channel, []).append(str(i))

        # 📤 再发单条（顺序）
        for mid in singles:

            send_single(channel, mid, channel)

            sent.setdefault(channel, []).append(str(mid))

        # 保存记录
        save("sent.json", sent)


if __name__ == "__main__":
    main()
