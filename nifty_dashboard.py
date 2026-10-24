import streamlit as st
st.set_page_config(page_title="FAST", layout="wide")
st.title("⚡ LIVE Nifty - Out of Oven!")

try:
    from tradingview_ta import TA_Handler, Interval
    st.success("TradingView installed OK!")
    
    @st.cache_data(ttl=60)
    def get_price(sym):
        try:
            h = TA_Handler(symbol=sym, exchange="NSE", screener="india", interval=Interval.INTERVAL_15_MINUTES)
            a = h.get_analysis()
            return {"Symbol":sym, "Price":a.indicators["close"], "Signal":a.summary["RECOMMENDATION"]}
        except Exception as e:
            return {"Symbol":sym, "Price":0, "Signal":str(e)[:50]}
    
    if st.button("Load RELIANCE"):
        r = get_price("RELIANCE")
        st.json(r)
        
except Exception as e:
    st.error(f"Error: {e}")
    st.info("Install tradingview-ta in requirements.txt")
