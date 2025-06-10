import streamlit as st
import yfinance as yf
from datetime import datetime, timedelta
import pandas as pd

def render():
    st.header("📈 Breakout Alerts")

    SYMBOL = "RELIANCE.NS"  # Changed from ^NSEI
    now = datetime.now()
    past = now - timedelta(days=5)

    # Download clean 5-minute data
    data = yf.download(SYMBOL, start=past, end=now, interval="5m", progress=False, auto_adjust=False)

    if data.empty or data.shape[1] > 10:
        st.error("❌ Could not fetch valid intraday data. Please try a different symbol.")
        return

    data = data.dropna()

    # Typical Price
    data["TP"] = (data["High"] + data["Low"] + data["Close"]) / 3

    # VWAP calculation
    vwap_numerator = (data["TP"] * data["Volume"]).cumsum()
    vwap_denominator = data["Volume"].cumsum()
    data["VWAP"] = vwap_numerator / vwap_denominator

    # Breakout logic
    last = data.iloc[-1]
    prev = data.iloc[-2]

    if last["Close"] > last["VWAP"] and last["Volume"] > prev["Volume"]:
        st.success(f"🚀 Breakout signal at {last.name.strftime('%Y-%m-%d %H:%M')} — Price: {last['Close']:.2f}")
    else:
        st.info("📊 No breakout signal yet.")
