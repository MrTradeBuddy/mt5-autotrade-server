from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

app = FastAPI()

# ✅ Add CORS settings here:
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Or set to your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/last-signal")
async def last_signal():
    return JSONResponse(content={
        "payload": {
            "symbol": "BTCUSDT",
            "price": 62000,
            "type": "buy",
            "amount": 0.1
        }
    })
