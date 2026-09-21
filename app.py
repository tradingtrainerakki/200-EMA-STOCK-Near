import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime
import time

st.set_page_config(page_title="NSE Screener 200 EMA", page_icon="📈", layout="wide")
st.title("📈 NSE Stock Screener — Uptrend + 200 EMA")

st.sidebar.header("⚙️ Settings")
near_ema_pct = st.sidebar.slider("200 EMA ke aaspaas % range", 1.0, 20.0, 5.0, 0.5)
ema_period = st.sidebar.number_input("EMA Period", value=200, min_value=20, max_value=500)
lookback = st.sidebar.selectbox("Lookback Period", ["6mo", "1y", "2y"], index=1)
batch_delay = st.sidebar.slider("Delay per stock (sec)", 0.1, 2.0, 0.5, 0.1)

NSE_STOCKS = [
    "RELIANCE.NS","TCS.NS","HDFCBANK.NS","INFY.NS","ICICIBANK.NS",
    "HINDUNILVR.NS","ITC.NS","SBIN.NS","BHARTIARTL.NS","KOTAKBANK.NS",
    "LT.NS","AXISBANK.NS","ASIANPAINT.NS","MARUTI.NS","BAJFINANCE.NS",
    "HCLTECH.NS","WIPRO.NS","SUNPHARMA.NS","TITAN.NS","ULTRACEMCO.NS",
    "NESTLEIND.NS","POWERGRID.NS","NTPC.NS","TATAMOTORS.NS","TATASTEEL.NS",
    "M&M.NS","ADANIENT.NS","ADANIPORTS.NS","JSWSTEEL.NS","GRASIM.NS",
    "TECHM.NS","INDUSINDBK.NS","HINDALCO.NS","BAJAJFINSV.NS","DRREDDY.NS",
    "CIPLA.NS","BRITANNIA.NS","COALINDIA.NS","DIVISLAB.NS","EICHERMOT.NS",
    "HEROMOTOCO.NS","APOLLOHOSP.NS","BPCL.NS","TATACONSUM.NS","SBILIFE.NS",
    "HDFCLIFE.NS","BAJAJ-AUTO.NS","ONGC.NS","UPL.NS","LTIM.NS",
    "DMART.NS","PIDILITIND.NS","GODREJCP.NS","DABUR.NS","MARICO.NS",
    "SIEMENS.NS","HAVELLS.NS","VOLTAS.NS","CUMMINSIND.NS","ABB.NS",
    "TRENT.NS","ZOMATO.NS","PAYTM.NS","NYKAA.NS","POLICYBZR.NS",
    "AMBUJACEM.NS","BANKBARODA.NS","BERGEPAINT.NS","BIOCON.NS","BOSCHLTD.NS",
    "CANBK.NS","CHOLAFIN.NS","COLPAL.NS","DLF.NS","GAIL.NS",
    "GODREJPROP.NS","ICICIGI.NS","ICICIPRULI.NS","IOC.NS","INDHOTEL.NS",
    "INDIGO.NS","JINDALSTEL.NS","JIOFIN.NS","LICI.NS","LODHA.NS",
    "LTF.NS","MOTHERSON.NS","NAUKRI.NS","PFC.NS","RECLTD.NS",
    "SHREECEM.NS","SRF.NS","TVSMOTOR.NS","TORNTPHARM.NS","VBL.NS",
    "VEDL.NS","ZYDUSLIFE.NS","MUTHOOTFIN.NS","PGHH.NS","FEDERALBNK.NS",
    "IDFCFIRSTB.NS","BANDHANBNK.NS","RBLBANK.NS","AUBANK.NS","YESBANK.NS",
    "PNB.NS","UNIONBANK.NS","INDIANB.NS","CENTRALBK.NS","BAJAJHLDNG.NS",
    "MANAPPURAM.NS","SBICARD.NS","HDFCAMC.NS","NIPPONAMC.NS","UTIAMC.NS",
    "ABCAPITAL.NS","PEL.NS","SHRIRAMFIN.NS","POONAWALLA.NS","CANFINHOME.NS",
    "LICHSGFIN.NS","IIFL.NS","PERSISTENT.NS","COFORGE.NS","MPHASIS.NS",
    "LTTS.NS","KPITTECH.NS","TATAELXSI.NS","CYIENT.NS","SONACOMS.NS",
    "TATATECH.NS","ZENSARTECH.NS","HEXAWARE.NS","NIITTECH.NS","OFSS.NS",
    "HAPPSTMNDS.NS","NEWGEN.NS","MASTEK.NS","BIRLASOFT.NS","ALKEM.NS",
    "LUPIN.NS","AUROPHARMA.NS","IPCALAB.NS","GLENMARK.NS","NATCOPHARM.NS",
    "AJANTPHARM.NS","GRANULES.NS","LAURUSLABS.NS","ABBOTINDIA.NS","PFIZER.NS",
    "SANOFI.NS","GLAXO.NS","SYNGENE.NS","MAXHEALTH.NS","FORTIS.NS",
    "NH.NS","ASTERDM.NS","ASHOKLEY.NS","ESCORTS.NS","BALKRISIND.NS",
    "MRF.NS","APOLLOTYRE.NS","CEATLTD.NS","JKTYRE.NS","EXIDEIND.NS",
    "AMARAJABAT.NS","SUNDRMFAST.NS","ENDURANCE.NS","SAIL.NS","NMDC.NS",
    "NATIONALUM.NS","HINDZINC.NS","APLAPOLLO.NS","RATNAMANI.NS","WELCORP.NS",
    "JSL.NS","MOIL.NS","GRAVITA.NS","EMAMILTD.NS","JYOTHYLAB.NS",
    "BAJAJCON.NS","HONASA.NS","RADICO.NS","UNITDSPR.NS","PATANJALI.NS",
    "BIKAJI.NS","DEVYANI.NS","JUBLFOOD.NS","HINDPETRO.NS","PETRONET.NS",
    "IGL.NS","MGL.NS","GUJGASLTD.NS","TATAPOWER.NS","ADANIPOWER.NS",
    "JSWENERGY.NS","ACC.NS","DALBHARAT.NS","JKCEMENT.NS","RAMCOCEM.NS",
    "HEIDELBERG.NS","BIRLACORPN.NS","GMRAIRPORT.NS","IRB.NS","KNRCON.NS",
    "NCC.NS","GPIL.NS","IRCON.NS","RVNL.NS","TITAGARH.NS",
    "TEXRAIL.NS","AARTIIND.NS","DEEPAKNTR.NS","NAVINFLUOR.NS","ATUL.NS",
    "VINATIORGA.NS","TATACHEM.NS","GNFC.NS","GSFC.NS","CHAMBLFERT.NS",
    "COROMANDEL.NS","PIIND.NS","SUMICHEM.NS","OBEROIRLTY.NS","PRESTIGE.NS",
    "BRIGADE.NS","SOBHA.NS","PHOENIXLTD.NS","MAHLIFE.NS","SUNTECK.NS",
    "KOLTEPATIL.NS","IDEA.NS","TATACOMM.NS","INDUSTOWER.NS","HFCL.NS",
    "TEJASNET.NS","ITI.NS","ZEEL.NS","SUNTV.NS","PVRINOX.NS",
    "MAXFIN.NS","STARHEALTH.NS","NIACL.NS","BEL.NS","HAL.NS",
    "BHEL.NS","BEML.NS","MDL.NS","COCHINSHIP.NS","GRSE.NS",
    "MAZDOCK.NS","BDL.NS","DATAPATTNS.NS","PARAS.NS","MIDHANI.NS",
    "SOLARINDS.NS","ASTRAL.NS","APARINDS.NS","IRCTC.NS","IRFC.NS",
    "HUDCO.NS","CGPOWER.NS","THERMAX.NS","BLUESTARCO.NS","CROMPTON.NS",
]
NSE_STOCKS = list(dict.fromkeys(NSE_STOCKS))

