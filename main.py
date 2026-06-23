import time
import json
import asyncio
from datetime import datetime
from zoneinfo import ZoneInfo

from collector import crawl
from ai import train, predict
from telegram import send_message

VN = ZoneInfo("Asia/Ho_Chi_Minh")


def today():
    return datetime.now(VN).strftime("%Y-%m-%d")


def load_storage():
    try:
        with open("storage.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {"last_sent": ""}


def save_storage(data):
    with open("storage.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


storage = load_storage()

print("🚀 XSMB AI v8.3 STARTED")

while True:

    try:

        data = crawl()

        if not data:
            print("⚠️ No data")
            time.sleep(10)
            continue

        model = train(data)
        result = predict(model, data)

        msg = (
            f"<b>"
            f"🚀 XSMB AI v8.3\n\n"
            f"📅 NGÀY: {today()}\n\n"
            f"📊 CONFIDENCE: {result['confidence']}%\n\n"
            f"🎯 BẠCH THỦ: {result['bach_thu']}\n\n"
            f"💥 XIÊN 2: {' - '.join(result['xien2'])}\n\n"
            f"💥 XIÊN 3: {' - '.join(result['xien3'])}\n\n"
            f"🎲 LÔ 3 SỐ:\n{' '.join(result['lo3'])}\n\n"
            f"💣 ĐỀ ĐẶC BIỆT: {result['special']}\n\n"
            f"</b>"
        )

        now = datetime.now(VN)

        if (
            now.hour == 17
            and now.minute == 30
            and storage["last_sent"] != today()
        ):

            print("📢 SEND 17:30 SIGNAL")

            asyncio.run(send_message(msg))

            storage["last_sent"] = today()
            save_storage(storage)

            print("✅ Sent successfully")

        time.sleep(5)

    except Exception as e:
        print("❌ ERROR:", e)
        time.sleep(5)
