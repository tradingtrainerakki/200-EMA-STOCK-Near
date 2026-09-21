"""
Stock Screener: Uptrend + 200 EMA ke aaspaas trade karne wale stocks
Author: Stock Screener App
Date: 2026
Universe: 200 NSE Stocks
"""

import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime
import time
import sys


# ============================================================
# CONFIGURATION
# ============================================================

# ============================================================
# 200 NSE STOCKS UNIVERSE
# ============================================================
NSE_STOCKS = [
    # ---------- NIFTY 50 (50 stocks) ----------
    "RELIANCE.NS", "TCS.NS", "HDFCBANK.NS", "INFY.NS", "ICICIBANK.NS",
    "HINDUNILVR.NS", "ITC.NS", "SBIN.NS", "BHARTIARTL.NS", "KOTAKBANK.NS",
    "LT.NS", "AXISBANK.NS", "ASIANPAINT.NS", "MARUTI.NS", "BAJFINANCE.NS",
    "HCLTECH.NS", "WIPRO.NS", "SUNPHARMA.NS", "TITAN.NS", "ULTRACEMCO.NS",
    "NESTLEIND.NS", "POWERGRID.NS", "NTPC.NS", "TATAMOTORS.NS", "TATASTEEL.NS",
    "M&M.NS", "ADANIENT.NS", "ADANIPORTS.NS", "JSWSTEEL.NS", "GRASIM.NS",
    "TECHM.NS", "INDUSINDBK.NS", "HINDALCO.NS", "BAJAJFINSV.NS", "DRREDDY.NS",
    "CIPLA.NS", "BRITANNIA.NS", "COALINDIA.NS", "DIVISLAB.NS", "EICHERMOT.NS",
    "HEROMOTOCO.NS", "APOLLOHOSP.NS", "BPCL.NS", "TATACONSUM.NS", "SBILIFE.NS",
    "HDFCLIFE.NS", "BAJAJ-AUTO.NS", "ONGC.NS", "UPL.NS", "LTIM.NS",

    # ---------- NIFTY NEXT 50 (50 stocks) ----------
    "DMART.NS", "PIDILITIND.NS", "GODREJCP.NS", "DABUR.NS", "MARICO.NS",
    "SIEMENS.NS", "HAVELLS.NS", "VOLTAS.NS", "CUMMINSIND.NS", "ABB.NS",
    "TRENT.NS", "ZOMATO.NS", "PAYTM.NS", "NYKAA.NS", "POLICYBZR.NS",
    "AMBUJACEM.NS", "BANKBARODA.NS", "BERGEPAINT.NS", "BIOCON.NS", "BOSCHLTD.NS",
    "CANBK.NS", "CHOLAFIN.NS", "COLPAL.NS", "DLF.NS", "GAIL.NS",
    "GODREJPROP.NS", "HAVELLS.NS", "ICICIGI.NS", "ICICIPRULI.NS", "IOC.NS",
    "INDHOTEL.NS", "INDIGO.NS", "JINDALSTEL.NS", "JIOFIN.NS", "LICI.NS",
    "LODHA.NS", "LTF.NS", "MOTHERSON.NS", "NAUKRI.NS", "PFC.NS",
    "RECLTD.NS", "SHREECEM.NS", "SRF.NS", "TVSMOTOR.NS", "TORNTPHARM.NS",
    "VBL.NS", "VEDL.NS", "ZYDUSLIFE.NS", "MUTHOOTFIN.NS", "PGHH.NS",

    # ---------- Banking & Finance (25 stocks) ----------
    "FEDERALBNK.NS", "IDFCFIRSTB.NS", "BANDHANBNK.NS", "RBLBANK.NS", "AUBANK.NS",
    "YESBANK.NS", "PNB.NS", "UNIONBANK.NS", "INDIANB.NS", "CENTRALBK.NS",
    "BAJAJHLDNG.NS", "MUTHOOTFIN.NS", "MANAPPURAM.NS", "CHOLAFIN.NS", "SBICARD.NS",
    "HDFCAMC.NS", "NIPPONAMC.NS", "UTIAMC.NS", "ABCAPITAL.NS", "PEL.NS",
    "SHRIRAMFIN.NS", "POONAWALLA.NS", "CANFINHOME.NS", "LICHSGFIN.NS", "IIFL.NS",

    # ---------- IT & Tech (20 stocks) ----------
    "PERSISTENT.NS", "COFORGE.NS", "MPHASIS.NS", "LTTS.NS", "KPITTECH.NS",
    "TATAELXSI.NS", "CYIENT.NS", "SONACOMS.NS", "TATATECH.NS", "ZENSARTECH.NS",
    "HEXAWARE.NS", "NIITTECH.NS", "OFSS.NS", "INFY.NS", "TECHM.NS",
    "HAPPSTMNDS.NS", "NEWGEN.NS", "MASTEK.NS", "SASKEN.NS", "BIRLASOFT.NS",

    # ---------- Pharma & Healthcare (20 stocks) ----------
    "ALKEM.NS", "LUPIN.NS", "AUROPHARMA.NS", "TORNTPHARM.NS", "IPCALAB.NS",
    "GLENMARK.NS", "NATCOPHARM.NS", "AJANTPHARM.NS", "GRANULES.NS", "LAURUSLABS.NS",
    "ABBOTINDIA.NS", "PFIZER.NS", "SANOFI.NS", "GLAXO.NS", "SYNGENE.NS",
    "MAXHEALTH.NS", "FORTIS.NS", "NH.NS", "APOLLOHOSP.NS", "ASTERDM.NS",

    # ---------- Auto & Ancillaries (20 stocks) ----------
    "BAJAJ-AUTO.NS", "HEROMOTOCO.NS", "TVSMOTOR.NS", "EICHERMOT.NS", "M&M.NS",
    "MARUTI.NS", "TATAMOTORS.NS", "ASHOKLEY.NS", "ESCORTS.NS", "BALKRISIND.NS",
    "MRF.NS", "APOLLOTYRE.NS", "CEATLTD.NS", "JKTYRE.NS", "MOTHERSON.NS",
    "BOSCHLTD.NS", "EXIDEIND.NS", "AMARAJABAT.NS", "SUNDRMFAST.NS", "ENDURANCE.NS",

    # ---------- Metals & Mining (15 stocks) ----------
    "TATASTEEL.NS", "JSWSTEEL.NS", "HINDALCO.NS", "VEDL.NS", "JINDALSTEL.NS",
    "SAIL.NS", "NMDC.NS", "NATIONALUM.NS", "HINDZINC.NS", "APLAPOLLO.NS",
    "RATNAMANI.NS", "WELCORP.NS", "JSL.NS", "MOIL.NS", "GRAVITA.NS",

    # ---------- FMCG & Consumer (20 stocks) ----------
    "HINDUNILVR.NS", "ITC.NS", "NESTLEIND.NS", "BRITANNIA.NS", "DABUR.NS",
    "MARICO.NS", "GODREJCP.NS", "COLPAL.NS", "EMAMILTD.NS", "JYOTHYLAB.NS",
    "BAJAJCON.NS", "HONASA.NS", "RADICO.NS", "UNITDSPR.NS", "VBL.NS",
    "TATACONSUM.NS", "PATANJALI.NS", "BIKAJI.NS", "DEVYANI.NS", "JUBLFOOD.NS",

    # ---------- Energy & Power (15 stocks) ----------
    "RELIANCE.NS", "ONGC.NS", "IOC.NS", "BPCL.NS", "HINDPETRO.NS",
    "GAIL.NS", "PETRONET.NS", "IGL.NS", "MGL.NS", "GUJGASLTD.NS",
    "NTPC.NS", "POWERGRID.NS", "TATAPOWER.NS", "ADANIPOWER.NS", "JSWENERGY.NS",

    # ---------- Infrastructure & Cement (20 stocks) ----------
    "LT.NS", "ULTRACEMCO.NS", "SHREECEM.NS", "AMBUJACEM.NS", "ACC.NS",
    "DALBHARAT.NS", "JKCEMENT.NS", "RAMCOCEM.NS", "HEIDELBERG.NS", "BIRLACORPN.NS",
    "ADANIPORTS.NS", "GMRAIRPORT.NS", "IRB.NS", "KNRCON.NS", "NCC.NS",
    "GPIL.NS", "IRCON.NS", "RVNL.NS", "TITAGARH.NS", "TEXRAIL.NS",

    # ---------- Chemicals & Specialty (15 stocks) ----------
    "PIDILITIND.NS", "SRF.NS", "AARTIIND.NS", "DEEPAKNTR.NS", "NAVINFLUOR.NS",
    "ATUL.NS", "VINATIORGA.NS", "TATACHEM.NS", "GNFC.NS", "GSFC.NS",
    "CHAMBLFERT.NS", "COROMANDEL.NS", "PIIND.NS", "UPL.NS", "SUMICHEM.NS",

    # ---------- Real Estate (10 stocks) ----------
    "DLF.NS", "GODREJPROP.NS", "OBEROIRLTY.NS", "PRESTIGE.NS", "BRIGADE.NS",
    "SOBHA.NS", "PHOENIXLTD.NS", "MAHLIFE.NS", "SUNTECK.NS", "KOLTEPATIL.NS",

    # ---------- Telecom & Media (10 stocks) ----------
    "BHARTIARTL.NS", "IDEA.NS", "TATACOMM.NS", "INDUSTOWER.NS", "HFCL.NS",
    "TEJASNET.NS", "ITI.NS", "ZEEL.NS", "SUNTV.NS", "PVRINOX.NS",

    # ---------- Insurance (8 stocks) ----------
    "SBILIFE.NS", "HDFCLIFE.NS", "ICICIPRULI.NS", "ICICIGI.NS", "LICI.NS",
    "MAXFIN.NS", "STARHEALTH.NS", "NIACL.NS",

    # ---------- PSU & Defence (15 stocks) ----------
    "BEL.NS", "HAL.NS", "BHEL.NS", "BEML.NS", "MDL.NS",
    "COCHINSHIP.NS", "GRSE.NS", "MAZDOCK.NS", "BDL.NS", "DATAPATTNS.NS",
    "PARAS.NS", "MIDHANI.NS", "SOLARINDS.NS", "ASTRAL.NS", "APARINDS.NS",

    # ---------- Midcap & Smallcap Stars (20 stocks) ----------
    "TRENT.NS", "DMART.NS", "ZOMATO.NS", "NYKAA.NS", "PAYTM.NS",
    "POLICYBZR.NS", "IRCTC.NS", "IRFC.NS", "HUDCO.NS", "RVNL.NS",
    "TITAGARH.NS", "CGPOWER.NS", "THERMAX.NS", "CUMMINSIND.NS", "ABB.NS",
    "SIEMENS.NS", "HAVELLS.NS", "VOLTAS.NS", "BLUESTARCO.NS", "CROMPTON.NS",
]

