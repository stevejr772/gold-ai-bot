import MetaTrader5 as mt5
import pandas as pd
import time

mt5.initialize()

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

    print("Fast MA:", fast)
    print("Slow MA:", slow)
    print("RSI:", rsi)

    if fast > slow and rsi < 30:
        print("🔥 STRONG BUY SIGNAL")

    elif fast < slow and rsi > 70:
        print("🔥 STRONG SELL SIGNAL")

    else:
        print("No strong signal")

    print("---------------------------")

    time.sleep(10)