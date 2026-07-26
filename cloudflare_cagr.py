#!/usr/bin/env python3
"""Get Cloudflare 5-year revenue data for CAGR calculation."""
import yfinance as yf
import json

ticker = yf.Ticker("NET")

# Get annual income statement
inc = ticker.income_stmt
print("=== Revenue Data (Annual) ===")
if inc is not None and not inc.empty:
    if 'Total Revenue' in inc.index:
        revs = inc.loc['Total Revenue']
        for i, (idx, val) in enumerate(revs.items()):
            print(f"  {idx.date() if hasattr(idx, 'date') else idx}: ${val:,.0f}")
        
        # Filter out NaN and get annual data points
        valid_revs = [(idx, val) for idx, val in revs.items() if val == val]
        print(f"\n  Valid data points: {len(valid_revs)}")
        
        if len(valid_revs) >= 6:
            # Most recent full year vs year 6 years ago
            newest = valid_revs[0][1]
            oldest_5y = valid_revs[5][1] if len(valid_revs) > 5 else valid_revs[-1][1]
            newest_date = valid_revs[0][0]
            oldest_date = valid_revs[5][0] if len(valid_revs) > 5 else valid_revs[-1][0]
            years_diff = 5  # approximate
            if oldest_5y > 0:
                cagr = (newest / oldest_5y) ** (1/years_diff) - 1
                print(f"\n  Newest ({newest_date.date()}): ${newest:,.0f}")
                print(f"  5yr ago ({oldest_date.date()}): ${oldest_5y:,.0f}")
                print(f"  5-year CAGR: {cagr*100:.2f}%")
            else:
                print("  Can't compute CAGR (oldest revenue <= 0)")
        elif len(valid_revs) >= 2:
            newest = valid_revs[0][1]
            oldest = valid_revs[-1][1]
            if oldest > 0:
                years = len(valid_revs) - 1
                cagr = (newest / oldest) ** (1/years) - 1
                print(f"\n  Newest: ${newest:,.0f}")
                print(f"  Oldest (over {years} years): ${oldest:,.0f}")
                print(f"  CAGR over {years} years: {cagr*100:.2f}%")
    else:
        print("  No 'Total Revenue' in index")
        print(f"  Available indices: {list(inc.index)}")
else:
    print("  No income statement data")

# Also check quarterly revenue for TTM comp
print("\n=== Quarterly Revenue (last 8 quarters) ===")
try:
    qinc = ticker.quarterly_income_stmt
    if qinc is not None and not qinc.empty:
        if 'Total Revenue' in qinc.index:
            qrevs = qinc.loc['Total Revenue']
            for i, (idx, val) in enumerate(qrevs.items()):
                if i < 8:
                    print(f"  {idx.date() if hasattr(idx, 'date') else idx}: ${val:,.0f}")
            
            valid_qrevs = [val for val in qrevs if val == val]
            if len(valid_qrevs) >= 4:
                ttm = sum(valid_qrevs[:4])
                print(f"\n  TTM Revenue (last 4 quarters): ${ttm:,.0f}")
except Exception as e:
    print(f"  Quarterly error: {e}")

# Free Cash Flow
print("\n=== Free Cash Flow (Annual) ===")
try:
    cf = ticker.cashflow
    if cf is not None and not cf.empty:
        if 'Free Cash Flow' in cf.index:
            fcfs = cf.loc['Free Cash Flow']
            for i, (idx, val) in enumerate(fcfs.items()):
                print(f"  {idx.date() if hasattr(idx, 'date') else idx}: ${val:,.0f}")
except Exception as e:
    print(f"  FCF error: {e}")
