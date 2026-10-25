import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
import pytz
import time

st.set_page_config(page_title="ALL 50 + SECTOR + INDUSTRY", layout="wide", page_icon="⚡")
st.title("⚡ NIFTY - ALL 50 OPTION CHAIN + SECTOR + INDUSTRY")

ist = pytz.timezone('Asia/Kolkata')
st.markdown(f"### REAL NSE LIVE - {datetime.now(ist).strftime('%d-%m-%Y %H:%M:%S IST')}")

INDUSTRY_MAP = {
"Financial Services": {"sector":"BANKING & FINANCE","stocks":["HDFCBANK.NS","ICICIBANK.NS","SBIN.NS","KOTAKBANK.NS","AXISBANK.NS","INDUSINDBK.NS","BAJFINANCE.NS","BAJAJFINSV.NS","SHRIRAMFIN.NS","SBILIFE.NS","HDFCLIFE.NS"],"weight":38},
"IT": {"sector":"IT","stocks":["TCS.NS","INFY.NS","WIPRO.NS","HCLTECH.NS","TECHM.NS","LTIM.NS"],"weight":14},
"Energy": {"sector":"ENERGY","stocks":["RELIANCE.NS","ONGC.NS","BPCL.NS","COALINDIA.NS","NTPC.NS","POWERGRID.NS","ADANIENT.NS","ADANIPORTS.NS"],"weight":12},
"Auto": {"sector":"AUTO","stocks":["MARUTI.NS","M&M.NS","BAJAJ-AUTO.NS","HEROMOTOCO.NS","EICHERMOT.NS","MOTHERSON.NS","BEL.NS"],"weight":8},
"Healthcare": {"sector":"PHARMA","stocks":["SUNPHARMA.NS","DIVISLAB.NS","CIPLA.NS","DRREDDY.NS","APOLLOHOSP.NS"],"weight":6},
"Metal": {"sector":"METAL","stocks":["JSWSTEEL.NS","HINDALCO.NS","TATASTEEL.NS","GRASIM.NS"],"weight":5},
"FMCG": {"sector":"FMCG","stocks":["ITC.NS","BRITANNIA.NS","NESTLEIND.NS","HINDUNILVR.NS","TITAN.NS","TRENT.NS","LT.NS","ULTRACEMCO.NS"],"weight":8},
"Telecom": {"sector":"TELECOM","stocks":["BHARTIARTL.NS"],"weight":3},
}

ALL_STOCKS = []
for v in INDUSTRY_MAP.values():
    ALL_STOCKS.extend(v["stocks"])
ALL_STOCKS = list(dict.fromkeys(ALL_STOCKS))

SECTOR_GROUP = {}
for ind, data in INDUSTRY_MAP.items():
    sec = data["sector"]
    if sec not in SECTOR_GROUP:
        SECTOR_GROUP[sec] = []
    SECTOR_GROUP[sec].extend(data["stocks"])
for sec in SECTOR_GROUP:
    SECTOR_GROUP[sec] = list(dict.fromkeys(SECTOR_GROUP[sec]))

@st.cache_data(ttl=120)
def get_ltp(sym):
    try:
        t = yf.Ticker(sym)
        df = t.history(period="1d", interval="5m")
        if len(df) > 0:
            ltp = float(df['Close'].iloc[-1])
            prev = float(t.info.get('previousClose', ltp))
            chg = (ltp - prev) / prev * 100
            return ltp, chg
    except:
        pass
    return None, None

@st.cache_data(ttl=300)
def get_chain_one(sym):
    try:
        t = yf.Ticker(sym)
        exps = t.options
        if not exps:
            return None
        exp = exps[0]
        oc = t.option_chain(exp)
        calls = oc.calls
        puts = oc.puts
        ltp, chg = get_ltp(sym)
        if ltp is None:
            return None
        calls['diff'] = abs(calls['strike'] - ltp)
        atm = calls.loc[calls['diff'].idxmin()]['strike']
        chain = pd.merge(calls[['strike','lastPrice','bid','ask','volume','openInterest']], puts[['strike','lastPrice','bid','ask','volume','openInterest']], on='strike', suffixes=('_CE','_PE'), how='outer')
        chain = chain[(chain['strike'] >= atm-300) & (chain['strike'] <= atm+300)].sort_values('strike')
        if chg > 1:
            rec = "STRONG BUY CE"
            act = f"BUY {atm} CE"
            score = 10
        elif chg > 0.3:
            rec = "BUY CE"
            act = f"BUY {atm+50} CE"
            score = 6
        elif chg < -1:
            rec = "STRONG BUY PE"
            act = f"BUY {atm} PE"
            score = -10
        elif chg < -
