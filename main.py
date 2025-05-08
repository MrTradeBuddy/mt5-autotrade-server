
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import requests
from datetime import datetime

app = FastAPI()

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Simple Signal Logic based on RSI levels
def get_signal(rsi: float):
    if rsi > 70:
        return "SELL"
    elif rsi < 30:
        return "BUY"
    else:
        return "HOLD"

# Signal History Store
signal_history = []

@app.get("/status/{symbol}")
def get_status(symbol: str):
    try:
        # 1. Fetch current price from Binance
        url = f"https://api.binance.com/api/v3/ticker/price?symbol={symbol.upper()}"
        response = requests.get(url)
        data = response.json()

        price = float(data["price"])
        rsi = round((price % 100) * 1.1, 2)  # Simulated RSI for demo
        signal = get_signal(rsi)

        return {
            "symbol": symbol.upper(),
            "price": price,
            "rsi": rsi,
            "signal": signal
        }
    except Exception as e:
        return {"error": str(e)}

@app.post("/order")
async def place_order(request: Request):
    body = await request.json()
    symbol = body.get("symbol", "BTCUSDT")
    side = body.get("side", "BUY")

    # Simulate order execution
    response = get_status(symbol)
    signal_history.insert(0, {
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "symbol": symbol.upper(),
        "price": response.get("price"),
        "rsi": response.get("rsi"),
        "side": side,
        "signal": response.get("signal")
    })
    return {"message": f"{side} order sent for {symbol}"}

@app.get("/history")
def history():
    return signal_history[:20]
