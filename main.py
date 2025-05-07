from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from order_sender import send_order  # Exness WebSocket trigger

app = FastAPI()

# ✅ CORS Setup (Allow Netlify Frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change this to ["https://autrz.netlify.app"] for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ API Root Test
@app.get("/")
def root():
    return {"status": "Backend Live ✅"}

# ✅ Order Request Model
class OrderRequest(BaseModel):
    pair: str
    action: str

# ✅ POST Order Trigger to MT5/Exness
@app.post("/order")
async def place_order(order: OrderRequest):
    result = send_order(order.pair, order.action)
    return {
        "message": f"{order.action.upper()} order sent for {order.pair}",
        "result": result
    }

# ✅ GET Signal Status for UI
@app.get("/status/btcusdt")
def get_btc_status():
    return {
        "price": 62753.45,  # Live price or test value
        "rsi": 72.1,
        "signal": "BUY"
    }