# Duplicates remove karein (safe rehne ke liye)
NSE_STOCKS = list(dict.fromkeys(NSE_STOCKS))

# Screening parameters
EMA_PERIOD = 200              # EMA period
NEAR_EMA_PERCENT = 5.0        # 200 EMA ke kitne % ke andar (5% = ±5%)
MIN_UPTREND_DAYS = 20         # Kitne din se uptrend me ho
LOOKBACK_PERIOD = "1y"        # Kitna data fetch karna hai
BATCH_DELAY = 0.5             # Rate limiting ke liye delay (seconds)
BATCH_SIZE = 50               # Kitne stocks ek batch me process karein
BATCH_PAUSE = 5               # Batch ke beech pause (seconds)


# ============================================================
# CORE FUNCTIONS
# ============================================================

def calculate_indicators(data: pd.DataFrame) -> pd.DataFrame:
    """200 EMA, 50 EMA aur 20 EMA calculate karta hai."""
    data = data.copy()
    data['EMA_200'] = data['Close'].ewm(span=EMA_PERIOD, adjust=False).mean()
    data['EMA_50'] = data['Close'].ewm(span=50, adjust=False).mean()
    data['EMA_20'] = data['Close'].ewm(span=20, adjust=False).mean()
    return data


def check_uptrend_and_near_ema(ticker: str) -> dict | None:
    """
    Ek stock ko check karta hai:
    - Kya uptrend me hai? (price > 200 EMA)
    - Kya 200 EMA ke aaspaas hai? (within NEAR_EMA_PERCENT)
    - Kya EMA stack bullish hai? (20 > 50 > 200)
    """
    try:
        stock = yf.Ticker(ticker)
        data = stock.history(period=LOOKBACK_PERIOD, auto_adjust=True)

        if data.empty or len(data) < EMA_PERIOD + 10:
            return None

        data = calculate_indicators(data)

        latest = data.iloc[-1]

        latest_close = float(latest['Close'])
        ema_200 = float(latest['EMA_200'])
        ema_50 = float(latest['EMA_50'])
        ema_20 = float(latest['EMA_20'])

        # Distance from 200 EMA in percentage
        distance_pct = ((latest_close - ema_200) / ema_200) * 100

        # ---- Condition 1: Uptrend (price above 200 EMA) ----
        is_uptrend = latest_close > ema_200

        # ---- Condition 2: Near 200 EMA (within ±NEAR_EMA_PERCENT) ----
        is_near_ema = abs(distance_pct) <= NEAR_EMA_PERCENT

        # ---- Condition 3: Bullish EMA stack ----
        is_bullish_stack = (ema_20 > ema_50) and (ema_50 > ema_200)

        # ---- Condition 4: 200 EMA itself rising (uptrend confirmation) ----
        ema_200_20days_ago = float(data['EMA_200'].iloc[-20]) if len(data) >= 20 else ema_200
        is_ema_rising = ema_200 > ema_200_20days_ago

        # ---- Condition 5: Recent momentum (last 5 days change) ----
        if len(data) >= 6:
            last_5d_change = ((latest_close - float(data['Close'].iloc[-6])) / float(data['Close'].iloc[-6])) * 100
        else:
            last_5d_change = 0.0

        if is_uptrend and is_near_ema:
            return {
                "Ticker": ticker.replace(".NS", ""),
                "Price": round(latest_close, 2),
                "200_EMA": round(ema_200, 2),
                "50_EMA": round(ema_50, 2),
                "20_EMA": round(ema_20, 2),
                "Distance_%": round(distance_pct, 2),
                "Bullish_Stack": "✅" if is_bullish_stack else "❌",
                "EMA_Rising": "✅" if is_ema_rising else "❌",
                "5D_Change_%": round(last_5d_change, 2),
                "Volume": int(latest['Volume']),
            }

        return None

    except Exception as e:
        print(f"  ⚠️  Error {ticker}: {e}", file=sys.stderr)
        return None


