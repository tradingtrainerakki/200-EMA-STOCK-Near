import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime
import time

# ============================================================
# PAGE CONFIG
# ============================================================
st.set_page_config(
    page_title="NSE Stock Screener — 200 EMA",
    page_icon="📈",
    layout="wide"
)

st.title("📈 NSE Stock Screener — Uptrend + 200 EMA")
st.markdown("**200 NSE stocks** scan karta hai jo **pure uptrend** me hain aur 200 EMA ke aaspaas trade kar rahe hain.")

# ============================================================
# SIDEBAR CONTROLS
# ============================================================
st.sidebar.header("⚙️ Basic Settings")

near_ema_pct = st.sidebar.slider(
    "200 EMA ke aaspaas % range",
    min_value=1.0, max_value=20.0, value=5.0, step=0.5,
    help="Stock 200 EMA ke kitne % andar ho"
)

ema_period = st.sidebar.number_input(
    "EMA Period", value=200, min_value=20, max_value=500
)

batch_delay = st.sidebar.slider(
    "Delay per stock (sec)", 0.1, 2.0, 0.3, 0.1,
    help="Rate limit avoid karne ke liye"
)

st.sidebar.markdown("---")
st.sidebar.subheader("🎯 Quality Filters")

min_above_pct = st.sidebar.slider(
    "Min % days above 200 EMA (1 year)",
    min_value=70, max_value=100, value=95, step=1,
    help="95 = Best balance. 100 = Strictest (kam stocks). 70 = Loose (zyada stocks)"
)

min_ema_rise = st.sidebar.slider(
    "Min 200 EMA rise % (1 year)",
    min_value=0.0, max_value=100.0, value=5.0, step=1.0,
    help="200 EMA pichhle 1 saal me kitna % upar gayi"
)

strict_stack = st.sidebar.checkbox(
    "🔒 Require Bullish EMA Stack (20>50>200)",
    value=True,
    help="Short + medium + long term sab bullish ho"
)

# ============================================================
# 200 NSE STOCKS
# ============================================================
NSE_STOCKS = [
    # NIFTY 50
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
    # NIFTY NEXT 50
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
    # Banking & Finance
    "IDFCFIRSTB.NS","BANDHANBNK.NS","RBLBANK.NS","AUBANK.NS","YESBANK.NS",
    "PNB.NS","UNIONBANK.NS","INDIANB.NS","CENTRALBK.NS","BAJAJHLDNG.NS",
    "MANAPPURAM.NS","SBICARD.NS","HDFCAMC.NS","NIPPONAMC.NS","UTIAMC.NS",
    "ABCAPITAL.NS","PEL.NS","SHRIRAMFIN.NS","POONAWALLA.NS","CANFINHOME.NS",
    "LICHSGFIN.NS","IIFL.NS",
    # IT & Tech
    "PERSISTENT.NS","COFORGE.NS","MPHASIS.NS","LTTS.NS","KPITTECH.NS",
    "TATAELXSI.NS","CYIENT.NS","SONACOMS.NS","TATATECH.NS","ZENSARTECH.NS",
    "HEXAWARE.NS","NIITTECH.NS","OFSS.NS","HAPPSTMNDS.NS","NEWGEN.NS",
    "MASTEK.NS","BIRLASOFT.NS",
    # Pharma
    "ALKEM.NS","LUPIN.NS","AUROPHARMA.NS","IPCALAB.NS","GLENMARK.NS",
    "NATCOPHARM.NS","AJANTPHARM.NS","GRANULES.NS","LAURUSLABS.NS","ABBOTINDIA.NS",
    "PFIZER.NS","SANOFI.NS","GLAXO.NS","SYNGENE.NS","MAXHEALTH.NS",
    "FORTIS.NS","NH.NS","ASTERDM.NS",
    # Auto
    "ASHOKLEY.NS","ESCORTS.NS","BALKRISIND.NS","MRF.NS","APOLLOTYRE.NS",
    "CEATLTD.NS","JKTYRE.NS","EXIDEIND.NS","AMARAJABAT.NS","SUNDRMFAST.NS",
    "ENDURANCE.NS",
    # Metals
    "SAIL.NS","NMDC.NS","NATIONALUM.NS","HINDZINC.NS","APLAPOLLO.NS",
    "RATNAMANI.NS","WELCORP.NS","JSL.NS","MOIL.NS","GRAVITA.NS",
    # FMCG
    "EMAMILTD.NS","JYOTHYLAB.NS","BAJAJCON.NS","HONASA.NS","RADICO.NS",
    "UNITDSPR.NS","PATANJALI.NS","BIKAJI.NS","DEVYANI.NS","JUBLFOOD.NS",
    # Energy
    "HINDPETRO.NS","PETRONET.NS","IGL.NS","MGL.NS","GUJGASLTD.NS",
    "TATAPOWER.NS","ADANIPOWER.NS","JSWENERGY.NS",
    # Infra & Cement
    "ACC.NS","DALBHARAT.NS","JKCEMENT.NS","RAMCOCEM.NS","HEIDELBERG.NS",
    "BIRLACORPN.NS","GMRAIRPORT.NS","IRB.NS","KNRCON.NS","NCC.NS",
    "GPIL.NS","IRCON.NS","RVNL.NS","TITAGARH.NS","TEXRAIL.NS",
    # Chemicals
    "AARTIIND.NS","DEEPAKNTR.NS","NAVINFLUOR.NS","ATUL.NS","VINATIORGA.NS",
    "TATACHEM.NS","GNFC.NS","GSFC.NS","CHAMBLFERT.NS","COROMANDEL.NS",
    "PIIND.NS","SUMICHEM.NS",
    # Real Estate
    "OBEROIRLTY.NS","PRESTIGE.NS","BRIGADE.NS","SOBHA.NS","PHOENIXLTD.NS",
    "MAHLIFE.NS","SUNTECK.NS","KOLTEPATIL.NS",
    # Telecom
    "IDEA.NS","TATACOMM.NS","INDUSTOWER.NS","HFCL.NS","TEJASNET.NS",
    "ITI.NS","ZEEL.NS","SUNTV.NS","PVRINOX.NS",
    # Insurance
    "MAXFIN.NS","STARHEALTH.NS","NIACL.NS",
    # PSU & Defence
    "BEL.NS","HAL.NS","BHEL.NS","BEML.NS","MDL.NS",
    "COCHINSHIP.NS","GRSE.NS","MAZDOCK.NS","BDL.NS","DATAPATTNS.NS",
    "PARAS.NS","MIDHANI.NS","SOLARINDS.NS","ASTRAL.NS","APARINDS.NS",
    # Midcap Stars
    "IRCTC.NS","IRFC.NS","HUDCO.NS","CGPOWER.NS","THERMAX.NS",
    "BLUESTARCO.NS","CROMPTON.NS",
]
NSE_STOCKS = list(dict.fromkeys(NSE_STOCKS))


