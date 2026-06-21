from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse
from ai import train, predict
from collector import crawl
from datetime import datetime
from zoneinfo import ZoneInfo
import asyncio
import json

app = FastAPI()

VN = ZoneInfo("Asia/Ho_Chi_Minh")

last_sent = None

def today():
    return datetime.now(VN).strftime("%Y-%m-%d")

def hour_min():
    now = datetime.now(VN)
    return now.hour, now.minute

@app.get("/")
def home():
    return HTMLResponse(open("templates/dashboard.html","r",encoding="utf-8").read())

@app.websocket("/ws")
async def ws(websocket: WebSocket):

    await websocket.accept()

    global last_sent

    while True:

        data = crawl()
        model = train(data)
        result = predict(model, data)

        await websocket.send_json(result)

        # =========================
        # ⏰ AUTO 17:00 DAILY SEND
        # =========================
        h, m = hour_min()
        d = today()

        if h == 17 and m == 0 and last_sent != d:

            print("📢 SEND 17:00 SIGNAL")

            # (ở đây bạn có thể add Telegram send)
            await websocket.send_json({
                **result,
                "event": "AUTO_17:00"
            })

            last_sent = d

        await asyncio.sleep(5)