def calc(data, p):
    d = data.copy()
    d['E200'] = d['Close'].ewm(span=p, adjust=False).mean()
    d['E50'] = d['Close'].ewm(span=50, adjust=False).mean()
    d['E20'] = d['Close'].ewm(span=20, adjust=False).mean()
    return d

def check(ticker, p, near, lb):
    try:
        t = yf.Ticker(ticker)
        d = t.history(period="2y", auto_adjust=True)  # 2y fetch karo (1y strict check ke liye)
        
        # ✅ Today's incomplete candle remove
        if len(d) > 1:
            d = d.iloc[:-1]
        
        # Minimum 1 year data hona chahiye
        if d.empty or len(d) < 250:
            return None
        
        # EMA calculate
        d['E200'] = d['Close'].ewm(span=p, adjust=False).mean()
        d['E50'] = d['Close'].ewm(span=50, adjust=False).mean()
        d['E20'] = d['Close'].ewm(span=20, adjust=False).mean()
        
        # ============================================================
        # 🚨 STRICT CONDITION 1: Pichhle 1 saal me EMA kabhi price ke upar nahi aayi
        # ============================================================
        # Last 250 trading days (1 year) ka data
        last_1y = d.tail(250)
        
        # Har din check karo: kya Close > EMA_200 tha?
        # Agar kabhi bhi Close <= EMA_200 hua, to 'all()' False dega
        always_above_ema = (last_1y['Close'] > last_1y['E200']).all()
        
        if not always_above_ema:
            return None  # ❌ Reject — kabhi bhi price 200 EMA ke neeche gaya
        
        # ============================================================
        # 🚨 STRICT CONDITION 2: 200 EMA khud bhi pichhle 1 saal me rising ho
        # ============================================================
        ema_start = float(last_1y['E200'].iloc[0])   # 1 saal pehle ki EMA
        ema_now = float(last_1y['E200'].iloc[-1])    # aaj ki EMA
        
        if ema_now <= ema_start:
            return None  # ❌ Reject — 200 EMA flat ya falling hai
        
        # ============================================================
        # Baaki conditions
        # ============================================================
        L = d.iloc[-1]
        c = float(L['Close'])
        e200 = float(L['E200'])
        e50 = float(L['E50'])
        e20 = float(L['E20'])
        
        dist = ((c - e200) / e200) * 100
        is_stack = (e20 > e50) and (e50 > e200)
        chg5 = ((c - float(d['Close'].iloc[-6])) / float(d['Close'].iloc[-6])) * 100 if len(d) >= 6 else 0
        
        # Strict EMA rise % over 1 year
        ema_rise_pct = ((ema_now - ema_start) / ema_start) * 100
        
        # ============================================================
        # 🎯 FINAL FILTER
        # ============================================================
        if (c > e200 and              # Price above 200 EMA (aaj)
            c > e50 and               # Price above 50 EMA (aaj)
            abs(dist) <= near and     # Near 200 EMA (±5%)
            is_stack and              # Bullish stack 20>50>200
            always_above_ema and      # ✅ 1 saal strict check
            ema_now > ema_start):     # ✅ 1 saal EMA rising
            
            return {
                "Ticker": ticker.replace(".NS",""),
                "Price": round(c, 2),
                "200_EMA": round(e200, 2),
                "50_EMA": round(e50, 2),
                "20_EMA": round(e20, 2),
                "Distance_%": round(dist, 2),
                "EMA_1Y_Rise_%": round(ema_rise_pct, 2),   # ⭐ Naya column
                "Bullish_Stack": "✅",
                "EMA_Rising": "✅",
                "5D_Change_%": round(chg5, 2),
                "Volume": int(L['Volume']),
            }
        return None
    except Exception:
        return None

