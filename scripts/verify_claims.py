#!/usr/bin/env python3
"""Verify specific claims more carefully."""

import yfinance as yf
import json

# 1. KTOS YTD check
t = yf.Ticker('KTOS')
hist = t.history(period='6mo')
# Find first trading day of 2026
jan_data = hist[hist.index.year == 2026]
if len(jan_data) > 0:
    jan2_close = jan_data.iloc[0]['Close']
    current = t.info.get('currentPrice') or hist.iloc[-1]['Close']
    ytd_drop = (jan2_close - current) / jan2_close * 100
    print(f"KTOS: Jan 2 close = ${jan2_close:.2f}, Current = ${current:.2f}, YTD drop = {ytd_drop:.1f}%")
    # Article says "from $79 to $50" 
    # Check if $79 was the Jan 2 price
    print(f"  Article says from $79 -> $50 (36% drop)")
    print(f"  Jan 2 actual price: ${jan2_close:.2f}")
    
print()

# 2. COIN Q1 revenue check
t2 = yf.Ticker('COIN')
q_inc = t2.quarterly_income_stmt
if q_inc is not None and 'Total Revenue' in q_inc.index:
    print(f"COIN quarterly revenue: {q_inc.loc['Total Revenue'].to_dict()}")
    
print()

# 3. CRWV annual revenue check  
t3 = yf.Ticker('CRWV')
inc = t3.income_stmt
if inc is not None and 'Total Revenue' in inc.index:
    print(f"CRWV annual revenue:")
    for col in inc.columns:
        try:
            rev = inc.loc['Total Revenue', col]
            print(f"  {col.strftime('%Y-%m-%d') if hasattr(col, 'strftime') else col}: ${rev/1e9:.2f}B")
        except:
            pass

print()

# 4. SMCI revenue check
t4 = yf.Ticker('SMCI')
inc4 = t4.income_stmt
if inc4 is not None and 'Total Revenue' in inc4.index:
    print(f"SMCI annual revenue:")
    for col in inc4.columns[:5]:
        try:
            rev = inc4.loc['Total Revenue', col]
            yr = col.strftime('%Y') if hasattr(col, 'strftime') else str(col)
            print(f"  {yr}: ${rev/1e9:.2f}B")
        except:
            pass

print()

# 5. AMAT ATH check
t5 = yf.Ticker('AMAT')
hist5 = t5.history(period='3mo')
# Check if ATH $739.67 was on June 30
june_data = hist5[(hist5.index.month == 6) & (hist5.index.year == 2026)]
if len(june_data) > 0:
    max_close = june_data['Close'].max()
    max_close_date = june_data['Close'].idxmax()
    print(f"AMAT June 2026 max close: ${max_close:.2f} on {max_close_date}")
    # Check ATH
    print(f"AMAT 52-week high from info: {t5.info.get('fiftyTwoWeekHigh')}")

# 6. NOW 52-week high
t6 = yf.Ticker('NOW')
print(f"\nNOW 52-week high: {t6.info.get('fiftyTwoWeekHigh')}")
print(f"NOW current price: {t6.info.get('currentPrice')}")

# 7. AXON financials
t7 = yf.Ticker('AXON')
inc7 = t7.income_stmt
if inc7 is not None and 'Total Revenue' in inc7.index:
    print(f"\nAXON annual revenue:")
    for col in inc7.columns[:4]:
        try:
            rev = inc7.loc['Total Revenue', col]
            yr = col.strftime('%Y') if hasattr(col, 'strftime') else str(col)
            print(f"  {yr}: ${rev/1e9:.2f}B")
        except:
            pass

# AXON backlog
print(f"AXON market cap: ${t7.info.get('marketCap', 0)/1e9:.2f}B")
