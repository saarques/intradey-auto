import streamlit as st
from pages import breakout_alerts, option_chain, charts

st.set_page_config(page_title="Intradey Terminal", layout="wide")
st.title("🚀 Intraday Breakout Terminal — Intradey")

tab1, tab2, tab3 = st.tabs(["📈 Breakout Alerts", "📂 Option Chain", "🕒 Chart Analysis"])

with tab1:
    breakout_alerts.render()

with tab2:
    option_chain.render()

with tab3:
    charts.render()
