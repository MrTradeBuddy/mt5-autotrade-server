from fastapi import FastAPI, WebSocket
from pydantic import BaseModel
import json
from websocket_manager import websocket_manager

app = FastAPI()

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
