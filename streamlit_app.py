import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go
import numpy as np
import pytz
from datetime import datetime
import math

st.set_page_config(page_title="HG BANKNIFTY BOT", layout="wide")

st.markdown("<style>.stApp{background:#d5dbe8;}.panel{background:#e8ecf3;border:1px solid #9aa4b8;padding:6px;}</style>", unsafe_allow_html=True)

ist = pytz.timezone('Asia/Kolkata')
now = datetime.now(ist)

st.markdown(f"<div style='background:#c2c9d9;padding:3px;font-size:10px;'>HG BANKNIFTY 5M BOT - {now.strftime('%H:%M:%S')} UTC</div><div style='background:#ff3b3b;color:white;font-size:9px;padding:2px;'>LIVE FEED 5M Up 0.42 Dn 0.50</div>", unsafe_allow_html=True)

@st.cache_data(ttl=120)
def get_nifty():
    t = yf.Ticker("^NSEI")
    df = t.history(period="1d", interval="5m")
    return df

df_nifty = get_nifty()
c1, c2, c3 = st.columns([0.9, 1.1, 2])

with c1:
    st.markdown("<div class='panel'><div style='font-size:9px'><b>WALLET LIVE</b></div><div style='font-size:32px;color:#00aa00'><b>+$219,991</b></div><div style='font-size:8px'>126011 FILLS - WIN 53.9% - EDGE +5.82c</div></div>", unsafe_allow_html=True)

with c2:
    if not df_nifty.empty:
        fig = go.Figure()
        fig.add_trace(go.Candlestick(x=df_nifty.index, open=df_nifty['Open'], high=df_nifty['High'], low=df_nifty['Low'], close=df_nifty['Close']))
        fig.update_layout(height=220, margin=dict(l=0, r=0, t=30, b=0), paper_bgcolor="#e8ecf3", plot_bgcolor="#e8ecf3")
