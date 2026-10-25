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
<div style="background:#c2c9d9; border:1px solid #8a95ad; padding:3px 6px; font-size:10px; display:flex; justify-content:space-between">
<div><span style="background:#2a2f3d; color:white; padding:2px 6px">HG</span> hot-garbage // BANKNIFTY 5M BOT - LIVE DIRECTIONAL</div>
<div style="text-align:right">NIFTY $63,006 - NIFTY 5M 0.97 - BANK 5M 1.00 - {now.strftime('%H:%M:%S')} UTC</div>
</div>
<div style="background:#ff3b3b; color:white; font-size:9px; padding:2px 6px">LIVE FEED 5M 10:00AM-10:05AM Up 0.42 Dn 0.50 FLIP SIDE</div>
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
    <div style="font-size:9px"><b>WALLET - 0X3319--9E2E</b> <span style="background:black; color:#00ff00">LIVE</span></div>
    <div style="font-size:9px">ALL-TIME PNL</div>
    <div style="font-size:32px; font-weight:bold; color:#00aa00">+$219,991</div>
    <div style="font-size:8px">126,011 FILLS - WIN RATE 53.9% - SET EDGE +5.82c</div>
    <div style="font-size:8px; margin-top:4px">DRAWDOWN RISK 2.2/10 SAFE</div>
    <hr>
    <div style="font-size:8px">DIRECTIONAL BIAS 56% UP<br>INVENTORY 86% / 14%</div>
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
            plot_bgcolor="#e8ecf3",
            xaxis_rangeslider_visible=False
        )
        fig.update_layout(title_text="BTC PRICE NIFTY 5M 63006")
        st.plotly_chart(fig, use_container_width=True)

with c3:
    st.markdown("""
    <div class="panel" style="font-size:9px">
    <b>MARKET LIFECYCLE - FILL - RESOLVE</b><br>
    <div style="height:70px; background:#d0d0d0; margin-top:6px"></div>
    </div>
    <div class="panel" style="font-size:9px; margin-top:6px">
    <b>RESOLUTION GRID - LIVE EXPIRIES</b><br>
    <div style="display:grid; grid-template-columns:repeat(12,1fr); gap:3px; margin-top:6px">
    <div style="background:#a8e6a3; border:1px solid #5a5; text-align:center; padding:3px">$1</div>
    <div style="background:#a8e6a3; border:1px solid #5a5; text-align:center; padding:3px">87c</div>
    <div style="background:#f0a8a8; border:1px solid #a55; text-align:center; padding:3px">26c</div>
    <div style="background:#f0a8a8; border:1px solid #a55; text-align:center; padding:3px">45c</div>
    <div style="background:#f0a8a8; border:1px solid #a55; text-align:center; padding:3px">28c</div>
    <div style="background:#f0a8a8; border:1px solid #a55; text-align:center; padding:3px">49c</div>
    <div style="background:#a8e6a3; border:1px solid #5a5; text-align:center; padding:3px">63c</div>
    <div style="background:#a8e6a3; border:1px solid #5a5; text-align:center; padding:3px">52c</div>
    <div style="background:#f0a8a8; border:1px solid #a55; text-align:center; padding:3px">12c</div>
    <div style="background:#f0a8a8; border:1px solid #a55; text-align:center; padding:3px">11c</div>
    <div style="background:#a8e6a3; border:1px solid #5a5; text-align:center; padding:3px">62c</div>
    <div style="background:#a8e6a3; border:1px solid #5a5; text-align:center; padding:3px">89c</div>
    </div>
    </div>
    """, unsafe_allow_html=True)

# NEURAL SHELL
st.markdown("""<div class="panel" style="padding:4px 6px; font-size:9px"><b>NEURAL SHELL</b> MARKET FEED - FEATURE LAYER - DECISION CORE</div>""", unsafe_allow_html=True)

fig = go.Figure()

ingest_names = ["NIFTY 5M", "BANK 5M", "ORDER BOOK", "TAPE", "VOLATILITY", "REP PRICE", "INVENTORY"]
ingest_vals = [77, 15, 33, 43, 28, 71, 100]
y_positions = [0.95, 0.8, 0.65, 0.5, 0.35, 0.2, 0.05]

