import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go
import numpy as np
import pytz
from datetime import datetime
import math

st.set_page_config(page_title="HG BANKNIFTY BOT", layout="wide")

st.markdown("""
<style>
.stApp { background:#d5dbe8; }
.panel { background:#e8ecf3; border:1px solid #9aa4b8; padding:6px; }
</style>
""", unsafe_allow_html=True)

ist = pytz.timezone('Asia/Kolkata')
now = datetime.now(ist)

st.markdown(f"""
<div style="background:#c2c9d9; border:1px solid #8a95ad; padding:3px 6px; font-size:10px;">
HG - hot-garbage // BANKNIFTY 5M BOT - LIVE DIRECTIONAL - {now.strftime('%H:%M:%S')} UTC
</div>
<div style="background:#ff3b3b; color:white; font-size:9px; padding:2px 6px">
LIVE FEED 5M 10:00AM-10:05AM Up 0.42 Dn 0.50
</div>
""", unsafe_allow_html=True)

@st.cache_data(ttl=120)
def get_nifty():
    try:
        t = yf.Ticker("^NSEI")
        df = t.history(period="1d", interval="5m")
        return df
    except:
        return pd.DataFrame()

df_nifty = get_nifty()

c1, c2, c3 = st.columns([0.9, 1.1, 2])

with c1:
    st.markdown("""
    <div class="panel">
    <div style="font-size:9px"><b>WALLET - 0X3319--9E2E LIVE</b></div>
    <div style="font-size:32px; color:#00aa00"><b>+$219,991</b></div>
    <div style="font-size:8px">126011 FILLS - WIN RATE 53.9% - EDGE +5.82c</div>
    <div style="font-size:8px; margin-top:4px">DRAWDOWN RISK 2.2/10 SAFE</div>
    </div>
    """, unsafe_allow_html=True)

with c2:
    if not df_nifty.empty:
        fig = go.Figure()
        fig.add_trace(go.Candlestick(
            x=df_nifty.index,
            open=df_nifty['Open'],
            high=df_nifty['High'],
            low=df_nifty['Low'],
            close=df_nifty['Close']
        ))
        fig.update_layout(
            height=220,
            margin=dict(l=0, r=0, t=30, b=0),
            paper_bgcolor="#e8ecf3",
            plot_bgcolor="#e8ecf3"
        )
        fig.update_layout(title_text="BTC PRICE NIFTY 5M")
        fig.update_xaxes(rangeslider_visible=False)
        st.plotly_chart(fig, use_container_width=True)

with c3:
    st.markdown("""
    <div class="panel" style="font-size:9px">
    <b>MARKET LIFECYCLE</b><br>
    <div style="height:70px; background:#d0d0d0; margin-top:6px"></div>
    </div>
    <div class="panel" style="font-size:9px; margin-top:6px">
    <b>RESOLUTION GRID</b><br>
    <div style="display:grid; grid-template-columns:repeat(6,1fr); gap:3px; margin-top:6px">
    <div style="background:#a8e6a3; text-align:center; padding:3px">$1</div>
    <div style="background:#a8e6a3; text-align:center; padding:3px">87c</div>
    <div style="background:#f0a8a8; text-align:center; padding:3px">26c</div>
    <div style="background:#f0a8a8; text-align:center; padding:3px">45c</div>
    <div style="background:#a8e6a3; text-align:center; padding:3px">63c</div>
    <div style="background:#a8e6a3; text-align:center; padding:3px">52c</div>
    </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("""<div class="panel" style="padding:4px 6px; font-size:9px"><b>NEURAL SHELL</b> MARKET FEED - FEATURE LAYER - DECISION CORE</div>""", unsafe_allow_html=True)

fig = go.Figure()

names = ["NIFTY 5M", "BANK 5M", "ORDER BOOK", "TAPE", "VOLATILITY", "REP PRICE", "INVENTORY"]
vals = [77, 15, 33, 43, 28, 71, 100]
ypos = [0.95, 0.8, 0.65, 0.5, 0.35, 0.2, 