run_btn = st.sidebar.button("🚀 Run Screener", type="primary", use_container_width=True)

if run_btn:
    st.info(f"🔍 Scanning {len(NSE_STOCKS)} stocks... Please wait.")
    prog = st.progress(0); status = st.empty()
    results = []; total = len(NSE_STOCKS)
    for i, tk in enumerate(NSE_STOCKS, 1):
        status.text(f"[{i}/{total}] {tk}...")
        r = check(tk, ema_period, near_ema_pct, lookback)
        if r: results.append(r)
        prog.progress(i/total)
        time.sleep(batch_delay)
    status.empty(); prog.empty()
    if not results:
        st.warning("❌ Koi stock match nahi hua. Sidebar me near_ema_pct badha kar try karein.")
    else:
        df = pd.DataFrame(results).sort_values("Distance_%", key=lambda x: abs(x)).reset_index(drop=True)
        st.success(f"✅ Total {len(df)} stocks mile!")
        st.subheader("📊 Results"); st.dataframe(df, use_container_width=True)
        st.subheader("🎯 Top 10 Closest to 200 EMA")
        st.dataframe(df.head(10)[["Ticker","Price","200_EMA","Distance_%","Bullish_Stack","EMA_Rising"]], use_container_width=True)
        st.download_button("💾 Download CSV", df.to_csv(index=False).encode('utf-8'),
                           f"results_{datetime.now().strftime('%Y%m%d_%H%M')}.csv", "text/csv", use_container_width=True)
        st.warning("⚠️ Ye tool sirf analysis ke liye hai. Investment advice nahi.")
else:
    st.info("👈 Sidebar me settings choose karein aur **Run Screener** button dabayein.")
