@app.route("/mt5-bridge", methods=["POST"])
def bridge():
    data = request.json
    print("📩 Received:", data)

    if data.get("type") == "price_update":
        symbol = data["payload"]["symbol"]
        price = float(data["payload"]["price"])

        if symbol == "EURUSD" and price < 1.0780:
            return jsonify({
                "type": "trade_request",
                "payload": {
                    "symbol": symbol,
                    "type": "buy",
                    "amount": "0.01",
                    "price": str(price)
                }
            })
    return jsonify({"type": "no_trade"})
