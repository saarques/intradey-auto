import streamlit as st
import yfinance as yf
from datetime import datetime, timedelta
import plotly.graph_objs as go

def plot(df, title):
    fig = go.Figure()
    fig.add_trace(go.Candlestick(x=df.index,
                                 open=df["Open"],
                                 high=df["High"],
                                 low=df["Low"],
                                 close=df["Close"],
                                 name="Candles"))
    df["TP"] = (df["High"] + df["Low"] + df["Close"]) / 3
    df["VWAP"] = (df["TP"] * df["Volume"]).cumsum() / df["Volume"].cumsum()
    fig.add_trace(go.Scatter(x=df.index, y=df["VWAP"], name="VWAP", line=dict(color="blue")))
    fig.update_layout(title=title, xaxis_rangeslider_visible=False)
    st.plotly_chart(fig, use_container_width=True)

def render():
    st.header("🕒 Multi-timeframe Chart Analysis")
    SYMBOL = "^NSEI"
    now = datetime.now()
    past = now - timedelta(days=2)

    with st.spinner("Fetching charts..."):
        data_1m = yf.download(SYMBOL, start=past, end=now, interval="1m")
        data_5m = yf.download(SYMBOL, start=past, end=now, interval="5m")
        data_15m = yf.download(SYMBOL, start=past, end=now, interval="15m")

    with st.expander("1-Minute Chart"):
        plot(data_1m[-100:], "NIFTY 1-Min Chart")
    with st.expander("5-Minute Chart"):
        plot(data_5m[-100:], "NIFTY 5-Min Chart")
    with st.expander("15-Minute Chart"):
        plot(data_15m[-100:], "NIFTY 15-Min Chart")
