import streamlit as st
import pandas as pd, requests, warnings, time, io
warnings.filterwarnings("ignore")
from tradingview_ta import TA_Handler, Interval
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime

st.set_page_config(page_title="⚡ NIFTY FULL PRO", layout="wide", page_icon="📈")
st.title("⚡ NIFTY BANKNIFTY FINNIFTY - FULL PRO - 1 SEC LOAD")

# ---------- CONFIG ----------
ALL_STOCKS = {
 "NIFTY50": ["RELIANCE","TCS","INFY","HDFCBANK","ICICIBANK","SBIN","BHARTIARTL","ITC","LT","KOTAKBANK","AXISBANK","BAJFINANCE","ASIANPAINT","MARUTI","WIPRO","HCLTECH","SUNPHARMA","TITAN","ULTRACEMCO","ONGC","NTPC","POWERGRID","M&M","TATAMOTORS","TATASTEEL","JSWSTEEL","ADANIENT","ADANIPORTS","COALINDIA","GRASIM","BPCL","BAJAJFINSV","BRITANNIA","CIPLA","DRREDDY","EICHERMOT","HDFCLIFE","HEROMOTOCO","HINDALCO","INDUSINDBK","NESTLEIND","SBILIFE","SHRIRAMFIN","TECHM","APOLLOHOSP","DIVISLAB","LTIM"],
 "BANKNIFTY": ["HDFCBANK","ICICIBANK","SBIN","KOTAKBANK","AXISBANK","INDUSINDBK","BANDHANBNK","FEDERALBNK","IDFCFIRSTB","PNB","BANKBARODA","AUBANK"],
 "FINNIFTY": ["BAJFINANCE","BAJAJFINSV","HDFC","HDFCLIFE","SBILIFE","ICICIPRULI","CHOLAFIN","SHRIRAMFIN"],
 "MIDCAP": ["PERSISTENT","MPHASIS","COFORGE","KPITTECH"]
}
INDEX_MAP = {"NIFTY":"NIFTY","BANKNIFTY":"BANKNIFTY","FINNIFTY":"CNXFINANCE"}
ALL_SYMBOLS = list(set(sum(ALL_STOCKS.values(), [])))

# ---------- FAST TV FETCHER ----------
@st.cache_data(ttl=20, show_spinner=False)
def fetch_one(symbol, interval_str):
    try:
        interval = {"15m":Interval.INTERVAL_15_MINUTES,"1h":Interval.INTERVAL_1_HOUR,"1D":Interval.INTERVAL_1_DAY}[interval_str]
        h = TA_Handler(symbol=symbol, exchange="NSE", screener="india", interval=interval)
        a = h.get_analysis()
        s, ind = a.summary, a.indicators
        ltp = ind.get("close",0)
        atr, rsi = ind.get("ATR", ltp*0.02), ind.get("RSI",50)
        ema20, ema50 = ind.get("EMA20",ltp), ind.get("EMA50",ltp)
        sig = s.get("RECOMMENDATION","NEUTRAL")
        
        # SCORING LOGIC
        score = 0
        if "STRONG_BUY" in sig: score=10
        elif "BUY" in sig: score=6
        elif "STRONG_SELL" in sig: score=-10
        elif "SELL" in sig: score=-6
        if rsi>60: score+=2
        if rsi<40: score-=2
        if ema20>ema50: score+=2
        else: score-=2
        
        # TREND + ACTION
        if score>=8: trend, action, color = "STRONG BULLISH", "BUY CE", "green"
        elif score>=4: trend, action, color = "BULLISH", "BUY CE / HOLD", "lightgreen"
        elif score<=-8: trend, action, color = "STRONG BEARISH", "BUY PE", "red"
        elif score<=-4: trend, action, color = "BEARISH", "BUY PE / HOLD", "orange"
        else: trend, action, color = "SIDEWAYS", "WAIT", "gray"
        
        # OPTIONS DATA
        strike = round(ltp/50)*50 if ltp<5000 else round(ltp/100)*100
        sl = ltp-1.5*atr if score>0 else ltp+1.5*atr
        t1, t2 = (ltp+2*atr, ltp+3.5*atr) if score>0 else (ltp-2*atr, ltp-3.5*atr)
        
        return {
            "Symbol":symbol, "LTP":round(ltp,2), "Trend":trend, "Action":action, "Score":score,
            "Signal":sig.replace("_"," "), "RSI":round(rsi,1), "EMA20>50":"YES" if ema20>ema50 else "NO",
            "Strike":strike, "Option":f"{strike} {'CE' if score>0 else 'PE'}", 
            "SL":round(sl,2), "T1":round(t1,2), "T2":round(t2,2), "Color":color
        }
    except: return None