def run_screener(tickers: list[str]) -> pd.DataFrame:
    """Saare stocks ko batch me scan karta hai aur matching stocks return karta hai."""
    results = []
    total = len(tickers)

    print(f"\n🔍 Scanning {total} stocks in batches of {BATCH_SIZE}...")
    print(f"   Criteria: Uptrend + within ±{NEAR_EMA_PERCENT}% of 200 EMA\n")

    for i, ticker in enumerate(tickers, 1):
        print(f"[{i}/{total}] Checking {ticker}...", end=" ", flush=True)
        result = check_uptrend_and_near_ema(ticker)

        if result:
            results.append(result)
            print(f"✅ MATCH (Dist: {result['Distance_%']}%)")
        else:
            print("—")

        # Batch pause for rate limiting
        if i % BATCH_SIZE == 0 and i < total:
            print(f"\n⏸️  Batch complete. Pausing {BATCH_PAUSE}s to avoid rate limits...\n")
            time.sleep(BATCH_PAUSE)
        else:
            time.sleep(BATCH_DELAY)

    if not results:
        return pd.DataFrame()

    df = pd.DataFrame(results)
    df = df.sort_values("Distance_%", key=lambda x: abs(x)).reset_index(drop=True)
    return df


def print_report(df: pd.DataFrame):
    """Sundar formatted report print karta hai."""
    print("\n" + "=" * 100)
    print(f"📊 STOCK SCREENER REPORT — {datetime.now().strftime('%d %b %Y, %I:%M %p')}")
    print("=" * 100)

    if df.empty:
        print("\n❌ Koi stock match nahi hua current criteria ke saath.")
        print("   Try karein: NEAR_EMA_PERCENT badha kar dekhein (e.g., 10.0)\n")
        return

    print(f"\n✅ Total {len(df)} stocks mile jo Uptrend me hain aur 200 EMA ke aaspaas hain:\n")
    print(df.to_string(index=False))

    print("\n" + "-" * 100)
    print("💡 Legend:")
    print("   • Distance_% : Price aur 200 EMA ke beech ka % difference (0 ke kareeb = bilkul paas)")
    print("   • Bullish_Stack : 20 EMA > 50 EMA > 200 EMA (strong uptrend)")
    print("   • EMA_Rising : 200 EMA khud upar ja raha hai")
    print("   • 5D_Change_% : Pichle 5 din me kitna % move hua")
    print("-" * 100)
    print("\n⚠️  DISCLAIMER: Ye sirf technical analysis tool hai, investment advice nahi.")
    print("   Koi bhi trade lene se pehle apne financial advisor se consult karein.\n")


