import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go
import numpy as np
import pytz
from datetime import datetime
import math

st.set_page_config(page_title="hot-garbage // BANKNIFTY BOT", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&display=swap');
.stApp { background:#d5dbe8; font-family:'JetBrains Mono', monospace; }
.panel { background:#e8ecf3; border:1px solid #9aa4b8; padding:6px; margin-bottom:6px; }
.small { font-size:9px; line-height:10px; }
.green { color:#00aa00; } .red{ color:#cc0000; }
.tile-green { background:#a8e6a3; border:1px solid #5a5; text-align:center; padding:3px; font-weight:bold; font-size:11px }
.tile-red { background:#f0a8a8; border:1px solid #a55; text-align:center; padding:3px; font-weight:bold; font-size:11px }
</style>
""", unsafe_allow_html=True)

ist = pytz.timezone('Asia/Kolkata')
now = datetime.now(ist)

# TOP BAR - EXACT LIKE IMAGE
st.markdown(f"""
<div style="background:#c2c9d9; border:1px solid #8a95ad; padding:3px 6px; font-size:10px; display:flex; justify-content:space-between">
<div><span style="background:#2a2f3d; color:white; padding:2px 6px; border-radius:3px">HG</span> 
• LIVE DIRECTIONAL • HEDGE 53% UP • SETS 41%: $1 46.3k &nbsp; <b>hot-garbage // BANKNIFTY 5M BOT</b> &nbsp; V4.2 - BTC - ETH - 5M UP-DOWN - HFT MAKER / CHEAP COMPLETE SETS + DYNAMIC HEDGE</div>
<div style="text-align:right">BTC SPOT<br><b>$63,006</b> &nbsp; BTC 5M 0.97 &nbsp; ETH 5M 1.00 &nbsp; SET EDGE 5.81¢<br>{now.strftime('%H:%M:%S')} UTC</div>
</div>
<div style="background:#ff3b3b; color:white; font-size:9px; padding:2px 6px; white-space:nowrap; overflow:hidden">
● LIVE FEED &nbsp; 5M 10:00AM-10:05AM - Up 0.42 - Dn 0.50 - FLIP SIDE - ETH 5M 9:55AM-10:00AM - SWITCH TO DOWN @ $0.42 - HEDGE ADD - ETH 5M - +DOWN @ $0.50 -
</div>
""", unsafe_allow_html=True)

@st.cache_data(ttl=120)
def get_nifty():
    try:
        t=yf.Ticker("^NSEI")
        df=t.history(period="1d", interval="5m")
        return df
    except: return pd.DataFrame()

df_nifty=get_nifty()

# ROW 1
c1,c2,c3=st.columns([0.9,1.1,2])

with c1:
    st.markdown("""
    <div class="panel">
    <div style="display:flex; justify-content:space-between; font-size:9px"><b>● WALLET - 0X3319--9E2E</b><span style="background:black; color:#00ff00; padding:0 4px">LIVE</span></div>
    <div style="font-size:9px; color:#666">0x3319--9E2E</div>
    <div style="font-size:9px; margin-top:6px">ALL-TIME PNL</div>
    <div style="font-size:32px; font-weight:bold; color:#00aa00; line-height:32px">+$219,991</div>
    <div style="font-size:8px">▲ ALL TIME - 126,011 FILLS</div>
    <div style="display:flex; gap:12px; font-size:8px; margin-top:8px; border-top:1px solid #aaa; padding-top:4px">
    <div>FILLS<br><b>126,011</b></div><div>WIN RATE<br><b>53.9%</b></div><div>SET EDGE<br><b>+5.82¢</b></div>
    </div>
    <div style="font-size:8px; margin-top:4px">DRAWDOWN RISK <b>2.2/10</b> <span style="background:#ffd54f; padding:1px 4px">SAFE</span></div>
    <hr style="margin:6px 0">
    <div style="font-size:8px"><b>+ INVENTORY & FLOW</b><span style="float:right; color:green">• LIVE</span><br>
    DIRECTIONAL BIAS &nbsp; 56% UP<br>
    <div style="height:8px; display:flex; margin:2px 0"><div style="width:56%; background:green"></div><div style="width:44%; background:red"></div></div>
    MATCHED / RESIDUAL &nbsp; 86% / 14%<br>
    <div style="height:8px; display:flex; margin:2px 0; border:1px solid #000"><div style="width:86%; background:orange"></div><div style="width:14%; background:#ccc"></div></div>
    VOLUME BY ASSET &nbsp; BTC 58% - ETH 42%<br>
    <div style="height:8px; display:flex; margin:2px 0"><div style="width:58%; background:black"></div><div style="width:42%; background:#4a90e2"></div></div>
    </div>
    </div>
    """, unsafe_allow_html=True)

with c2:
    if not df_nifty.empty:
        fig=go.Figure(data=[go.Candlestick(x=df_nifty.index, open=df_nifty['Open'], high=df_nifty['High'], low=df_nifty['Low'], close=df_nifty['Close'], increasing_line_color='green', decreasing_line_color='red')])
        fig.update_layout(height=220, margin=dict(l=0,r=0,t=25,b=0), paper_bgcolor="#e8ecf3", plot_bgcolor="#e8ecf3", font=dict(size=8, family="JetBrains Mono"), title=dict(text="● BTC PRICE BTC/USD - 5M $63,006 ▼ 0.01%", font=dict(size=9)), xaxis_rangeslider_visible=False, xaxis=dict(showgrid=False), yaxis=dict(showgrid=False, side="right"))
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar':False})
    st.markdown("""
    <div class="panel small" style="font-size:8px">
    <div style="display:flex; justify-content:space-between"><span>5M UP</span><span>$5.2K Vol</span></div>
    <div style="display:grid; grid-template-columns:1fr 1fr 1fr; gap:2px; margin-top:4px">
    <div style="background:#ffcccc; padding:1px">54s 139.92 $193.38</div><div style="background:#ffcccc; padding:1px">53s 179.25 $113.62</div>
    <div style="background:#ffcccc; padding:1px">52s 19.37 $14.28</div><div style="background:#ffcccc; padding:1px">52s 19.37 $14.28</div>
    <div style="background:#ffcccc; padding:1px">51s 4.09 $3.24</div>
    </div>
    <div style="margin-top:4px; border-top:1px solid #aaa">
    Last: 514 &nbsp; Spread: 1.16<br>
    50s 299.94 $161.22<br>
    49s 88.86 $221.41<br>
    48s 203.37 $102.86<br>
    47s 80.86 $159.58
    </div>
    </div>
    """, unsafe_allow_html=True)

with c3:
    st.markdown("""
    <div class="panel small">
    <b>● MARKET LIFECYCLE - FILL - RESOLVE</b> &nbsp; ONE LANE = ONE MARKET - TICKS = FILLS - GOLD = SIDE FLIP
    <div style="margin-top:6px">
    <div style="display:flex; align-items:center; gap:4px; margin:2px 0"><span style="width:50px">BTC 5M</span><div style="flex:1; height:6px; background:#d0d0d0; position:relative"><div style="position:absolute; left:35%; width:40%; height:6px; background:#4a90e2"></div><div style="position:absolute; left:75%; width:4px; height:6px; background:orange; border-radius:50%"></div></div></div>
    <div style="display:flex; align-items:center; gap:4px; margin:2px 0"><span style="width:50px">BTC 5M</span><div style="flex:1; height:6px; background:#d0d0d0; position:relative"><div style="position:absolute; left:50%; width:45%; height:6px; background:#4a90e2"></div></div></div>
    <div style="display:flex; align-items:center; gap:4px; margin:2px 0"><span style="width:50px">BTC 10M</span><div style="flex:1; height:6px; background:#d0d0d0; position:relative"><div style="position:absolute; left:10%; width:60%; height:6px; background:#4a90e2"></div><div style="position:absolute; left:70%; width:4px; height:6px; background:orange; border-radius:50%"></div></div></div>
    </div>
    </div>
    <div class="panel small" style="margin-top:6px">
    <b>● RESOLUTION GRID - LIVE EXPIRIES</b> &nbsp; <span style="float:right">SETTLING 1 | OPEN 33</span><br>
    EACH TILE = A MARKET - COLOUR = TIME TO RESOLVE &nbsp; <span style="float:right">BTC / ETH 5M TRACKED</span>
    <div style="display:grid; grid-template-columns:repeat(12,1fr); gap:3px; margin-top:6px">
    <div class="tile-green">$1</div><div class="tile-green">87¢</div><div class="tile-red">26¢</div><div class="tile-red">45¢</div><div class="tile-red">28¢</div><div class="tile-red">49¢</div><div class="tile-green">63¢</div><div class="tile-green">52¢</div><div class="tile-red">12¢</div><div class="tile-red">11¢</div><div class="tile-green">62¢</div><div class="tile-green">89¢</div>
    <div class="tile-green">71¢</div><div class="tile-red">4¢</div><div class="tile-red">4¢</div><div class="tile-red">36¢</div><div class="tile-red">$0</div><div class="tile-green">54¢</div><div class="tile-green">57¢</div><div class="tile-green">94¢</div><div class="tile-red">75¢</div><div class="tile-red">23¢</div><div class="tile-green">82¢</div><div class="tile-green">92¢</div>
    </div>
    <div style="font-size:7px; margin-top:4px">AVG HOLD 00:05 - LIFET-ORDER MAKER &nbsp; <span style="float:right">RESOLVED 102</span></div>
    </div>
    """, unsafe_allow_html=True)

# NEURAL SHELL - EXACT LIKE IMAGE
st.markdown("""
<div class="panel" style="padding:0">
<div style="display:flex; justify-content:space-between; font-size:9px; padding:4px 6px; border-bottom:1px solid #aaa">
<div><b>● NEURAL SHELL</b> &nbsp; MARKET FEED - FEATURE LAYER - DECISION CORE - BTC 5M / 10M</div>
<div>818 / 1010 UNITS - ROUTED 49%</div>
</div>
</div>
""", unsafe_allow_html=True)

# Build the mind map like in picture
col_left, col_mid, col_right = st.columns([1.2,0.8,2.5])

# We will use one big plotly figure to replicate the shell
fig = go.Figure()

# Left ingest charts data mock (like image: BTC 5M 77, ETH 5M 15, ORDER BOOK 33, TAPE 43, VOLATILITY 28, REP PRICE 71, INVENTORY 100)
ingest = [
    ("BTC 5M", 77, "blue", [10,12,15,13,18,22,20,25,30,28]),
    ("ETH 5M", 15, "orange", [5,6,5,7,8,6,9,7,8]),
    ("ORDER BOOK", 33, "blue", [5,8,12,10,15,12,18,15]),
    ("TAPE", 43, "gray", [10,9,11,10,12,11,13,12]),
    ("VOLATILITY", 28, "red", [15,14,16,18,17,19,20,18]),
    ("REP PRICE", 71, "black", [10,12,11,13,12,14,13,15]),
    ("INVENTORY", 100, "green", [10,20,30,40,50,60,70,90,40]),
]

# Plot small sparklines on left (we will annotate as text in plotly for simplicity)
y_positions = [0.95, 0.8, 0.65, 0.5, 0.35, 0.2, 0.05]
for idx, (name,val,color,data) in enumerate(ingest):
    y = y_positions[idx]
    # line
    x_small = np.linspace(0, 0.18, len(data))
    fig.add_trace(go.Scatter(x=x_small, y=[y + d*0.005 for d in data], mode='lines', line=dict(color=color, width=1.5), showlegend=False))
    fig.add_trace(go.Scatter(x=[0], y=[y], mode='text', text=[f"<b>{name}</b>"], textposition="middle left", showlegend=False, textfont=dict(size=8, color="black")))
    fig.add_trace(go.Scatter(x=[0.18], y=[y], mode='text', text=[f"<b>{val}</b>"], textposition="middle right", showlegend=False, textfont=dict(size=9, color=color)))

# Feature extraction vertical dotted line at x=0.5
for y in np.linspace(0,1,48):
    fig.add_trace(go.Scatter(x=[0.5], y=[y], mode='markers', marker=dict(size=3, color="#1a4d9c"), showlegend=False))

# Feature labels
features = ["X PRICE","MOMENTUM","XL-REBALANCE","ON-ORDER","REP-QUEST","TIME LEFT","SPREAD","TAPE FLOW"]
fy = np.linspace(0.92, 0.08, len(features))
for f, y in zip(features, fy):
    fig.add_trace(go.Scatter(x=[0.5], y=[y], mode='text', text=[f], textposition="middle right", xanchor="left", showlegend=False, textfont=dict(size=7)))

# Connections - curved lines from ingest to features
np.random.seed(42)
for i, y1 in enumerate(y_positions):
    for _ in range(3):
        y2 = np.random.choice(fy)
        fig.add_trace(go.Scatter(x=[0.18,0.34,0.5], y=[y1, (y1+y2)/2 + np.random.randn()*0.05, y2], mode='lines', line=dict(color="rgba(100,100,100,0.25)", width=0.8), showlegend=False))

# Right core - large circular blob of dots
# Blue outer, orange center like image
np.random.seed(7)
# Outer blue scattered
for _ in range(250):
    ang = np.random.rand()*2*math.pi
    r = 0.25 + np.random.rand()*0.35
    x = 0.82 + r*math.cos(ang)*0.5
    y = 0.5 + r*math.sin(ang)*0.9
    fig.add_trace(go.Scatter(x=[x], y=[y], mode='markers', marker=dict(size=4, color="#4a6fc7"), showlegend=False))
# Inner orange cluster
for _ in range(180):
    ang = np.random.rand()*2*math.pi
    r = np.random.rand()*0.18
    x = 0.84 + r*math.cos(ang)*0.4
    y = 0.5 + r*math.sin(ang)*0.6
    size = 5 + np.random.rand()*7
    fig.add_trace(go.Scatter(x=[x], y=[y], mode='markers', marker=dict(size=size, color="#e67e22"), showlegend=False))

# Some black dots
for _ in range(30):
    x = 0.7 + np.random.rand()*0.4
    y = 0.1 + np.random.rand()*0.8
    fig.add_trace(go.Scatter(x=[x], y=[y], mode='markers', marker=dict(size=4, color="black"), showlegend=False))

# Connections from features to core
for y2 in fy
