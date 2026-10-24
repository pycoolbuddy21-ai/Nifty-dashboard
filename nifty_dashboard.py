import streamlit as st
import yfinance as yf
import pandas as pd
import pandas_ta as ta
import requests, time
from datetime import datetime

TELEGRAM_BOT_TOKEN = "8945760262:AAEfs1uofPGbMXRGsYH6Z6QMPvhjFo_Ki38"
TELEGRAM_CHAT_ID = "531385858"

def send_telegram(msg):
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        requests.post(url, data={"chat_id": TELEGRAM_CHAT_ID, "text": msg}, timeout=10)
    except: pass

st.set_page_config(layout="wide")
NIFTY50 = ["RELIANCE","TCS","INFY","HDFCBANK","ICICIBANK","SBIN","BHARTIARTL","ITC","LT","KOTAKBANK","AXISBANK","BAJFINANCE","ASIANPAINT","MARUTI","WIPRO","HCLTECH","SUNPHARMA","TITAN","ULTRACEMCO","NESTLEIND","POWERGRID","NTPC","BAJAJFINSV","ONGC","TATAMOTORS","ADANIENT","JSWSTEEL","COALINDIA","HINDALCO","GRASIM","HINDUNILVR","CIPLA","DRREDDY","EICHERMOT","BRITANNIA","DIVISLAB","TECHM","SBILIFE","APOLLOHOSP","BAJAJ-AUTO","HEROMOTOCO","INDUSINDBK","BPCL","TATACONSUM","ADANIPORTS","TATASTEEL","UPL","LTIM"]

def get_analysis(symbol):
    try:
        df = yf.download(f"{symbol}.NS", period="6mo", interval="1d", progress=False)
        if df.empty: return None
        if isinstance(df.columns, pd.MultiIndex): df.columns = df.columns.get_level_values(0)
        df['RSI'] = ta.rsi(df['Close'], 14)
        df['EMA9'] = ta.ema(df['Close'], 9)
        df['EMA21'] = ta.ema(df['Close'], 21)
        macd = ta.macd(df['Close'])
        df['MACD'] = macd['MACD_12_26_9']
        df['MACD_S'] = macd['MACDs_12_26_9']
        df['ATR'] = ta.atr(df['High'], df['Low'], df['Close'], 14)
        df['ST'] = ta.supertrend(df['High'], df['Low'], df['Close'], 10, 3)['SUPERT_10_3.0']
        last = df.iloc[-1]
        score = 0
        if last['RSI'] < 30: score+=2
        elif last['RSI'] > 70: score-=2
        if last['EMA9'] > last['EMA21']: score+=2
        else: score-=2
        if last['MACD'] > last['MACD_S']: score+=2
        else: score-=2
        if last['Close'] > last['ST']: score+=2
        else: score-=2
        signal = "STRONG BUY" if score>=6 else "BUY" if score>=3 else "STRONG SELL" if score<=-6 else "SELL" if score<=-3 else "HOLD"
        entry = float(last['Close']); atr = float(last['ATR'])
        sl = entry - 1.5*atr if score>0 else entry + 1.5*atr
        t1 = entry + 2*atr if score>0 else entry - 2*atr
        rr = abs(t1-entry)/abs(entry-sl) if entry!=sl else 0
        return {"Symbol":symbol,"LTP":round(entry,2),"Signal":signal,"Score":score,"RSI":round(float(last['RSI']),1),"Entry":round(entry,2),"SL":round(sl,2),"T1":round(t1,2),"RR":round(rr,2),"Est%":round(abs(t1-entry)/entry*100,2),"Option":f"{round(entry/50)*50} {'CE' if score>0 else 'PE'}"}
    except: return None

st.title("🔴 Nifty 50 LIVE + Telegram Alert")
st.success(f"Alerts to: Pradeep {TELEGRAM_CHAT_ID}")
if st.button("🔔 Test Telegram"):
    send_telegram("✅ Test Working! Dashboard LIVE")
    st.success("Check Telegram!")

results=[]
bar=st.progress(0)
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
            msg=f"🚨 {top['Signal']} {top['Symbol']} @ {top['LTP']} Option:{top['Option']} Entry:{top['Entry']} SL:{top['SL']} T1:{top['T1']} RR:{top['RR']}"
            send_telegram(msg)
            st.session_state.last_alert=key
            st.balloons()
    st.dataframe(df_all,use_container_width=True)
time.sleep(5)
st.rerun()
