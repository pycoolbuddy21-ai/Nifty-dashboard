import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go
import numpy as np
import pytz
from datetime import datetime
import math

st.set_page_config(page_title="HG - BANKNIFTY BOT", layout="wide")

st.markdown("""
<style>
.stApp { background:#d5dbe8; }
.panel { background:#e8ecf3; border:1px solid #9aa4b8; padding:6px; }
.tile-green { background:#a8e6a3; border:1px solid #5a5; text-align:center; padding:3px; font-weight:bold; font-size:11px }
.tile-red { background:#f0a8a8; border:1px solid #a55; text-align:center; padding:3px; font-weight:bold; font-size:11px }
</style>
""", unsafe_allow_html=True)

ist = pytz.timezone('Asia/Kolkata')
now = datetime.now(ist)

st.markdown(f"""
<div style="background:#c2c9d9; border:1px solid #8a95ad; padding:3px 6px; font-size:10px; display:flex; justify-content:space-between">
<div><span style="background:#2a2f3d; color:white; padding:2px 6px; border-radius:3px">HG</span> - LIVE DIRECTIONAL - HEDGE 53% UP - SETS 41%: $1 46.3k &nbsp; <b>hot-garbage // BANKNIFTY 5M BOT</b></div>
<div style="text-align:right">NIFTY SPOT $63,006 &nbsp; NIFTY 5M 0.97 &nbsp; BANK 5M 1.00 &nbsp; SET EDGE 5.81c<br>{now.strftime('%H:%M:%S')} UTC</div>
</div>
<div style="background:#ff3b3b; color:white; font-size:9px; padding:2px 6px">● LIVE FEED 5M 10:00AM-10:05AM - Up 0.42 - Dn 0.50 - FLIP SIDE - BANK 5M 9:55AM-10:00AM - SWITCH TO DOWN @ $0.42 -</div>
""", unsafe_allow_html=True)

@st.cache_data(ttl=120)
def get_nifty():
    try:
        t=yf.Ticker("^NSEI")
        df=t.history(period="1d", interval="5m")
        return df
    except:
        return pd.DataFrame()

df_nifty=get_nifty()

c1,c2,c3=st.columns([0.9,1.1,2])

with c1:
    st.markdown("""
    <div class="panel">
    <div style="display:flex; justify-content:space-between; font-size:9px"><b>● WALLET - 0X3319--9E2E</b><span style="background:black; color:#00ff00; padding:0 4px">LIVE</span></div>
    <div style="font-size:9px; color:#666">0x3319--9E2E</div>
    <div style="font-size:9px; margin-top:6px">ALL-TIME PNL</div>
    <div style="font-size:32px; font-weight:bold; color:#00aa00; line-height:32px">+$219,991</div>
    <div style="font-size:8px">ALL TIME - 126,011 FILLS</div>
    <div style="display:flex; gap:12px; font-size:8px; margin-top:8px; border-top:1px solid #aaa; padding-top:4px">
    <div>FILLS<br><b>126,011</b></div><div>WIN RATE<br><b>53.9%</b></div><div>SET EDGE<br><b>+5.82c</b></div>
    </div>
    <div style="font-size:8px; margin-top:4px">DRAWDOWN RISK <b>2.2/10</b> <span style="background:#ffd54f; padding:1px 4px">SAFE</span></div>
    <hr style="margin:6px 0">
    <div style="font-size:8px"><b>+ INVENTORY & FLOW</b><br>DIRECTIONAL BIAS 56% UP<br><div style="height:8px; display:flex; margin:2px 0"><div style="width:56%; background:green"></div><div style="width:44%; background:red"></div></div>
    MATCHED / RESIDUAL 86% / 14%<br><div style="height:8px; display:flex; margin:2px 0; border:1px solid #000"><div style="width:86%; background:orange"></div><div style="width:14%; background:#ccc"></div></div></div>
    </div>
    """, unsafe_allow_html=True)

with c2:
    if not df_nifty.empty:
        fig=go.Figure(data=[go.Candlestick(x=df_nifty.index, open=df_nifty['Open'], high=df_nifty['High'], low=df_nifty['Low'], close=df_nifty['Close'])])
        fig.update_layout(height=220, margin=dict(l=0,r=0,t=25,b=0), paper_bgcolor="#e8ecf3", plot_bgcolor="#e8ecf3", font=dict(size=8), title=dict(text="● BTC PRICE NIFTY - 5M $63,006", font=dict(size=9)), xaxis_rangeslider
