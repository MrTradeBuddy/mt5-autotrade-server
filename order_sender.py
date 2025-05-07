import websocket
import json

WS_SERVER_URL = "ws://localhost:3000"  # Replace with your MT5 WebSocket

def send_order(symbol, action):
    try:
        ws = websocket.create_connection(WS_SERVER_URL)
        message = {
            "symbol": symbol,
            "action": action
        }
        ws.send(json.dumps(message))
        response = ws.recv()
        ws.close()
        return response
    except Exception as e:
        return str(e)
