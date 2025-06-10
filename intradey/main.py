import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
import requests
from datetime import datetime, timedelta

# --- Config ---
SYMBOL = "^NSEI"
EXPIRY_DATE = "2024-06-13"
NSE_OPTION_CHAIN_URL = "https://www.nseindia.com/api/option-chain-indices?symbol=NIFTY"

st.set_page_config(page_title="NIFTY Breakout Dashboard", layout="wide")
st.title("📈 NIFTY Intraday Momentum Breakout Dashboard")

@st.cache_data(ttl=60)
def fetch_candles():
    now = datetime.now()
    past = now - timedelta(days=2)
    data_1m = yf.download(SYMBOL, start=past, end=now, interval="1m")
    data_5m = yf.download(SYMBOL, start=past, end=now, interval="5m")
    data_15m = yf.download(SYMBOL, start=past, end=now, interval="15m")
    return data_1m, data_5m, data_15m

def calculate_vwap(df):
    df["TP"] = (df["High"] + df["Low"] + df["Close"]) / 3
    df["VWAP"] = (df["TP"] * df["Volume"]).cumsum() / df["Volume"].cumsum()
    return df

@st.cache_data(ttl=120)
def fetch_option_chain():
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept": "application/json",
    }
    try:
        res = requests.get(NSE_OPTION_CHAIN_URL, headers=headers, timeout=10)
        data = res.json()
        df = pd.DataFrame(data['records']['data'])
        return df
    except Exception as e:
        return pd.DataFrame()

def plot_chart(df, title):
    import plotly.graph_objs as go
    fig = go.Figure()
    fig.add_trace(go.Candlestick(x=df.index, open=df['Open'], high=df['High'],
                                 low=df['Low'], close=df['Close'], name='Candles'))
    if "VWAP" in df:
        fig.add_trace(go.Scatter(x=df.index, y=df['VWAP'], mode='lines', name='VWAP', line=dict(color='blue')))
    fig.update_layout(title=title, xaxis_rangeslider_visible=False)
    st.plotly_chart(fig, use_container_width=True)

st.subheader("📊 Price Action")
data_1m, data_5m, data_15m = fetch_candles()
data_1m = calculate_vwap(data_1m)
data_5m = calculate_vwap(data_5m)
data_15m = calculate_vwap(data_15m)

with st.expander("1-Min Chart"):
    plot_chart(data_1m[-100:], "NIFTY 1-Min Chart")
with st.expander("5-Min Chart"):
    plot_chart(data_5m[-100:], "NIFTY 5-Min Chart")
with st.expander("15-Min Chart"):
    plot_chart(data_15m[-100:], "NIFTY 15-Min Chart")

st.subheader("✅ Breakout Checklist")
last_price = data_5m["Close"].iloc[-1]
last_vwap = data_5m["VWAP"].iloc[-1]

checklist = {
    "Price > VWAP (5-min)": last_price > last_vwap,
    "Bullish candle (5-min)": data_5m["Close"].iloc[-1] > data_5m["Open"].iloc[-1],
    "Higher High formed": data_5m["High"].iloc[-1] > data_5m["High"].iloc[-2],
    "VWAP upward slope": data_5m["VWAP"].iloc[-1] > data_5m["VWAP"].iloc[-3]
}
st.dataframe(pd.DataFrame(checklist.items(), columns=["Condition", "Met? "]))

if all(checklist.values()):
    st.success("🚀 Breakout Confirmed — Consider Entry (watch OI data)")
else:
    st.warning("⏳ Breakout Not Yet Confirmed")

st.subheader("📂 Option Chain Snapshot")
oc_df = fetch_option_chain()

if not oc_df.empty:
    oc_filtered = oc_df[["strikePrice", "CE", "PE"]].dropna()
    ce_data = pd.DataFrame([d['CE'] for d in oc_filtered["CE"]])
    pe_data = pd.DataFrame([d['PE'] for d in oc_filtered["PE"]])
    combined_df = pd.DataFrame({
        "Strike": oc_filtered["strikePrice"].values,
        "CE OI": ce_data["openInterest"].values,
        "PE OI": pe_data["openInterest"].values,
        "PCR": pe_data["openInterest"].values / (ce_data["openInterest"].values + 1)
    })
    st.dataframe(combined_df.sort_values("Strike"))
else:
    st.error("⚠️ Unable to fetch Option Chain data. Please retry later.")
