import json
import random
from config import CHANNELS, DAILY_COUNT
from tg import send_single, send_album


def load(file, default):
    try:
        with open(file, "r") as f:
            return json.load(f)
    except:
        return default


def save(file, data):
    with open(file, "w") as f:
        json.dump(data, f)


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

        selected = random.sample(unsent, DAILY_COUNT)

        albums = {}
        singles = []

        # 🔥 相册 & 单图分类
        for m in selected:

            if m.get("group"):
                albums.setdefault(m["group"], []).append(m["id"])
            else:
                singles.append(m["id"])

        # 📤 发相册（不拆图）
        for gid, ids in albums.items():
            send_album(channel, ids, channel)
            for i in ids:
                sent.setdefault(channel, []).append(str(i))

        # 📤 发单图
        for mid in singles:
            send_single(channel, mid, channel)
            sent.setdefault(channel, []).append(str(mid))

        save("sent.json", sent)


if __name__ == "__main__":
    main()
