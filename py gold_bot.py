import MetaTrader5 as mt5
import pandas as pd
import time
import requests

TOKEN = "8622288541:AAEJ4Bzmu4OnsKW4Wr8qUrXJ1YRY--Tl6rM"
CHAT_ID = "5990826600"

def send_telegram(message):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": message}
    requests.post(url, data=data)
def open_trade(signal):

    lot = 0.05
    symbol = "XAUUSD"

    tick = mt5.symbol_info_tick(symbol)

    if signal == "BUY":
        price = tick.ask
        order_type = mt5.ORDER_TYPE_BUY
        sl = price - 5
        tp = price + 10

    else:
        price = tick.bid
        order_type = mt5.ORDER_TYPE_SELL
        sl = price + 5
        tp = price - 10

    request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": lot,
        "type": order_type,
        "price": price,
        "sl": sl,
        "tp": tp,
        "deviation": 20,
        "magic": 123456,
        "comment": "Gold AI Bot",
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_IOC,
    }

    result = mt5.order_send(request)

    print(result)

    send_telegram(f"{signal} XAUUSD | Lot {lot}")
mt5.initialize()
send_telegram("BOT TEST MESSAGE")
send_telegram("GOLD BOT IS CONNECTED")
send_telegram("Telegram connected to Gold Bot")
symbol = "XAUUSD"
timeframe = mt5.TIMEFRAME_M1

def calculate_rsi(data, period=14):
    delta = data.diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)

    avg_gain = gain.rolling(period).mean()
    avg_loss = loss.rolling(period).mean()

    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

while True:

    rates = mt5.copy_rates_from_pos(symbol, timeframe, 0, 100)

    df = pd.DataFrame(rates)

    df['ma_fast'] = df['close'].rolling(5).mean()
    df['ma_slow'] = df['close'].rolling(20).mean()

    df['rsi'] = calculate_rsi(df['close'])

    fast = df['ma_fast'].iloc[-1]
    slow = df['ma_slow'].iloc[-1]
    rsi = df['rsi'].iloc[-1]
    trend_strength = abs(fast - slow)

last_close = df['close'].iloc[-1]
prev_close = df['close'].iloc[-2]

momentum = last_close - prev_close

support = df['low'].rolling(20).min().iloc[-1]
resistance = df['high'].rolling(20).max().iloc[-1]

price = df['close'].iloc[-1]


# BUY logic
if fast > slow and rsi < 40 and momentum > 0 and price > support and trend_strength > 0.5:
    print("AI PRO BUY SIGNAL")

    send_telegram(f"""
BUY XAUUSD
Price: {price}
RSI: {rsi}
Trend Strength: {trend_strength}
""")

    open_trade("BUY")


# SELL logic
elif fast < slow and rsi > 60 and momentum < 0 and price < resistance and trend_strength > 0.5:
    print("AI PRO SELL SIGNAL")

    send_telegram(f"""
SELL XAUUSD
Price: {price}
RSI: {rsi}
Trend Strength: {trend_strength}
""")

    open_trade("SELL")


else:
    print("No strong signal")

    print("---------------------------")

    time.sleep(10)