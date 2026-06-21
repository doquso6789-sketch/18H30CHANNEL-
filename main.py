import time
import json
from datetime import datetime
from zoneinfo import ZoneInfo

from collector import crawl
from ai import train, predict
from telegram import send_message

VN = ZoneInfo("Asia/Ho_Chi_Minh")

def today():
    return datetime.now(VN).strftime("%Y-%m-%d")

def now_time():
    n = datetime.now(VN)
    return n.hour, n.minute

# =========================
# LOAD STORAGE
# =========================
def load_storage():
    try:
        with open("storage.json","r") as f:
            return json.load(f)
    except:
        return {"last_sent": ""}

def save_storage(data):
    with open("storage.json","w") as f:
        json.dump(data,f)

storage = load_storage()

print("🚀 XSMB AI v8.3 STARTED")

# =========================
# LOOP
# =========================
while True:

    try:

        data = crawl()

        if len(data) == 0:
            print("⚠️ no data")
            time.sleep(10)
            continue

        model = train(data)
        result = predict(model, data)

        # =====================
        # FORMAT MESSAGE
        # =====================
        msg = f"""
🚀 <b>XSMB AI v8.3</b>

📊 CONFIDENCE: {result['confidence']}

🎯 BẠCH THỦ: {result['bach_thu']}

🔗 XIÊN 2: {' - '.join(result['xien2'])}

🔗 XIÊN 3: {' - '.join(result['xien3'])}

🎲 LÔ 3 SỐ:
{' '.join(result['lo3'])}

👑 ĐỀ ĐẶC BIỆT: {result['special']}
"""

        # =====================
        # ⏰ AUTO 17:00
        # =====================
        h = datetime.now(VN).hour
        m = datetime.now(VN).minute

        if h == 17 and m == 0:

            if storage["last_sent"] != today():

                print("📢 SEND 17:00 SIGNAL")

                send_message(msg)

                storage["last_sent"] = today()
                save_storage(storage)

        time.sleep(5)

    except Exception as e:
        print("ERROR:", e)
        time.sleep(5)
