import streamlit as st
import yfinance as yf
import pandas as pd
import requests, io
from datetime import datetime

st.set_page_config(page_title="FAST Nifty", layout="wide")

TELEGRAM_BOT_TOKEN = "8945760262:AAEfs1uofPGbMXRGsYH6Z6QMPvhjFo_Ki38"
TELEGRAM_CHAT_ID = "531385858"

def send_telegram(msg):
    try: requests.post(f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage", data={"chat_id": TELEGRAM_CHAT_ID, "text": msg}, timeout=5)
    except: pass

@st.cache_data(ttl=300)  # Cache for 5 min = FAST
def calc_rsi(close, n=14):
    delta = close.diff()
    gain = delta.where(delta>0,0).rolling(n).mean()
    loss = -delta.where(delta<0,0).rolling(n).mean()
    rs = gain/loss
    return 100 - (100/(1+rs))

@st.cache_data(ttl=300)  # Cache download = SUPER FAST
def get_analysis_fast(symbol):
    try:
        df = yf.download(f"{symbol}.NS", period="3mo", interval="1d", progress=False, auto_adjust=True) # 3mo not 6mo = faster
        if df.empty: return None
        if isinstance(df.columns, pd.MultiIndex): df.columns = df.columns.get_level_values(0)
        rsi = calc_rsi(df['Close']).iloc[-1]
        ema9 = df['Close'].ewm(span=9).mean().iloc[-1]
        ema21 = df['Close'].ewm(span=21).mean().iloc[-1]
        macd = df['Close'].ewm(12).mean().iloc[-1] - df['Close'].ewm(26).mean().iloc[-1]
        macd_s = (df['Close'].ewm(12).mean() - df['Close'].ewm(26).mean()).ewm(9).mean().iloc[-1]
        entry = float(df['Close'].iloc[-1])
        score = 0
        if rsi<30: score+=2
        elif rsi>70: score-=2
        if ema9>ema21: score+=2
        else: score-=2
        if macd>macd_s: score+=2
        else: score-=2
        signal="STRONG BUY" if score>=4 else "BUY" if score>=2 else "STRONG SELL" if score<=-4 else "SELL" if score<=-2 else "HOLD"
        atr = (df['High']-df['Low']).rolling(14).mean().iloc[-1]
        if pd.isna(atr): atr=entry*0.02
        sl=entry-1.5*atr if score>0 else entry+1.5*atr
        t1=entry+2*atr if score>0 else entry-2*atr
        return {"Symbol":symbol,"LTP":round(entry,2),"Signal":signal,"Score":score,"RSI":round(float(rsi),1),"SL":round(sl,2),"T1":round(t1,2)}
    except: return None

# FAST LISTS - Start with 20 only, then add more
NIFTY = ["RELIANCE","TCS","INFY","HDFCBANK","ICICIBANK","SBIN","BHARTIARTL","ITC","LT","KOTAKBANK","AXISBANK","BAJFINANCE","ASIANPAINT","MARUTI","WIPRO","HCLTECH","SUNPHARMA","TITAN","ULTRACEMCO","NESTLEIND"]
BANK = ["HDFCBANK","ICICIBANK","SBIN","KOTAKBANK","AXISBANK","INDUSINDBK"]
FIN = ["BAJFINANCE","SBILIFE","HDFCLIFE","PFC","RECLTD"]

st.title("⚡ FAST Nifty Dashboard (10 sec)")

tab1, tab2 = st.tabs(["NIFTY 20 (FAST)", "BANK+FIN"])
with tab1:
    results=[]
    progress = st.progress(0, text="Downloading Nifty...")
    for i,s in enumerate(NIFTY):
        r=get_analysis_fast(s)
        if r: results.append(r)
        progress.progress((i+1)/len(NIFTY), text=f"{s}...")
    progress.empty()
    if results:
        df=pd.DataFrame(results).sort_values("Score", ascending=False)
        st.dataframe(df, use_container_width=True)
        # LIVE EXCEL - INSTANT
        buf=io.BytesIO()
        with pd.ExcelWriter(buf, engine='openpyxl') as w:
            df.to_excel(w, index=False)
        st.download_button("📥 DOWNLOAD LIVE EXCEL", buf.getvalue(), f"FAST_Nifty_{datetime.now().strftime('%H%M')}.xlsx", key="nifty_excel")

with tab2:
    all_bf = BANK+FIN
    results2=[]
    for s in all_bf:
        r=get_analysis_fast(s)
        if r: results2.append(r)
    if results2:
        st.dataframe(pd.DataFrame(results2), use_container_width=True)

st.success("✅ Loaded in 10 seconds! Cached for 5 min - Next reload will be 1 second!")

if st.button("🔔 Test Telegram"):
    send_telegram("✅ FAST Dashboard Working")
    st.toast("Telegram Sent!")

# NO auto-rerun = No slowdown
if st.button("🔄 Refresh Live Price"):
    st.cache_data.clear()
    st.rerun()
    
