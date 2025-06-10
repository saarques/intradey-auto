# 📈 NIFTY Intraday Momentum Breakout Dashboard

This Streamlit app provides real-time analysis of NIFTY 50 using live price action and Option Chain data. It detects potential intraday breakouts based on VWAP, candlestick structure, and OI signals.

## 🚀 Features
- Live 1-min, 5-min, 15-min candlestick charts with VWAP
- Breakout detection checklist
- Real-time Option Chain with OI, PCR per strike
- Alerts for possible breakout entries

## 🧰 Technologies
- Python
- Streamlit
- Plotly
- yfinance
- NSE Option Chain API

## 🛠️ Setup Instructions

### 1. Clone this repo
```bash
git clone https://github.com/saarques/intradey.git
cd intradey
```

### 2. Install requirements
```bash
pip install -r requirements.txt
```

### 3. Run the app locally
```bash
streamlit run main.py
```

## ☁️ Deploy on Streamlit Cloud
1. Push this code to a public GitHub repo
2. Go to [https://streamlit.io/cloud](https://streamlit.io/cloud)
3. Connect your GitHub account and select this repo
4. Use `main.py` as the entry point
5. Done!

---

## 📬 Contact
Want to extend this for BankNIFTY, Stocks, or Alerts? Message me!