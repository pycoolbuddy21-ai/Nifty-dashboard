import streamlit as st
import yfinance as yf
import pandas as pd
import requests, time
import numpy as np
from datetime import datetime

TELEGRAM_BOT_TOKEN = "8945760262:AAEfs1uofPGbMXRGsYH6Z6QMPvhjFo_Ki38"
TELEGRAM_CHAT_ID = "531385858"

def send_telegram(msg):
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        requests.post(url, data={"chat_id": TELEGRAM_CHAT_ID, "text": msg}, timeout=10)
    except: pass

def calc_rsi(close, n=14):
    delta = close.diff()
    gain = delta.where(delta>0,0).rolling(n).mean()
    loss = -delta.where(delta<0,0).rolling(n).mean()
    rs = gain/loss
    return 100 - (100/(1+rs))

st.set_page_config(layout="wide")
NIFTY50 = ["RELIANCE","TCS","INFY","HDFCBANK","ICICIBANK","SBIN","BHARTIARTL","ITC","LT","KOTAKBANK","AXISBANK","BAJFINANCE","ASIANPAINT","MARUTI","WIPRO","HCLTECH","SUNPHARMA","TITAN","ULTRACEMCO","NESTLEIND","POWERGRID","NTPC","BAJAJFINSV","ONGC","TATAMOTORS","ADANIENT","JSWSTEEL","COALINDIA","HINDALCO","GRASIM","HINDUNILVR","CIPLA","DRREDDY","EICHERMOT","BRITANNIA","DIVISLAB","TECHM","SBILIFE","APOLLOHOSP","BAJAJ-AUTO","HEROMOTOCO","INDUSINDBK","BPCL","TATACONSUM","ADANIPORTS","TATASTEEL","UPL","LTIM"]

def get_analysis(symbol):
    try:
        df = yf.download(f"{symbol}.NS", period="6mo", interval="1d", progress=False, auto_adjust=True)
        if df.empty: return None
        if isinstance(df.columns, pd.MultiIndex): df.columns = df.columns.get_level_values(0)
        df['RSI'] = calc_rsi(df['Close'])
        df['EMA9'] = df['Close'].ewm(span=9).mean()
        df['EMA21'] = df['Close'].ewm(span=21).mean()
        df['EMA12'] = df['Close'].ewm(span=12).mean()
        df['EMA26'] = df['Close'].ewm(span=26).mean()
        df['MACD'] = df['EMA12']-df['EMA26']
        df['MACD_S'] = df['MACD'].ewm(span=9).mean()
        hl = df['High']-df['Low']
        hc = (df['High']-df['Close'].shift()).abs()
        lc = (df['Low']-df['Close'].shift()).abs()
        tr = pd.concat([hl,hc,lc],axis=1).max(axis=1)
        df['ATR'] = tr.rolling(14).mean()
        last = df.iloc[-1]
        score=0
        if last['RSI']<30: score+=2
        elif last['RSI']>70: score-=2
        if last['EMA9']>last['EMA21']: score+=2
        else: score-=2
        if last['MACD']>last['MACD_S']: score+=2
        else: score-=2
        if last['Close']>last['EMA21']: score+=2
        else: score-=2
        signal="STRONG BUY" if score>=6 else "BUY" if score>=3 else "STRONG SELL" if score<=-6 else "SELL" if score<=-3 else "HOLD"
        entry=float(last['Close']); atr=float(last['ATR']) if not pd.isna(last['ATR']) else entry*0.02
        sl=entry-1.5*atr if score>0 else entry+1.5*atr
        t1=entry+2*atr if score>0 else entry-2*atr
        rr=abs(t1-entry)/abs(entry-sl) if entry!=sl else 0
        return {"Symbol":symbol,"LTP":round(entry,2),"Signal":signal,"Score":score,"RSI":round(float(last['RSI']),1),"Entry":round(entry,2),"SL":round(sl,2),"T1":round(t1,2),"RR":round(rr,2),"Est%":round(abs(t1-entry)/entry*100,2),"Option":f"{round(entry/50)*50} {'CE' if score>0 else 'PE'}"}
    except Exception as e:
        return None

st.title("🔴 Nifty 50 LIVE + Telegram")
st.success(f"Alerts to Pradeep {TELEGRAM_CHAT_ID}")
if st.button("🔔 Test Telegram"):
    send_telegram("✅ Test Working! Dashboard LIVE")
    st.success("Check Telegram!")

results=[]; bar=st.progress(0)
for i,s in enumerate(NIFTY50):
    r=get_analysis(s)
    if r: results.append(r)
    bar.progress((i+1)/len(NIFTY50))

if results:
    df_all=pd.DataFrame(results).sort_values("Score",ascending=False)
    top=df_all.iloc[0]
    if top['Signal'] in ["STRONG BUY","STRONG SELL"]:
        key=f"{top['Symbol']}{top['Signal']}"
        if 'last_alert' not in st.session_state or st.session_state.last_alert!=key:
            msg=f"🚨 {top['Signal']} {top['Symbol']} @ {top['LTP']} {top['Option']} Entry:{top['Entry']} SL:{top['SL']} T1:{top['T1']} RR:{top['RR']}"
            send_telegram(msg)
            st.session_state.last_alert=key
            st.balloons()
    st.dataframe(df_all,use_container_width=True)
time.sleep(5)
st.rerun()
