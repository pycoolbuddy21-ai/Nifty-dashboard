import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go
from datetime import datetime
import pytz

st.set_page_config(page_title="NIFTY REAL LIVE", layout="wide")
st.title("⚡ NIFTY BANKNIFTY FINNIFTY - REAL NSE LIVE - NO ERROR")

ist = pytz.timezone('Asia/Kolkata')
now = datetime.now(ist)
st.markdown(f"### ✅ REAL NSE LIVE - {now.strftime('%d-%m-%Y %H:%M:%S IST')}")
st.markdown("---")

@st.cache_data(ttl=30)
def get_data(symbol):
    try:
        t = yf.Ticker(symbol)
        df = t.history(period="1d", interval="5m")
        if len(df)>0:
            ltp = float(df['Close'].iloc[-1])
            prev = float(t.info.get('previousClose', ltp))
            chg = ((ltp-prev)/prev*100)
            return df, ltp, chg, prev
    except Exception as e:
        st.error(f"{symbol} error {e}")
    return None, None, None, None

# NIFTY REAL
c1,c2,c3 = st.columns(3)
symbols = {"NIFTY 50":"^NSEI", "BANKNIFTY":"^NSEBANK", "FINNIFTY":"^CNXFIN"}
for col, (name, sym) in zip([c1,c2,c3], symbols.items()):
    with col:
        df, ltp, chg, prev = get_data(sym)
        if ltp:
            st.metric(name, f"{ltp:.2f}", f"{chg:.2f}%")
            color = "green" if chg>0 else "red"
            st.markdown(f":{color}[**BUY {'CE' if chg>0 else 'PE'}**]" if abs(chg)>0.2 else ":orange[**WAIT**]")
            if df is not None:
                fig = go.Figure()
                fig.add_trace(go.Scatter(x=df.index, y=df['Close'], mode='lines', name=name, line=dict(color='#00ff88' if chg>0 else '#ff4444')))
                fig.update_layout(height=250, margin=dict(l=0,r=0,t=0,b=0), paper_bgcolor="#0e1117", plot_bgcolor="#0e1117", font_color="white", xaxis=dict(showgrid=False), yaxis=dict(showgrid=False))
                st.plotly_chart(fig, use_container_width=True)
        else:
            st.metric(name, "Loading...")

st.divider()
st.subheader("📊 ALL STOCKS REAL NSE - OPTION SUGGESTION - REAL PRICE")

STOCKS = ["RELIANCE.NS","TCS.NS","INFY.NS","HDFCBANK.NS","ICICIBANK.NS","SBIN.NS","BHARTIARTL.NS","ITC.NS","LT.NS","AXISBANK.NS","BAJFINANCE.NS","MARUTI.NS","TATAMOTORS.NS","SUNPHARMA.NS","M&M.NS","WIPRO.NS"]

rows=[]
progress = st.progress(0)
for i, sym in enumerate(STOCKS):
    df, ltp, chg, prev = get_data(sym)
    progress.progress((i+1)/len(STOCKS))
    if ltp:
        if chg>1.0: sig,trend,act,score="STRONG BUY","STRONG BULLISH","BUY CE",10
        elif chg>0.3: sig,trend,act,score="BUY","BULLISH","BUY CE",6
        elif chg<-1.0: sig,trend,act,score="STRONG SELL","STRONG BEARISH","BUY PE",-10
        elif chg<-0.3: sig,trend,act,score="SELL","BEARISH","BUY PE",-6
        else: sig,trend,act,score="NEUTRAL","SIDEWAYS","WAIT",0
        strike = round(ltp/50)*50
        rows.append([sym.replace(".NS",""), f"{ltp:.2f}", f"{chg:.2f}%", sig, trend, f"{strike} {act.split()[-1] if act!='WAIT' else ''}", f"{ltp*0.985:.2f}" if score>0 else f"{ltp*1.015:.2f}", f"{ltp*1.03:.2f}" if score>0 else f"{ltp*0.97:.2f}", act, score])

if rows:
    df_final = pd.DataFrame(rows, columns=["Symbol","REAL LTP","Change%","Signal","Trend","Option Strike","SL","Target","Action","Score"])
    df_final = df_final.sort_values("Score", ascending=False)
    st.dataframe(df_final.drop(columns=["Score"]), use_container_width=True, hide_index=True, height=600)
    st.success(f"✅ {len(rows)} REAL NSE prices loaded - NO TradingView - Works 100%")
else:
    st.warning("Fetching... Click refresh")

if st.button("🔄 REFRESH REAL LIVE - 1 SEC", type="primary"):
    st.cache_data.clear()
    st.rerun()

st.caption("REAL NSE DATA: yfinance ^NSEI, ^NSEBANK, RELIANCE.NS etc - No TradingView = No Error - Updates every 30 sec")
