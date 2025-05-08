from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

# ✅ Allow frontend hosted on Netlify to access backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://autrz.netlify.app"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# 🛠️ Structure of order request
class OrderRequest(BaseModel):
    symbol: str
    side: str  # "buy" or "sell"

@app.get("/")
def read_root():
    return {"message": "AutoTrade API is live!"}

# ✅ API to get signal status
@app.get("/status/{symbol}")
def get_status(symbol: str):
    symbol = symbol.upper()
    dummy_data = {
        "BTCUSDT": {"price": 64321.22, "rsi": 61.3, "signal": "BUY"},
        "EURUSD": {"price": 1.0855, "rsi": 52.0, "signal": "WAIT"},
        "XAUUSD": {"price": 2320.75, "rsi": 47.9, "signal": "SELL"}
    }

    if symbol in dummy_data:
        return dummy_data[symbol]
    else:
        return {"error": "No data for this symbol"}

# ✅ API to place Buy/Sell order
@app.post("/order")
def place_order(req: OrderRequest):
    return {"message": f"{req.side.upper()} order sent for {req.symbol.upper()}"}
from order_sender import send_order

@app.post("/order")
def place_order(req: Request):
    data = asyncio.run(req.json())
    symbol = data.get("symbol")
    action = data.get("action")
    return send_order(symbol, action)
