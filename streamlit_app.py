import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go
from datetime import datetime
import pytz
import time

st.set_page_config(page_title="NIFTY REAL LIVE ALL 50", layout="wide", page_icon="⚡")
st.title("⚡ NIFTY BANKNIFTY FINNIFTY - REAL NSE LIVE - ALL 50 STOCKS")

ist = pytz.timezone('Asia/Kolkata')
now = datetime.now(ist)
st.markdown(f"### REAL NSE LIVE - {now.strftime('%d-%m-%Y %H:%M:%S IST')} - NO TRADINGVIEW")
st.markdown("---")

@st.cache_data(ttl=120)
def get_data(symbol):
    try:
        t = yf.Ticker(symbol)
        df = t.history(period="1d", interval="5m")
        if len(df)>0:
            ltp = float(df['Close'].iloc[-1])
            prev = float(t.info.get('previousClose', ltp))
            chg = ((ltp-prev)/prev*100)
            return df, ltp, chg, prev
    except:
        pass
    return None, None, None, None

@st.cache_data(ttl=180)
def get_all_batch(stock_tuple):
    rows=[]
    for sym in stock_tuple:
        try:
            t = yf.Ticker(sym)
            df = t.history(period="1d", interval="5m")
            if len(df)>0:
                ltp = float(df['Close'].iloc[-1])
                prev = float(t.info.get('previousClose', ltp))
                chg = ((ltp-prev)/prev*100)
                if chg>1.2:
                    sig="STRONG BUY"; trend="STRONG BULLISH"; act="BUY CE"; score=10
                elif chg>0.4:
                    sig="BUY"; trend="BULLISH"; act="BUY CE"; score=6
                elif chg<-1.2:
                    sig="STRONG SELL"; trend="STRONG BEARISH"; act="BUY PE"; score=-10
                elif chg<-0.4:
                    sig="SELL"; trend="BEARISH"; act="BUY PE"; score=-6
                else:
                    sig="NEUTRAL"; trend="SIDEWAYS"; act="WAIT"; score=0
                strike = round(ltp/50)*50
                sl = ltp*0.985 if score>0 else ltp*1.015
                tgt = ltp*1.03 if score>0 else ltp*0.97
                opt = f"{strike} {act.split()[-1]}" if act!="WAIT" else ""
                rows.append([sym.replace(".NS",""), f"{ltp:.2f}", f"{chg:.2f}%", sig, trend, opt, f"{sl:.2f}", f"{tgt:.2f}", act, score])
            time.sleep(0.35)
        except:
            continue
    return rows

c1,c2,c3 = st.columns(3)
for col, (name, sym) in zip([c1,c2,c3], [("NIFTY 50","^NSEI"), ("BANKNIFTY","^NSEBANK"), ("FINNIFTY","^CNXFIN")]):
    with col:
        df, ltp, chg, prev = get_data(sym)
        if ltp:
            st.metric(name, f"{ltp:.2f}", f"{chg:.2f}%")
            if df is not None:
                fig = go.Figure()
                fig.add_trace(go.Scatter(x=df.index, y=df['Close'], mode='lines', line=dict(color='#00ff88' if chg>0 else '#ff4444')))
                fig.update_layout(height=220, margin=dict(l=0,r=0,t=0,b=0), paper_bgcolor="#0e1117", plot_bgcolor="#0e1117", font_color="white", xaxis=dict(showgrid=False), yaxis=dict(showgrid=False))
                st.plotly_chart(fig, use_container_width=True)

st.divider()

ALL_STOCKS = [
"RELIANCE.NS","TCS.NS","INFY.NS","HDFCBANK.NS","ICICIBANK.NS","SBIN.NS","BHARTIARTL.NS","ITC.NS","LT.NS","KOTAKBANK.NS",
"AXISBANK.NS","BAJFINANCE.NS","MARUTI.NS","MOTHERSON.NS","SUNPHARMA.NS","M&M.NS","WIPRO.NS","ULTRACEMCO.NS","NTPC.NS","POWERGRID.NS",
"ONGC.NS","HCLTECH.NS","TITAN.NS","BAJAJFINSV.NS","ADANIENT.NS","ADANIPORTS.NS","COALINDIA.NS","JSWSTEEL.NS","HINDALCO.NS","TATASTEEL.NS",
"GRASIM.NS","TECHM.NS","DIVISLAB.NS","CIPLA.NS","DRREDDY.NS","APOLLOHOSP.NS","EICHERMOT.NS","BPCL.NS","BRITANNIA.NS","NESTLEIND.NS",
"HINDUNILVR.NS","INDUSINDBK.NS","BAJAJ-AUTO.NS","HEROMOTOCO.NS","SHRIRAMFIN.NS","LTIM.NS","TRENT.NS","BEL.NS","SBILIFE.NS","HDFCLIFE.NS"
]

st.subheader(f"ALL {len(ALL_STOCKS)} STOCKS - REAL NSE - BUY SELL + OPTION")

col_a, col_b = st.columns([1,2])
with col_a:
    view = st.radio("View", ["1-20 Fast","21-40","41-50","ALL 50 (25 sec)"], index=0)
with col_b:
    if st.button("LOAD REAL PRICES", type="primary"):
        st.cache_data.clear()
        st.rerun()

if view=="1-20 Fast":
    batch = ALL_STOCKS[:20]
elif view=="21-40":
    batch = ALL_STOCKS[20:40]
elif view=="41-50":
    batch = ALL_STOCKS[40:]
else:
    batch = ALL_STOCKS

with st.spinner(f"Fetching {len(batch)} REAL prices... Wait..."):
    rows = get_all_batch(tuple(batch))

if rows:
    df_final = pd.DataFrame(rows, columns=["Symbol","REAL LTP","Change%","Signal","Trend","Option Strike","SL","Target","Action","Score"])
    df_final = df_final.sort_values("Score", ascending=False)
    st.dataframe(df_final.drop(columns=["Score"]), width='stretch', hide_index=True, height=800)
    st.success(f"{len(rows)} REAL NSE prices loaded - ALL VISIBLE")
    csv = df_final.to_csv(index=False).encode('utf-8')
    st.download_button("DOWNLOAD CSV", csv, "nifty_all_50_real.csv", "text/csv")
else:
    st.warning("No data - Click LOAD")

st.caption("REAL NSE via yfinance - No TradingView - Cache 120s - 0.35s delay - No throttle")
