import streamlit as st
import MetaTrader5 as mt5

st.title("Gold AI Trading Bot Dashboard")

mt5.initialize()

account = mt5.account_info()

st.write("Balance:", account.balance)
st.write("Equity:", account.equity)

positions = mt5.positions_get()

if positions:
    st.subheader("Open Trades")
    for pos in positions:
        st.write(f"{pos.symbol} | Lot: {pos.volume} | Profit: {pos.profit}")
else:
    st.write("No open trades")

st.success("Bot is running")