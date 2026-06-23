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

        sent_ids = set(sent.get(channel, []))

        unsent = [m for m in pool if str(m["id"]) not in sent_ids]

        if len(unsent) < DAILY_COUNT:
            sent[channel] = []
            unsent = pool

        # ✔ 顺序发送
        selected = unsent[:DAILY_COUNT]

        albums = {}
        singles = []

        # 📦 分组（相册 / 单条）
        for m in selected:

            gid = m.get("group")

            if gid:
                albums.setdefault(gid, []).append(m["id"])
            else:
                singles.append(m["id"])

        # 📤 相册（不会拆）
        for gid, ids in albums.items():

            ids = sorted(ids)

            send_album(channel, ids)

            for i in ids:
                sent.setdefault(channel, []).append(str(i))

        # 📤 单条（已修复 crash）
        for mid in singles:

            send_single(channel, mid, channel)

            sent.setdefault(channel, []).append(str(mid))

        save("sent.json", sent)


if __name__ == "__main__":
    main()
