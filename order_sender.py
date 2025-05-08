import MetaTrader5 as mt5

def send_order(symbol, action):
    if not mt5.initialize(login=12345678, server="Exness-Real", password="your_password"):
        return {"message": "MT5 init failed"}
    
    lot = 0.1
    order_type = mt5.ORDER_TYPE_BUY if action == "buy" else mt5.ORDER_TYPE_SELL

    request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": lot,
        "type": order_type,
        "price": mt5.symbol_info_tick(symbol).ask,
        "deviation": 10,
        "magic": 234000,
        "comment": "AutoTrade",
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_IOC,
    }

    result = mt5.order_send(request)
    mt5.shutdown()

    return {"message": f"{action.upper()} order {'success' if result.retcode == mt5.TRADE_RETCODE_DONE else 'failed'}"}
