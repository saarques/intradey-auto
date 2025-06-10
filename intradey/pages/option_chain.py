import streamlit as st
import requests
import pandas as pd

def render():
    st.header("📂 Option Chain Viewer")
    url = "https://www.nseindia.com/api/option-chain-indices?symbol=NIFTY"

    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept": "application/json"
    }

    try:
        res = requests.get(url, headers=headers, timeout=10)
        data = res.json()
        df = pd.DataFrame(data['records']['data'])
        oc_filtered = df[["strikePrice", "CE", "PE"]].dropna()
        ce_data = pd.DataFrame([d['CE'] for d in oc_filtered["CE"]])
        pe_data = pd.DataFrame([d['PE'] for d in oc_filtered["PE"]])
        combined_df = pd.DataFrame({
            "Strike": oc_filtered["strikePrice"].values,
            "CE OI": ce_data["openInterest"].values,
            "PE OI": pe_data["openInterest"].values,
            "PCR": pe_data["openInterest"].values / (ce_data["openInterest"].values + 1)
        })
        st.dataframe(combined_df.sort_values("Strike"))
    except Exception as e:
        st.error(f"⚠️ Error fetching Option Chain: {e}")
