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
        json.dump(data, f, ensure_ascii=False, indent=2)


def main():

    data = load("data.json", {})
    sent = load("sent.json", {})

    print("📦 CHANNELS:", CHANNELS)
    print("📦 DAILY_COUNT:", DAILY_COUNT)

    for channel in CHANNELS:

        pool = data.get(channel, [])

        print(f"\n📌 频道: {channel}")
        print(f"📦 总内容: {len(pool)}")

        if not pool:
            print("⚠️ 该频道没有数据")
            continue

        sent_ids = set(sent.get(channel, []))

        # ✔ 去重
        unsent = [m for m in pool if str(m["id"]) not in sent_ids]

        print(f"🟡 未发送数量: {len(unsent)}")

        # ✔ 不够则重置
        if len(unsent) < DAILY_COUNT:
            print("♻️ 重置已发送记录")
            sent[channel] = []
            unsent = pool

        selected = unsent[:DAILY_COUNT]

        print(f"📤 本次发送: {len(selected)}")

        for m in selected:

            msg_id = m["id"]

            print(f"➡️ 发送 message_id={msg_id}")

            res = copy_post(
                chat_id=channel,
                from_chat_id=channel,
                message_id=msg_id
            )

            # ❗ Telegram失败检测
            try:
                if not res.json().get("ok"):
                    print("❌ 发送失败:", res.text)
                    continue
            except:
                pass

            sent.setdefault(channel, []).append(str(msg_id))

        save("sent.json", sent)

    print("\n✅ 完成运行")


if __name__ == "__main__":
    main()
