import streamlit as st
import yfinance as yf
from datetime import datetime, timedelta
import pandas as pd

def render():
    st.header("📈 Breakout Alerts")

    SYMBOL = "^NSEI"
    now = datetime.now()
    past = now - timedelta(days=2)
    data = yf.download(SYMBOL, start=past, end=now, interval="5m")

    data["TP"] = (data["High"] + data["Low"] + data["Close"]) / 3
    data["VWAP"] = (data["TP"] * data["Volume"]).cumsum() / data["Volume"].cumsum()

    last = data.iloc[-1]
    prev = data.iloc[-2]

    st.metric("Last Price", round(last["Close"], 2))
    st.metric("VWAP", round(last["VWAP"], 2))
    st.metric("Volume", int(last["Volume"]))

    checklist = {
        "Price > VWAP": last["Close"] > last["VWAP"],
        "Bullish Candle": last["Close"] > last["Open"],
        "Higher High": last["High"] > prev["High"],
        "VWAP Slope Up": last["VWAP"] > data["VWAP"].iloc[-3]
    }

    st.write("### 🔍 Signal Conditions")
    st.dataframe(pd.DataFrame(checklist.items(), columns=["Condition", "Met?"]))

    if all(checklist.values()):
        st.success("✅ Breakout Signal Detected")
    else:
        st.info("ℹ️ No breakout yet, keep monitoring.")
