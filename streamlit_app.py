import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go
import numpy as np
import pytz
from datetime import datetime
import math

st.set_page_config(page_title="HG BANKNIFTY BOT", layout="wide")

ist = pytz.timezone('Asia/Kolkata')
now = datetime.now(ist)
st.title("HG - BANKNIFTY 5M BOT")
st.caption(f"LIVE - {now.strftime('%H:%M:%S')} IST - NIFTY SPOT 63006")

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
    st.metric("ALL-TIME PNL", "+$219,991", "126,011 FILLS")
    st.write("WIN RATE 53.9%")
    st.write("SET EDGE +5.82c")
    st.write("DRAWDOWN RISK 2.2/10 SAFE")
    st.divider()
    st.write("DIRECTIONAL BIAS 56% UP")
    st.progress(56)
    st.write("MATCHED 86% / RESIDUAL 14%")
    st.progress(86)

with c2:
    if not df_nifty.empty:
        fig = go.Figure()
        fig.add_trace(go.Candlestick(x=df_nifty.index, open=df_nifty['Open'], high=df_nifty['High'], low=df_nifty['Low'], close=df_nifty['Close']))
        fig.update_layout(height=240, title_text="NIFTY 5M", margin=dict(l=0, r=0, t=30, b=0))
        fig.update_xaxes(rangeslider_visible=False)
        st.plotly_chart(fig, use_container_width=True)

with c3:
    st.write("MARKET LIFECYCLE - FILL - RESOLVE")
    st.write("RESOLUTION GRID - LIVE EXPIRIES")
    cols = st.columns(12)
    vals = ["$1", "87c", "26c", "45c", "28c", "49c", "63c", "52c", "12c", "11c", "62c", "89c"]
    for i in range(12):
        cols[i].write(vals[i])

st.divider()
st.subheader("NEURAL SHELL - MARKET FEED - FEATURE LAYER - DECISION CORE")

fig2 = go.Figure()
names = ["NIFTY 5M", "BANK 5M", "ORDER BOOK", "TAPE", "VOLATILITY", "REP PRICE", "INVENTORY"]
vals2 = [77, 15, 33, 43, 28, 71, 100]
ypos = [0.95, 0.8, 0.65, 0.5, 0.35, 0.2, 0.05]

for i in range(7):
    y = ypos[i]
    xs = np.linspace(0, 0.18, 10)
    ys = [y + math.sin(xi*10)*0.02 for xi in xs]
    fig2.add_trace(go.Scatter(x=xs, y=ys, mode='lines', showlegend=False))
    fig2.add_trace(go.Scatter(x=[0], y=[y], mode='text', text=[names[i]], showlegend=False))
    fig2.add_trace(go.Scatter(x=[0.18], y=[y], mode='text', text=[str(vals2[i])], showlegend=False))

for y in np.linspace(0, 1, 48):
    fig2.add_trace(go.Scatter(x=[0.5], y=[y], mode='markers', marker=dict(size=3, color="blue"), showlegend=False))

for y1 in ypos:
    fig2.add_trace(go.Scatter(x=[0.18, 0.34, 0.5], y=[y1, (y1+0.5)/2, 0.5], mode='lines', line=dict(color="rgba(100,100,100,0.2)"), showlegend=False))

np.random.seed(7)
for i in range(200):
    ang = np.random.rand()*6.283
    r = 0.25 + np.random.rand()*0.35
    x = 0.82 + r*math.cos(ang)*0.5
    y = 0.5 + r*math.sin(ang)*0.9
    fig2.add_trace(go.Scatter(x=[x], y=[y], mode='markers', marker=dict(size=4, color="#4a6fc7"), showlegend=False))

for i in range(120):
    ang = np.random.rand()*6.283
    r = np.random.rand()*0.18
    x = 0.84 + r*math.cos(ang)*0.4
    y = 0.5 + r*math.sin(ang)*0.6
    fig2.add_trace(go.Scatter(x=[x], y=[y], mode='markers', marker=dict(size=6, color="#e67e22"), showlegend=False))

fy = [0.92, 0.8, 0.68, 0.56, 0.44, 0.32, 0.2, 0.08]
for y2 in fy:
    fig2.add_trace(go.Scatter(x=[0.5, 0.65, 0.82], y=[y2, (y2+0.5)/2, 0.5], mode='lines', line=dict(color="rgba(230,126,34,0.25)"), showlegend=False))

