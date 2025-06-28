import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(layout="wide")
st.title("📈 Capital Markets Dashboard")

# Sidebar
st.sidebar.header("Settings")
ticker = st.sidebar.text_input("Enter Ticker Symbol", value="AAPL")
start_date = st.sidebar.date_input("Start Date", value=pd.to_datetime("2023-01-01"))
end_date = st.sidebar.date_input("End Date", value=pd.to_datetime("today"))

# Fetch data
data = yf.download(ticker, start=start_date, end=end_date)

if data.empty:
    st.error("No data found. Please check the ticker.")
else:
    st.subheader(f"{ticker} Closing Price")
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=data.index, y=data['Close'], mode='lines', name='Close Price'))
    st.plotly_chart(fig, use_container_width=True)

    st.subheader(f"{ticker} Summary Stats")
    st.write(data.describe())

import time
from tqdm import tqdm

st.subheader("📊 Top 5 Gainers and Losers (Nasdaq 100)")

nasdaq_tickers = [
    "AAPL", "MSFT", "AMZN", "GOOGL", "META", "TSLA", "NVDA", "PYPL", "INTC", "ADBE",
    "CMCSA", "CSCO", "PEP", "AVGO", "TXN", "COST", "QCOM", "AMGN", "SBUX", "AMD",
    "ISRG", "CHTR", "MDLZ", "BKNG", "FISV", "GILD", "ADP", "INTU", "VRTX", "REGN"
]

@st.cache_data(show_spinner=False)
def get_daily_changes(tickers):
    changes = []
    for ticker in tqdm(tickers):
        df = yf.download(ticker, period='2d', interval='1d', progress=False)
        if len(df) == 2:
            yesterday, today = df['Close'].iloc[0], df['Close'].iloc[1]
            change_pct = ((today - yesterday) / yesterday) * 100
            changes.append((ticker, round(change_pct, 2)))
    return changes

with st.spinner("Loading market movers..."):
    movers = [(symbol, df['change'].iloc[-1]) for symbol, df in some_data.items()]
    movers_sorted = sorted(movers, key=lambda x: x[1], reverse=True)
    top_gainers = movers_sorted[:5]
    top_losers = movers_sorted[-5:]

col1, col2 = st.columns(2)

with col1:
    st.markdown("### 🔼 Top 5 Gainers")
    for ticker, change in top_gainers:
        st.write(f"**{ticker}**: {change}%")

with col2:
    st.markdown("### 🔽 Top 5 Losers")
    for ticker, change in reversed(top_losers):
        st.write(f"**{ticker}**: {change}%")
