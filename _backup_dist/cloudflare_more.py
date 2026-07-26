#!/usr/bin/env python3
"""Get more historical data for Cloudflare."""
import yfinance as yf
import json

ticker = yf.Ticker("NET")

# Try getting historical annual data differently
inc = ticker.financials
print("=== Financials (Annual) ===")
if inc is not None and not inc.empty:
    if 'Total Revenue' in inc.index:
        revs = inc.loc['Total Revenue']
        for i, (idx, val) in enumerate(revs.items()):
            print(f"  {idx.date() if hasattr(idx, 'date') else idx}: ${val:,.0f}")

# Net income too
    if 'Net Income' in inc.index:
        ni = inc.loc['Net Income']
        print("\n=== Net Income ===")
        for i, (idx, val) in enumerate(ni.items()):
            print(f"  {idx.date() if hasattr(idx, 'date') else idx}: ${val:,.0f}")

# Debt detail
print("\n=== Balance Sheet ===")
bs = ticker.balance_sheet
if bs is not None and not bs.empty:
    for row_name in ['Total Debt', 'Long Term Debt', 'Short Long Term Debt', 'Cash And Cash Equivalents', 
                     'Cash', 'Total Assets', 'Stockholders Equity', 'Net Tangible Assets']:
        if row_name in bs.index:
            vals = bs.loc[row_name]
            for i, (idx, val) in enumerate(vals.items()):
                if i == 0:
                    print(f"  {row_name}: ${val:,.0f} (most recent)")
                    break

# Summary
print("\n=== KEY METRICS (TTM) FROM QUARTERLY DATA ===")
qinc = ticker.quarterly_income_stmt
if qinc is not None and not qinc.empty and 'Total Revenue' in qinc.index:
    qrevs = qinc.loc['Total Revenue']
    valid = [v for v in qrevs if v == v]
    if len(valid) >= 4:
        ttm_rev = sum(valid[:4])
        print(f"  Revenue TTM: ${ttm_rev:,.0f} (${ttm_rev/1e9:.2f}B)")

qcf = ticker.quarterly_cashflow
if qcf is not None and not qcf.empty:
    if 'Free Cash Flow' in qcf.index:
        fcfs = qcf.loc['Free Cash Flow']
        valid_fcf = [v for v in fcfs if v == v]
        if len(valid_fcf) >= 4:
            ttm_fcf = sum(valid_fcf[:4])
            print(f"  FCF TTM: ${ttm_fcf:,.0f} (${ttm_fcf/1e6:.1f}M)")
    elif 'Operating Cash Flow' in qcf.index:
        ocf = qcf.loc['Operating Cash Flow']
        valid_ocf = [v for v in ocf if v == v]
        if len(valid_ocf) >= 4:
            ttm_ocf = sum(valid_ocf[:4])
            print(f"  OCF TTM: ${ttm_ocf:,.0f}")
    if 'Capital Expenditure' in qcf.index:
        capex = qcf.loc['Capital Expenditure']
        valid_capex = [v for v in capex if v == v]
        if len(valid_capex) >= 4:
            ttm_capex = sum(valid_capex[:4])
            print(f"  Capex TTM: ${ttm_capex:,.0f}")