for idx in range(len(ingest_names)):
    y = y_positions[idx]
    name = ingest_names[idx]
    val = ingest_vals[idx]
    x_small = np.linspace(0, 0.18, 10)
    y_small = [y + math.sin(xi*10)*0.02 for xi in x_small]
    fig.add_trace(go.Scatter(x=x_small, y=y_small, mode='lines', showlegend=False))
    fig.add_trace(go.Scatter(x=[0], y=[y], mode='text', text=[name], showlegend=False, textfont=dict(size=8)))
    fig.add_trace(go.Scatter(x=[0.18], y=[y], mode='text', text=[str(val)], showlegend=False))

for y in np.linspace(0, 1, 48):
    fig.add_trace(go.Scatter(x=[0.5], y=[y], mode='markers', marker=dict(size=3, color="blue"), showlegend=False))

for y1 in y_positions:
    y2 = 0.5
    fig.add_trace(go.Scatter(x=[0.18, 0.34, 0.5], y=[y1, (y1+y2)/2, y2], mode='lines', line=dict(color="rgba(100,100,100,0.25)"), showlegend=False))

np.random.seed(7)
for i in range(250):
    ang = np.random.rand()*2*math.pi
    r = 0.25 + np.random.rand()*0.35
    x = 0.82 + r*math.cos(ang)*0.5
    y = 0.5 + r*math.sin(ang)*0.9
    fig.add_trace(go.Scatter(x=[x], y=[y], mode='markers', marker=dict(size=4, color="#4a6fc7"), showlegend=False))

for i in range(180):
    ang = np.random.rand()*2*math.pi
    r = np.random.rand()*0.18
    x = 0.84 + r*math.cos(ang)*0.4
    y = 0.5 + r*math.sin(ang)*0.6
    fig.add_trace(go.Scatter(x=[x], y=[y], mode='markers', marker=dict(size=6, color="#e67e22"), showlegend=False))

fy = np.linspace(0.92, 0.08, 8)
for y2 in fy:
    fig.add_trace(go.Scatter(x=[0.5, 0.65, 0.82], y=[y2, (y2+0.5)/2, 0.5], mode='lines', line=dict(color="rgba(230,126,34,0.25)"), showlegend=False))

fig.update_layout(
    height=520,
    margin=dict(l=5, r=5, t=5, b=5),
    paper_bgcolor="#eef2f8",
    plot_bgcolor="#eef2f8",
    xaxis=dict(visible=False, range=[-0.05, 1.25]),
    yaxis=dict(visible=False, range=[-0.1, 1.1]),
    showlegend=False
)

st.plotly_chart(fig, use_container_width=True)

# BOTTOM
c4, c5 = st.columns(2)
with c4:
    x = np.random.rand(80)*10
    y = x + np.random.randn(80)*1.8
    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(x=x, y=y, mode='markers'))
    fig2.add_shape(type="line", x0=0, y0=0, x1=10, y1=10, line=dict(dash="dash"))
    fig2.update_layout(title_text="EDGE MATRIX", height=320, paper_bgcolor="#e8ecf3")
    st.plotly_chart(fig2, use_container_width=True)

with c5:
    fig3 = go.Figure(data=[go.Sankey(
        node=dict(label=["BTC 5M","ETH 5M","LIMIT FILL","OPPOSITE SIDE","SET COMPLETED","RESIDUAL UP","MATCHED"]),
        link=dict(source=[0,0,1,1,2,2,3], target=[2,3,2,3,4,5,6], value=[12,4,10,6,8,6,4])
    )])
    fig3.update_layout(title_text="HEDGE FLOW", height=320, paper_bgcolor="#e8ecf3")
    st.plotly_chart(fig3, use_container_width=True)

st.divider()
st.markdown("### NIFTY REAL BUY/SELL + OPTION CHAIN + PAST DATA")

@st.cache_data(ttl=300)
def fetch_all():
    syms = ["RELIANCE.N
