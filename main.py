import json
from config import CHANNELS, DAILY_COUNT
from tg import send_group, send_single


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

    channel_index = 0

    for channel in CHANNELS:

        pool = data.get(channel, [])

        print(f"\n📌 频道: {channel}")
        print(f"📦 内容总数: {len(pool)}")

        if not pool:
            continue

        sent_ids = set(sent.get(channel, []))

        unsent = []

        # ✔ 去重逻辑（支持 album）
        for item in pool:
            if item["type"] == "album":
                key = f"album:{item['message_ids'][0]}"
            else:
                key = f"msg:{item['message_id']}"

            if key not in sent_ids:
                unsent.append(item)

        # ✔ 不够则重置
        if len(unsent) < DAILY_COUNT:
            print("♻️ 重置去重记录")
            sent[channel] = []
            unsent = pool

        selected = unsent[:DAILY_COUNT]

        print(f"📤 本次发送: {len(selected)}")

        for item in selected:

            # 🔥 album（图集 / 视频组）
            if item["type"] == "album":

                print("🖼 发送图集:", item["message_ids"])

                ok = send_group(channel, channel, item["message_ids"])

                if ok:
                    sent.setdefault(channel, []).append(
                        f"album:{item['message_ids'][0]}"
                    )

            # 🔥 单条
            else:

                print("📄 发送单条:", item["message_id"])

                ok = send_single(channel, channel, item["message_id"])

                if ok:
                    sent.setdefault(channel, []).append(
                        f"msg:{item['message_id']}"
                    )

        save("sent.json", sent)

    print("\n✅ 完成运行")


if __name__ == "__main__":
    main()