def export_to_csv(df: pd.DataFrame, filename: str = "screener_results.csv"):
    """Results ko CSV me save karta hai."""
    if df.empty:
        print("⚠️  Koi data nahi hai export karne ke liye.")
        return
    df.to_csv(filename, index=False)
    print(f"💾 Results saved to: {filename}")


# ============================================================
# MAIN
# ============================================================

def main():
    print("=" * 100)
    print("🚀 NSE STOCK SCREENER — Uptrend + 200 EMA Proximity")
    print(f"📋 Universe: {len(NSE_STOCKS)} NSE stocks")
    print("=" * 100)

    # Estimate time
    est_seconds = len(NSE_STOCKS) * (BATCH_DELAY + 1) + (len(NSE_STOCKS) // BATCH_SIZE) * BATCH_PAUSE
    est_minutes = est_seconds / 60
    print(f"⏱️  Estimated time: ~{est_minutes:.1f} minutes\n")

    start_time = time.time()
    df = run_screener(NSE_STOCKS)
    elapsed = (time.time() - start_time) / 60

    print_report(df)
    print(f"⏱️  Total scan time: {elapsed:.1f} minutes")

    if not df.empty:
        export_to_csv(df)

        # Top picks highlight
        print("\n🎯 TOP 10 CLOSEST TO 200 EMA (Best entry opportunities):\n")
        top10 = df.head(10)[["Ticker", "Price", "200_EMA", "Distance_%", "Bullish_Stack", "EMA_Rising"]]
        print(top10.to_string(index=False))

        # Strong bullish setups filter
        strong = df[(df["Bullish_Stack"] == "✅") & (df["EMA_Rising"] == "✅")]
        if not strong.empty:
            print(f"\n🔥 STRONG BULLISH SETUPS (Bullish Stack + Rising 200 EMA): {len(strong)} stocks\n")
            print(strong[["Ticker", "Price", "200_EMA", "Distance_%", "5D_Change_%"]].to_string(index=False))
        print()


if __name__ == "__main__":
    main()