# ============================================================
# CORE FUNCTIONS
# ============================================================
def check(ticker, p, near, min_above_pct, min_ema_rise, strict_stack):
    try:
        t = yf.Ticker(ticker)
        d = t.history(period="2y", auto_adjust=True)
        
        # ✅ Today's incomplete candle remove
        if len(d) > 1:
            d = d.iloc[:-1]
        
        # Minimum 1 year data
        if d.empty or len(d) < 250:
            return None
        
        # EMAs
        d['E200'] = d['Close'].ewm(span=p, adjust=False).mean()
        d['E50'] = d['Close'].ewm(span=50, adjust=False).mean()
        d['E20'] = d['Close'].ewm(span=20, adjust=False).mean()
        
        L = d.iloc[-1]
        c = float(L['Close'])
        e200 = float(L['E200'])
        e50 = float(L['E50'])
        e20 = float(L['E20'])
        
        dist = ((c - e200) / e200) * 100
        is_stack = (e20 > e50) and (e50 > e200)
        chg5 = ((c - float(d['Close'].iloc[-6])) / float(d['Close'].iloc[-6])) * 100 if len(d) >= 6 else 0
        
        # ============================================================
        # 1-YEAR QUALITY CHECKS
        # ============================================================
        last_1y = d.tail(250)
        
        # Kitne % din price 200 EMA ke upar thi?
        above_pct = (last_1y['Close'] > last_1y['E200']).mean() * 100
        
        # 200 EMA 1 saal me kitna badhi?
        ema_start = float(last_1y['E200'].iloc[0])
        ema_now = float(last_1y['E200'].iloc[-1])
        ema_rise_pct = ((ema_now - ema_start) / ema_start) * 100
        
        # ============================================================
        # FILTERS
        # ============================================================
        quality_uptrend = above_pct >= min_above_pct
        ema_growing = ema_rise_pct >= min_ema_rise
        
        # Base conditions
        base_pass = (
            c > e200 and              # Price above 200 EMA
            c > e50 and               # Price above 50 EMA
            abs(dist) <= near and     # Near 200 EMA
            quality_uptrend and       # 1Y quality
            ema_growing               # EMA rising
        )
        
        # Stack condition (optional)
        if strict_stack:
            base_pass = base_pass and is_stack
        
        if base_pass:
            return {
                "Ticker": ticker.replace(".NS",""),
                "Price": round(c, 2),
                "200_EMA": round(e200, 2),
                "50_EMA": round(e50, 2),
                "20_EMA": round(e20, 2),
                "Distance_%": round(dist, 2),
                "Above_200_1Y_%": round(above_pct, 1),
                "EMA_1Y_Rise_%": round(ema_rise_pct, 2),
                "Bullish_Stack": "✅" if is_stack else "❌",
                "5D_Change_%": round(chg5, 2),
                "Volume": int(L['Volume']),
            }
        return None
    except Exception:
        return None


