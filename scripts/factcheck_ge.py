#!/usr/bin/env python3
"""Verify GE FCF claims."""
import yfinance as yf

t = yf.Ticker("GE")
cf = t.cashflow
if cf is not None and not cf.empty:
    print("Annual Cash Flow:")
    for row_name in ['Capital Expenditure', 'Free Cash Flow', 'Operating Cash Flow']:
        if row_name in cf.index:
            for col in cf.columns[:4]:
                v = cf.loc[row_name, col]
                yr = col.strftime("%Y") if hasattr(col, 'strftime') else str(col)
                print(f"  {row_name} {yr}: ${float(v)/1e9:.2f}B")

q_cf = t.quarterly_cashflow
if q_cf is not None and not q_cf.empty:
    print("\nQuarterly FCF (last 4):")
    if 'Free Cash Flow' in q_cf.index:
        vals = q_cf.loc['Free Cash Flow'].iloc[:4]
        for idx, v in vals.items():
            yr = idx.strftime("%Y-%m") if hasattr(idx, 'strftime') else str(idx)
            print(f"  {yr}: ${float(v)/1e9:.2f}B")
        print(f"  TTM: ${float(vals.sum())/1e9:.2f}B")
