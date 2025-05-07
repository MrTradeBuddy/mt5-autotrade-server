from fastapi import FastAPI, Request
from pydantic import BaseModel
import random

app = FastAPI()

# Mock trading logic
def get_fake_data(pair):
    return {
        "pair": pair.upper(),
        "price": round(random.uniform(1000, 65000), 2),
        "rsi": round(random.uniform(10, 90), 2),
        "signal": random.choice(["Buy", "Sell", "Wait"])
    }

class OrderRequest(BaseModel):
    pair: str
    action: str

@app.get("/status/{pair}")
async def get_status(pair: str):
    data = get_fake_data(pair)
    return data

@app.post("/order")
async def place_order(order: OrderRequest):
    # You can integrate Binance/Exness API here
    return {"message": f"{order.action.upper()} order placed for {order.pair}"}
