#!/usr/bin/env python3
"""Check SMCI run rate and more specific claims."""

import yfinance as yf

# SMCI TTM revenue check
t = yf.Ticker('SMCI')
q_inc = t.quarterly_income_stmt
if q_inc is not None and 'Total Revenue' in q_inc.index:
    # Get last 4 quarters
    q_revs = q_inc.loc['Total Revenue'].dropna().head(4)
    ttm_rev = q_revs.sum()
    print(f"SMCI last 4 quarters revenue: {q_revs.values}")
    print(f"SMCI TTM revenue: ${ttm_rev/1e9:.2f}B")
    
print()

# SMCI gross margins TTM
info = t.info
print(f"SMCI gross margins: {info.get('grossMargins')}")
print(f"SMCI trailing PE: {info.get('trailingPE')}")
print(f"SMCI forward PE: {info.get('forwardPE')}")

# Check AXON price
print()
t2 = yf.Ticker('AXON')
hist = t2.history(period='1mo')
print("AXON last 10 days:")
print(hist.tail(10)[['Close']].to_string())

# Verify AXON 52-week high
print(f"\nAXON 52-week high: {t2.info.get('fiftyTwoWeekHigh')}")
print(f"AXON market cap: ${t2.info.get('marketCap',0)/1e9:.2f}B")

# CRWV - check revenue growth rate
print()
t3 = yf.Ticker('CRWV')
q_inc3 = t3.quarterly_income_stmt
if q_inc3 is not None and 'Total Revenue' in q_inc3.index:
    q_revs3 = q_inc3.loc['Total Revenue'].dropna()
    print(f"CRWV quarterly revenues: {q_revs3.values}")
    # Check YoY growth
    if len(q_revs3) >= 4:
        current_q = q_revs3.iloc[0]
        year_ago_q = q_revs3.iloc[4] if len(q_revs3) >= 5 else None
        if year_ago_q and year_ago_q > 0:
            yoy = (current_q - year_ago_q) / year_ago_q * 100
            print(f"CRWV QoQ YoY growth: {yoy:.1f}%")