def fetch_fast(symbols, interval, max_workers=15):
    results=[]
    with ThreadPoolExecutor(max_workers=max_workers) as ex:
        futures = {ex.submit(fetch_one, s, interval): s for s in symbols}
        for f in as_completed(futures):
            r=f.result()
            if r: results.append(r)
    return results

# ---------- UI ----------
c1,c2,c3,c4 = st.columns(4)
with c1: idx_filter = st.selectbox("Index", ["ALL","NIFTY50","BANKNIFTY","FINNIFTY","MIDCAP"])
with c2: tf = st.selectbox("Timeframe", ["15m","1h","1D"], index=0)
with c3: auto = st.checkbox("⚡ Auto Refresh 5 sec")
with c4: st.metric("Time", datetime.now().strftime("%H:%M:%S"))

symbols_to_load = ALL_SYMBOLS if idx_filter=="ALL" else ALL_STOCKS[idx_filter]

# INSTANT LOAD FIRST 5
placeholder = st.empty()
table_ph = st.empty()

start = time.time()
first_batch = symbols_to_load[:8]
with st.spinner(f"Loading first 8 stocks..."):
    res1 = fetch_fast(first_batch, tf, max_workers=8)
    if res1:
        df1 = pd.DataFrame(res1).sort_values("Score", ascending=False)
        table_ph.dataframe(df1[["Symbol","LTP","Trend","Action","Score","RSI","Option","SL","T1","T2"]], use_container_width=True, height=400)
        placeholder.success(f"✅ LIVE {len(res1)} stocks in {time.time()-start:.1f}s - Loading rest in background...")

# BACKGROUND LOAD REST
if len(symbols_to_load)>8:
    res2 = fetch_fast(symbols_to_load[8:], tf, max_workers=20)
    all_res = res1 + res2
else:
    all_res = res1

df_all = pd.DataFrame(all_res).sort_values("Score", ascending=False)

# COLOR CODING
def color_row(row):
    if row["Score"]>=8: return ['background-color: #d4edda']*len(row)
    if row["Score"]<=-8: return ['background-color: #f8d7da']*len(row)
    return ['']*len(row)

st.divider()
st.subheader(f"📊 FULL LIVE DASHBOARD - {idx_filter} - {len(df_all)} Stocks - Updated {datetime.now().strftime('%H:%M:%S')}")

st.dataframe(df_all.style.apply(color_row, axis=1), use_container_width=True, height=700)

# ---------- OPTIONS SUMMARY ----------
st.divider()
c1,c2 = st.columns(2)
with c1:
    st.subheader("🔥 TOP BUY (CE)")
    st.dataframe(df_all[df_all["Score"]>=4][["Symbol","LTP","Strike","Option","T1","T2"]].head(10), use_container_width=True)
with c2:
    st.subheader("🔻 TOP SELL (PE)")
    st.dataframe(df_all[df_all["Score"]<=-4][["Symbol","LTP","Strike","Option","T1","T2"]].head(10), use_container_width=True)

# ---------- INDEX OPTIONS ----------
st.divider()
st.subheader("📈 INDEX Options - NIFTY / BANKNIFTY / FINNIFTY")
idx_data=[]
for name, tv_sym in INDEX_MAP.items():
    r = fetch_one(tv_sym, tf)
    if r:
        r["Index"]=name
        idx_data.append(r)
if idx_data:
    df_idx = pd.DataFrame(idx_data)
    st.dataframe(df_idx[["Index","LTP","Trend","Action","Option","SL","T1"]], use_container_width=True)

# ---------- DOWNLOAD ----------
buf = io.BytesIO()
with pd.ExcelWriter(buf, engine='openpyxl') as w:
    df_all.to_excel(w, sheet_name="All_Stocks", index=False)
    df_all[df_all["Score"]>=4].to_excel(w, sheet_name="BUY_CE", index=False)
    df_all[df_all["Score"]<=-4].to_excel(w, sheet_name="BUY_PE", index=False)

st.download_button("📥 DOWNLOAD FULL EXCEL - LIVE + OPTIONS + SUGGESTIONS", buf.getvalue(), f"FULL_NIFTY_{datetime.now().strftime('%d%m%H%M')}.xlsx", type="primary", use_container_width=True)

if auto:
    time.sleep(5)
    st.cache_data.clear()
    st.rerun()

if st.button("🔄 REFRESH 1 SEC"):
    st.cache_data.clear()
    st.rerun()
