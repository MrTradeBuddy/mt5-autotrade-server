from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI()

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