# ============================================================
# MAIN UI
# ============================================================
st.sidebar.markdown("---")
st.sidebar.markdown(f"**📋 Total stocks:** {len(NSE_STOCKS)}")

run_btn = st.sidebar.button(
    "🚀 Run Screener", type="primary", use_container_width=True
)

if run_btn:
    st.info(f"🔍 Scanning {len(NSE_STOCKS)} stocks with strict filters... Please wait.")
    
    prog = st.progress(0)
    status = st.empty()
    results = []
    total = len(NSE_STOCKS)
    
    for i, tk in enumerate(NSE_STOCKS, 1):
        status.text(f"[{i}/{total}] Scanning {tk}...")
        r = check(tk, ema_period, near_ema_pct, min_above_pct, min_ema_rise, strict_stack)
        if r:
            results.append(r)
        prog.progress(i / total)
        time.sleep(batch_delay)
    
    status.empty()
    prog.empty()
    
    if not results:
        st.warning("❌ Koi stock match nahi hua. Filters thode relax karein.")
        st.markdown("""
        **Try karein:**
        - `Min % days above 200 EMA` ko **90** ya **85** karein
        - `Min EMA rise %` ko **3** karein
        - `200 EMA ke aaspaas % range` ko **8-10** karein
        """)
    else:
        df = pd.DataFrame(results)
        df = df.sort_values("Above_200_1Y_%", ascending=False).reset_index(drop=True)
        
        st.success(f"✅ Total **{len(df)}** quality stocks mile!")
        
        # ============================
        # METRICS
        # ============================
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("📊 Total Stocks", len(df))
        col2.metric("🎯 Avg Above 200 EMA", f"{df['Above_200_1Y_%'].mean():.1f}%")
        col3.metric("📈 Avg EMA 1Y Rise", f"{df['EMA_1Y_Rise_%'].mean():.1f}%")
        col4.metric("🔥 Strong Stacks", (df['Bullish_Stack'] == '✅').sum())
        
        # ============================
        # FULL RESULTS
        # ============================
        st.subheader("📊 All Results (Sorted by Quality)")
        st.dataframe(df, use_container_width=True, height=400)
        
        # ============================
        # TOP 10
        # ============================
        st.subheader("🎯 Top 10 Closest to 200 EMA (Best Entry)")
        top10 = df.copy()
        top10['abs_dist'] = top10['Distance_%'].abs()
        top10 = top10.nsmallest(10, 'abs_dist').drop(columns='abs_dist')
        st.dataframe(
            top10[["Ticker","Price","200_EMA","Distance_%","Above_200_1Y_%","EMA_1Y_Rise_%","Bullish_Stack"]],
            use_container_width=True
        )
        
        # ============================
        # SUPER STRONG (90%+ & 20%+ EMA rise)
        # ============================
        super_strong = df[(df["Above_200_1Y_%"] >= 90) & (df["EMA_1Y_Rise_%"] >= 20)]
        if not super_strong.empty:
            st.subheader(f"🔥 Elite Setups ({len(super_strong)} stocks)")
            st.caption("Above 200 EMA 90%+ days AND EMA rise 20%+ in 1 year")
            st.dataframe(
                super_strong[["Ticker","Price","200_EMA","Distance_%","Above_200_1Y_%","EMA_1Y_Rise_%"]],
                use_container_width=True
            )
        
        # ============================
        # DOWNLOAD
        # ============================
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            "💾 Download CSV",
            csv,
            f"screener_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
            "text/csv",
            use_container_width=True
        )
    
    st.caption(f"⏱️ Scan completed at {datetime.now().strftime('%d %b %Y, %I:%M %p')}")
    st.warning("⚠️ Ye tool sirf analysis ke liye hai. Investment advice nahi.")

else:
    st.info("👈 Sidebar me settings choose karein aur **🚀 Run Screener** dabayein.")
    
    with st.expander("📖 Settings Ka Matlab"):
        st.markdown("""
        | Setting | Default | Kya Karta Hai |
        |---------|---------|---------------|
        | **200 EMA ke aaspaas % range** | 5% | Stock 200 EMA ke kitne % andar ho |
        | **Min % days above 200 EMA** | 95% | Pichhle 1 saal me kitne % din price 200 EMA ke upar thi |
        | **Min 200 EMA rise %** | 5% | 200 EMA pichhle 1 saal me kitna % badhi |
        | **Bullish EMA Stack** | ✅ On | 20>50>200 EMA mandatory |
        
        **Recommended Values:**
        - 🟢 **Loose** (30+ stocks): 85%, 3%, ±10%
        - 🟡 **Balanced** (10-20 stocks): 92%, 5%, ±5%
        - 🔴 **Strict** (3-10 stocks): 97%, 10%, ±3%
        """)
