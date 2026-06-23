import json
import random
from config import CHANNELS, DAILY_COUNT
from tg import send_message

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

        for msg in selected:

            send_message(channel, msg["id"], channel)

            sent.setdefault(channel, []).append(str(msg["id"]))

        save("sent.json", sent)


if __name__ == "__main__":
    main()