fig2.update_layout(height=520, margin=dict(l=5, r=5, t=5, b=5), xaxis=dict(visible=False, range=[-0.05, 1.25]), yaxis=dict(visible=False, range=[-0.1, 1.1]), showlegend=False)
st.plotly_chart(fig2, use_container_width=True)

b1, b2 = st.columns(2)
with b1:
    x = np.random.rand(80)*10
    y = x + np.random.randn(80)*1.8
    fig3 = go.Figure()
    fig3.add_trace(go.Scatter(x=x, y=y, mode='markers'))
    fig3.add_shape(type="line", x0=0, y0=0, x1=10, y1=10, line=dict(dash="dash"))
    fig3.update_layout(title_text="EDGE MATRIX", height=340)
    st.plotly_chart(fig3, use_container_width=True)
with b2:
    fig4 = go.Figure(data=[go.Sankey(node=dict(label=["BTC 5M", "ETH 5M", "LIMIT FILL", "OPPOSITE SIDE", "SET COMPLETED", "RESIDUAL UP", "MATCHED"]), link=dict(source=[0, 0, 1, 1, 2, 2, 3], target=[2, 3, 2, 3, 4, 5, 6], value=[12, 4, 10, 6, 8, 6, 4]))])
    fig4.update_layout(title_text="HEDGE FLOW", height=340)
    st.plotly_chart(fig4, use_container_width=True)

st.divider()
st.subheader("NIFTY REAL BUY/SELL + OPTION CHAIN + PAST DATA")

@st.cache_data(ttl=300)
def fetch_all():
    syms = []
    syms.append("RELIANCE.NS")
    syms.append("TCS.NS")
    syms.append("INFY.NS")
    syms.append("HDFCBANK.NS")
    syms.append("ICICIBANK.NS")
    syms.append("SBIN.NS")
    syms.append("BHARTIARTL.NS")
    syms.append("ITC.NS")
    syms.append("LT.NS")
    syms.append("KOTAKBANK.NS")
    rows = []
    for s in syms:
        try:
            t = yf.Ticker(s)
            df = t.history(period="5d")
            if len(df) > 1:
                ltp = df['Close'].iloc[-1]
                chg = (df['Close'].iloc[-1] - df['Close'].iloc[-2]) / df['Close'].iloc[-2] * 100
                if chg > 0.3:
                    sig = "BUY CE"
                elif chg < -0.3:
                    sig = "BUY PE"
                else:
                    sig = "NEUTRAL"
                rows.append([s.replace(".NS", ""), round(float(ltp), 2), round(float(chg), 2), sig, float(chg)])
        except:
            continue
    return rows

rows = fetch_all()
if rows:
    df = pd.DataFrame(rows, columns=["Symbol", "LTP", "Change", "Signal", "Score"])
    df = df.sort_values("Score", ascending=False)
    st.dataframe(df, use_container_width=True, hide_index=True)
    sel = st.selectbox("Select for Option Chain", df["Symbol"].tolist())
    try:
        t = yf.Ticker(sel + ".NS")
        exp = t.options[0]
        oc = t.option_chain(exp)
        left = oc.calls[['strike', 'lastPrice', 'volume', 'openInterest']]
        right = oc.puts[['strike', 'lastPrice', 'volume', 'openInterest']]
        chain = pd.merge(left, right, on='strike', suffixes=('_CE', '_PE'))
        chain = chain.sort_values('strike')
        ca, cb = st.columns(2)
        with ca:
            st.write(f"Option Chain {sel} {exp}")
            st.dataframe(chain.head(30), height=420)
        with cb:
            df5 = t.history(period="5d")
            fig5 = go.Figure()
            fig5.add_trace(go.Candlestick(x=df5.index, open=df5['Open'], high=df5['High'], low=df5['Low'], close=df5['Close']))
            fig5.update_layout(height=420, title_text=sel + " Past 5 Days")
            fig5.update_xaxes(rangeslider_visible=False)
            st.plotly_chart(fig5, use_container_width=True)
    except Exception as e:
        st.write("Option chain not available")
