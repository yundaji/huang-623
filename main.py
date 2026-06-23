import json
from config import CHANNELS, DAILY_COUNT
from tg import copy_post


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

        # ✔ 去重（昨天发过的不再发）
        unsent = [m for m in pool if str(m["id"]) not in sent_ids]

        # ✔ 不够则重置循环
        if len(unsent) < DAILY_COUNT:
            sent[channel] = []
            unsent = pool

        # ✔ 顺序发布（不是随机）
        selected = unsent[:DAILY_COUNT]

        # 📤 逐条原样复制（包括：图+视频+文本整体）
        for m in selected:

            copy_post(
                channel,      # 发到哪个频道
                channel,      # 从哪个频道复制（同源）
                m["id"]       # 消息ID
            )

            # ✔ 记录已发送
            sent.setdefault(channel, []).append(str(m["id"]))

        save("sent.json", sent)


if __name__ == "__main__":
    main()
