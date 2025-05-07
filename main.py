from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import requests
from order_sender import send_order  # This handles real order execution

app = FastAPI()

# ✅ Allow frontend from Netlify
origins = [
    "https://autrz.netlify.app",
    "http://localhost:3000"  # for local dev
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Live BTCUSDT Price + RSI Signal API
@app.get("/status/btcusdt")
def get_btc_status():
    try:
        # Live price from Binance
        price_response = requests.get("https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT")
        price_data = price_response.json()
        price = float(price_data["price"])

        # Dummy RSI logic (replace with real calculation or TradingView webhook logic)
        rsi = 68.7  # for example
        signal = "BUY" if rsi > 60 else "SELL" if rsi < 40 else "WAIT"

        return {
            "price": round(price, 2),
            "rsi": rsi,
            "signal": signal
        }
    except Exception as e:
        return {
            "price": None,
            "rsi": None,
            "signal": "Error",
            "error": str(e)
        }

# ✅ Real Trade Order API (Buy/Sell from UI)
@app.post("/order")
async def place_order(req: Request):
    try:
        body = await req.json()
        symbol = body.get("symbol")
        side = body.get("side")

        # Pass to WebSocket handler (MT5 or Exness bridge)
        result = send_order(symbol, side)

        return {"message": f"{side.upper()} order sent for {symbol}", "status": "success"}
    except Exception as e:
        return {"message": "Error placing order", "error": str(e)}
