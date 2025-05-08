def send_order(symbol, side):
    return {
        "message": f"🧪 Simulated {side.upper()} order sent for {symbol.upper()}",
        "status": "success"
    }
