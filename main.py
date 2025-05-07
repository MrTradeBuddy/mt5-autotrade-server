from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from order_sender import send_order  # 🔁 Call to MT5 via WebSocket

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class OrderRequest(BaseModel):
    pair: str
    action: str

@app.post("/order")
async def place_order(order: OrderRequest):
    result = send_order(order.pair, order.action)
    return {
        "message": f"{order.action.upper()} order sent for {order.pair}",
        "result": result
    }
from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import json
from websocket_manager import websocket_manager

app = FastAPI()

# ✅ CORS Fix
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Or specify: ["https://autrz.netlify.app"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class OrderRequest(BaseModel):
    pair: str
    action: str

@app.post("/order")
async def place_order(order: OrderRequest):
    message = {
        "symbol": order.pair,
        "action": order.action
    }
    await websocket_manager.send_to_all(json.dumps(message))
    return {"message": f"{order.action.upper()} order sent for {order.pair}"}

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket_manager.connect(websocket)
    try:
        while True:
            await websocket.receive_text()
    except:
        websocket_manager.disconnect(websocket)
