import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import pytz
import time
import math

st.set_page_config(page_title="MIND MAP NIFTY", layout="wide", page_icon="🧠")
st.title("🧠 NIFTY MIND MAP - Branches - BUY/SELL + OPTION CHAIN + PAST DATA")
ist = pytz.timezone('Asia/Kolkata')
st.markdown(f"### REAL NSE - {datetime.now(ist).strftime('%d-%m-%Y %H:%M:%S IST')}")

INDUSTRY_MAP = {
"Financial Services": {"sector":"BANKING","stocks":["HDFCBANK.NS","ICICIBANK.NS","SBIN.NS","KOTAKBANK.NS","AXISBANK.NS","INDUSINDBK.NS","BAJFINANCE.NS","BAJAJFINSV.NS"],"weight":38,"color":"#00ff88"},
"IT": {"sector":"IT","stocks":["TCS.NS","INFY.NS","WIPRO.NS","HCLTECH.NS","TECHM.NS","LTIM.NS"],"weight":14,"color":"#00aaff"},
"Energy": {"sector":"ENERGY","stocks":["RELIANCE.NS","ONGC.NS","BPCL.NS","COALINDIA.NS","NTPC.NS","POWERGRID.NS"],"weight":12,"color":"#ffaa00"},
"Auto": {"sector":"AUTO","stocks":["MARUTI.NS","M&M.NS","BAJAJ-AUTO.NS","HEROMOTOCO.NS","EICHERMOT.NS","MOTHERSON.NS"],"weight":8,"color":"#ff4444"},
"Healthcare": {"sector":"PHARMA","stocks":["SUNPHARMA.NS","DIVISLAB.NS","CIPLA.NS","DRREDDY.NS","APOLLOHOSP.NS"],"weight":6,"color":"#ff00ff"},
"Metal": {"sector":"METAL","stocks":["JSWSTEEL.NS","HINDALCO.NS","TATASTEEL.NS","GRASIM.NS"],"weight":5,"color":"#8888ff"},
"FMCG": {"sector":"FMCG","stocks":["ITC.NS","BRITANNIA.NS","NESTLEIND.NS","HINDUNILVR.NS","TITAN.NS","TRENT.NS"],"weight":8,"color":"#ffff00"},
}

ALL_STOCKS = list(dict.fromkeys([s for v in INDUSTRY_MAP.values() for s in v["stocks"]]))

@st.cache_data(ttl=120)
def get_ltp(sym):
    try:
        t=yf.Ticker(sym)
        df=t.history(period="5d", interval="1d")
        hist=t.history(period="1d", interval="5m")
        if len(df)>0:
            ltp=float(df['Close'].iloc[-1])
            prev=float(df['Close'].iloc[-2]) if len(df)>1 else ltp
            chg=(ltp-prev)/prev*100
            change_1d = ((df['Close'].iloc[-1]-df['Close'].iloc[-2])/df['Close'].iloc[-2]*100) if len(df)>1 else 0
            change_5d = ((df['Close'].iloc[-1]-df['Close'].iloc[0])/df['Close'].iloc[0]*100) if len(df)>0 else 0
            return ltp, chg, change_1d, change_5d, df, hist
    except: pass
    return None,None,None,None,None,None

@st.cache_data(ttl=300)
def get_chain_one(sym):
    try:
        t=yf.Ticker(sym)
        exps=t.options
        if not exps: return None
        exp=exps[0]
        oc=t.option_chain(exp)
        calls=oc.calls
        puts=oc.puts
        ltp,chg,c1,c5,df,hist=get_ltp(sym)
        if ltp is None: return None
        calls['diff']=abs(calls['strike']-ltp)
        atm=calls.loc[calls['diff'].idxmin()]['strike']
        chain=pd.merge(calls[['strike','lastPrice','volume','openInterest']], puts[['strike','lastPrice','volume','openInterest']], on='strike', suffixes=('_CE','_PE'), how='outer')
        chain=chain[(chain['strike']>=atm-300) & (chain['strike']<=atm+300)].sort_values('strike')
        if chg>1: rec="STRONG BUY CE"; score=10
        elif chg>0.3: rec="BUY CE"; score=6
        elif chg<-1: rec="STRONG BUY PE"; score=-10
        elif chg<-0.3: rec="BUY PE"; score=-6
        else: rec="NEUTRAL"; score=0
        return {"symbol":sym.replace(".NS",""), "full":sym, "ltp":ltp, "chg":chg, "c1":c1, "c5":c5, "atm":atm, "chain":chain, "rec":rec, "score":score, "exp":exp, "hist":hist, "df":df}
    except:
        return None

# FETCH ALL
view=st.radio("Mind Map View", ["ALL 50 (60s)","BANKING","IT","ENERGY","AUTO","PHARMA"], index=0, horizontal=True)
if view=="ALL 50 (60s)": stocks_to_show=ALL_STOCKS
else:
    key=list(INDUSTRY_MAP.keys())[["BANKING","IT","ENERGY","AUTO","PHARMA"].index(view)] if view!="ALL 50 (60s)" else "Financial Services"
    # simple mapping
    if view=="BANKING": stocks_to_show=INDUSTRY_MAP["Financial Services"]["stocks"]
    elif view=="IT": stocks_to_show=INDUSTRY_MAP["IT"]["stocks"]
    elif view=="ENERGY": stocks_to_show=INDUSTRY_MAP["Energy"]["stocks"]
    elif view=="AUTO": stocks_to_show=INDUSTRY_MAP["Auto"]["stocks"]
    elif view=="PHARMA": stocks_to_show=INDUSTRY_MAP["Healthcare"]["stocks"]
    else: stocks_to_show=ALL_STOCKS

if st.button("GENERATE MIND MAP", type="primary"):
    st.cache_data.clear()
    st.rerun()

progress=st.progress(0)
chains=[]
for i,sym in enumerate(stocks_to_show):
    progress.progress((i+1)/len(stocks_to_show))
    data=get_chain_one(sym)
   
