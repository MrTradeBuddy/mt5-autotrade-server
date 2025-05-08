from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from order_sender import send_order  # ✅ MT5 இல்லாத version

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change to Netlify URL for security
    allow_methods=["*"],
    allow_headers=["*"],
)

class OrderRequest(BaseModel):
    symbol: str
    side: str

@app.get("/")
def read_root():
    return {"message": "AutoTrade API is live!"}

@app.get("/status/{symbol}")
def get_status(symbol: str):
    symbol = symbol.upper()
    dummy_data = {
        "BTCUSDT": {"price": 64321.22, "rsi": 61.3, "signal": "BUY"},
        "EURUSD": {"price": 1.0855, "rsi": 52.0, "signal": "WAIT"},
        "XAUUSD": {"price": 2320.75, "rsi": 47.9, "signal": "SELL"}
    }

    return dummy_data.get(symbol, {"error": "No data for this symbol"})

@app.post("/order")
def place_order(req: OrderRequest):
    return send_order(req.symbol, req.side)
