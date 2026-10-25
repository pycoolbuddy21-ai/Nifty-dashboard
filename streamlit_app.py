import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go
import numpy as np
import pytz
from datetime import datetime
import math

st.set_page_config(page_title="HG BANKNIFTY BOT", layout="wide")

st.markdown("<style>.stApp{background:#d5dbe8;}.panel{background:#e8ecf3;border:1px solid #9aa4b8;padding:6px;border-radius:4px;}</style>", unsafe_allow_html=True)

ist = pytz.timezone('Asia/Kolkata')
now = datetime.now(ist)

st.markdown(f"<div style='background:#c2c9d9;padding:6px;font-size:11px;border:1px solid #8a95ad;'><b>HG - hot-garbage // BANKNIFTY 5M BOT</b> - LIVE DIRECTIONAL - {now.strftime('%d %b %H:%M:%S')} IST</div><div style='background:#ff3b3b;color:white;font-size:10px;padding:2px 6px;'>LIVE FEED 5M 10:00-10:05 Up 0.42 Dn 0.50 FLIP SIDE BANK 5M 9:55-10:00 SWITCH TO DOWN</div>", unsafe_allow_html=True)

@st.cache_data(ttl=120)
def get_nifty():
    try:
        t = yf.Ticker("^NSEI")
        df = t.history(period="1d", interval="5m")
        return df
    except:
        return pd.DataFrame()

df_nifty = get_nifty()

col1, col2, col3 = st.columns([0.9, 1.1, 2])

with col1:
    st.markdown("<div class='panel'><div style='font-size:10px;'><b>WALLET - 0X3319--9E2E</b> <span style='background:black;color:#00ff00;padding:1px 4px;border-radius:3px;'>LIVE</span></div><div style='font-size:10px;color:#666;margin-top:4px;'>ALL-TIME PNL</div><div style='font-size:36px;font-weight:bold;color:#00aa00;line-height:36px;'>+$219,991</div><div style='font-size:9px;margin-top:4px;'>ALL TIME - 126,011 FILLS</div><div style='display:flex;gap:10px;font-size:8px;margin-top:8px;border-top:1px solid #aaa;padding-top:6px;'><div>FILLS<br><b>126,011</b></div><div>WIN RATE<br><b>53.9%</b></div><div>SET EDGE<br><b>+5.82c</b></div></div><div style='font-size:8
