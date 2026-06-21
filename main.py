from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse
from ai import train, predict
from collector import crawl
import asyncio

app = FastAPI()

model, data = train()

@app.get("/")
def home():
    return HTMLResponse(open("templates/dashboard.html","r",encoding="utf-8").read())

@app.websocket("/ws")
async def ws(websocket: WebSocket):

    await websocket.accept()

    global data

    while True:

        try:
            new_data = crawl()

            if new_data:
                data = new_data

            result = predict(model, data)

            await websocket.send_json(result)

            await asyncio.sleep(5)

        except:
            await asyncio.sleep(5)
