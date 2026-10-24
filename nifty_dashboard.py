import streamlit as st
import pandas as pd
import requests, io, warnings
warnings.filterwarnings("ignore")
from tradingview_ta import TA_Handler, Interval
from datetime import datetime

st.set_page_config(page_title="⚡ TradingView Nifty LIVE", layout="wide")

TELEGRAM_BOT_TOKEN = "8945760262:AAEfs1uofPGbMXRGsYH6Z6QMPvhjFo_Ki38"
TELEGRAM_CHAT_ID = "531385858"

def send_telegram(msg):
    try:
        requests.post(f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage", data={"chat_id": TELEGRAM_CHAT_ID, "text": msg}, timeout=5)
    except: pass

@st.cache_data(ttl=60)  # Cache 1 min
def get_tv_analysis(symbol, interval=Interval.INTERVAL_15_MINUTES):
    try:
        handler = TA_Handler(
            symbol=symbol,
            exchange="NSE",
            screener="india",
            interval=interval
        )
        analysis = handler.get_analysis()
        s = analysis.summary
        ind = analysis.indicators
        
        # Calculate SL/TGT
        ltp = ind.get("close", 0)
        atr = ind.get("ATR", ltp*0.02)
        signal = s.get("RECOMMENDATION", "NEUTRAL")
        
        # Convert TradingView signal to our format
        if "STRONG_BUY" in signal: score=8
        elif "BUY" in signal: score=4
        elif "STRONG_SELL" in signal: score=-8
        elif "SELL" in signal: score=-4
        else: score=0
        
        sl = ltp - 1.5*atr if score>0 else ltp + 1.5*atr
        t1 = ltp + 2*atr if score>0 else ltp - 2*atr
        
        return {
            "Symbol": symbol,
            "LTP": round(ltp,2),
            "Signal": signal.replace("_"," "),
            "Score": score,
            "RSI": round(ind.get("RSI", 0),1),
            "MACD": round(ind.get("MACD.macd", 0),2),
            "EMA20": round(ind.get("EMA20", 0),2),
            "Buy": s.get("BUY",0),
            "Sell": s.get("SELL",0),
            "Entry": round(ltp,2),
            "SL": round(sl,2),
            "T1": round(t1,2),
            "Option": f"{round(ltp/50)*50} {'CE' if score>0 else 'PE'}"
        }
    except Exception as e:
        return None

# STOCKS
INDICES = {
    "NIFTY 50": ["RELIANCE","TCS","INFY","HDFCBANK","ICICIBANK","SBIN","BHARTIARTL","ITC","LT","KOTAKBANK","AXISBANK","BAJFINANCE","ASIANPAINT","MARUTI","WIPRO","HCLTECH","SUNPHARMA","TITAN","ULTRACEMCO","NESTLEIND"],
    "BANKNIFTY": ["HDFCBANK","ICICIBANK","SBIN","KOTAKBANK","AXISBANK","INDUSINDBK","BANDHANBNK","PNB","IDFCFIRSTB","FEDERALBNK"],
    "FINNIFTY": ["HDFCBANK","ICICIBANK","BAJFINANCE","BAJAJFINSV","SBILIFE","HDFCLIFE","ICICIPRULI","PFC","RECLTD","CHOLAFIN"]
}

st.title("⚡ TradingView LIVE - 5 Sec Load")

interval_choice = st.selectbox("Timeframe", ["15m","1h","1D"], index=0)
interval_map = {"15m": Interval.INTERVAL_15_MINUTES, "1h": Interval.INTERVAL_1_HOUR, "1D": Interval.INTERVAL_1_DAY}
selected_interval = interval_map[interval_choice]

c1,c2 = st.columns([1,4])
if c1.button("🔄 Refresh NOW"):
    st.cache_data.clear()
    st.rerun()
if c2.button("🔔 Test Telegram"):
    send_telegram(f"⚡ TradingView LIVE Working - {datetime.now()}")
    st.success("Sent!")

tab1, tab2, tab3 = st.tabs(["NIFTY 50", "BANKNIFTY", "FINNIFTY"])

all_results=[]
for tab_name, tab in zip(INDICES.keys(), [tab1, tab2, tab3]):
    with tab:
        st.subheader(f"{tab_name} - {interval_choice} Signals")
        symbols = INDICES[tab_name]
        results=[]
        prog = st.progress(0, text="Loading from TradingView...")
        for i,sym in enumerate(symbols):
            r = get_tv_analysis(sym, selected_interval)
            if r:
                r["Index"]=tab_name
                results.append(r)
                all_results.append(r)
            prog.progress((i+1)/len(symbols), text=f"{sym} - {r['Signal'] if r else '...'}")
        prog.empty()
        
        if results:
            df = pd.DataFrame(results).sort_values("Score", ascending=False)
            st.dataframe(df, use_container_width=True, height=500)
            
            # Top signal alert
            top = df.iloc[0]
            if "STRONG" in top["Signal"]:
                st.balloons()
                if st.button(f"🚨 Send {top['Symbol']} {top['Signal']} to Telegram", key=tab_name):
                    send_telegram(f"🚨 {tab_name} {top['Signal']} {top['Symbol']} @ {top['LTP']} RSI:{top['RSI']} Option:{top['Option']} SL:{top['SL']} T1:{top['T1']}")

# LIVE EXCEL DOWNLOAD
if all_results:
    df_all = pd.DataFrame(all_results)
    buf = io.BytesIO()
    with pd.ExcelWriter(buf, engine='openpyxl') as writer:
        df_all.to_excel(writer, sheet_name='TradingView_Live', index=False)
        for idx in INDICES.keys():
            df_idx = df_all[df_all["Index"]==idx]
            if not df_idx.empty:
                df_idx.to_excel(writer, sheet_name=idx[:31], index=False)
    
    st.download_button(
        "📥 DOWNLOAD LIVE EXCEL (TradingView)",
        buf.getvalue(),
        f"TradingView_LIVE_{datetime.now().strftime('%Y%m%d_%H%M')}.xlsx",
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        type="primary"
    )

st.info(f"⚡ Last Updated: {datetime.now().strftime('%H:%M:%S')} | Data from TradingView | Loads in 5 sec | Cache 60 sec")
