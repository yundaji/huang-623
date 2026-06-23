import json
from config import CHANNELS, DAILY_COUNT
from tg import copy_posts


def load(file, default):
    try:
        with open(file, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return default


def save(file, data):
    with open(file, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def main():

    data = load("data.json", {})
    sent = load("sent.json", {})

    print("🚀 START BOT")

    for channel in CHANNELS:

        pool = data.get(channel, [])

        print(f"\n📌 频道: {channel}")
        print(f"📦 总帖子: {len(pool)}")

        if not pool:
            print("⚠️ 空频道")
            continue

        sent_ids = set(sent.get(channel, []))

        # ✔ 去重
        unsent = [m for m in pool if str(m["id"]) not in sent_ids]

        # ✔ 不够则重置
        if len(unsent) < DAILY_COUNT:
            print("♻️ 重置去重池")
            sent[channel] = []
            unsent = pool

        selected = unsent[:DAILY_COUNT]

        # ✅ 关键：一次性发送（不拆组）
        message_ids = [m["id"] for m in selected]

        print("📤 发送 message_ids:", message_ids)

        copy_posts(
            chat_id=channel,
            from_chat_id=channel,
            message_ids=message_ids
        )

        # ✔ 记录已发送
        sent.setdefault(channel, [])
        sent[channel].extend([str(i) for i in message_ids])

        save("sent.json", sent)

    print("✅ DONE")


if __name__ == "__main__":
    main()
