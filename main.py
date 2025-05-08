from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime
from typing import List

app = FastAPI()

# ✅ Allow all CORS (for Netlify front-end)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 🧾 Signal History Memory Store
signal_history = []

# 📥 Order Request Model
class OrderRequest(BaseModel):
    symbol: str
    side: str

# 📤 Signal Data Model
class SignalResponse(BaseModel):
    price: float
    rsi: float
    signal: str

# 🧠 Logic to simulate RSI + Price (Replace with real calculation)
def get_signal(symbol: str):
    import random
    price = round(random.uniform(64000, 64500), 2)
    rsi = round(random.uniform(30, 70), 1)
    signal = "BUY" if rsi < 60 else "SELL"

    # 📌 Add to history
    signal_history.insert(0, {
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "symbol": symbol.upper(),
        "price": price,
        "rsi": rsi,
        "side": "Buy" if signal == "BUY" else "Sell",
        "signal": signal,
    })

    return {"price": price, "rsi": rsi, "signal": signal}

# 🚀 Endpoint 1: Signal Status (GET)
@app.get("/status/{symbol}", response_model=SignalResponse)
def status(symbol: str):
    return get_signal(symbol)

# 🚀 Endpoint 2: Order POST
@app.post("/order")
def place_order(order: OrderRequest):
    return {"message": f"{order.side.upper()} order sent for {order.symbol.upper()}"}

# 🚀 Endpoint 3: Signal History Table
@app.get("/history")
def get_history() -> List[dict]:
    return signal_history
