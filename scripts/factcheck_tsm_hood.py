#!/usr/bin/env python3
"""Check TSM capex and HOOD debt details."""
import yfinance as yf

print("=" * 50)
print("TSM CAPEX DETAILS")
print("=" * 50)

t = yf.Ticker("TSM")

# Annual cash flow
cf = t.cashflow
if cf is not None and not cf.empty:
    print("\n--- Annual Cash Flow ---")
    for row_name in ['Capital Expenditure', 'Operating Cash Flow', 'Free Cash Flow']:
        if row_name in cf.index:
            print(f"\n{row_name}:")
            for col in cf.columns[:4]:
                v = cf.loc[row_name, col]
                yr = col.strftime("%Y") if hasattr(col, 'strftime') else str(col)
                print(f"  {yr}: ${float(v)/1e9:.2f}B")

# Quarterly cash flow
q_cf = t.quarterly_cashflow
if q_cf is not None and not q_cf.empty:
    print("\n--- Quarterly Cash Flow (last 4 quarters) ---")
    for row_name in ['Capital Expenditure', 'Operating Cash Flow', 'Free Cash Flow']:
        if row_name in q_cf.index:
            vals = q_cf.loc[row_name].iloc[:4]
            print(f"\n{row_name}:")
            for i, (idx, v) in enumerate(vals.items()):
                yr = idx.strftime("%Y-%m") if hasattr(idx, 'strftime') else str(i)
                print(f"  {yr}: ${float(v)/1e9:.2f}B")
            print(f"  TTM: ${float(vals.sum())/1e9:.2f}B")

# Also check info capex
info = t.info
print(f"\nCapex from info: ${info.get('capitalExpenditures', 0)/1e9:.2f}B")
print(f"Total Revenue TTM: ${info.get('totalRevenue', 0)/1e9:.2f}B")

print("\n" + "=" * 50)
print("HOOD DEBT DETAILS")
print("=" * 50)

t2 = yf.Ticker("HOOD")
info2 = t2.info
print(f"Total Debt: ${info2.get('totalDebt', 0)/1e9:.2f}B")
print(f"Total Cash: ${info2.get('totalCash', 0)/1e9:.2f}B")
print(f"Net Cash: ${(info2.get('totalCash', 0) - info2.get('totalDebt', 0))/1e9:.2f}B")
print(f"Short Term Debt: ${info2.get('shortTermDebt', 0)/1e9:.2f}B")
print(f"Long Term Debt: ${info2.get('longTermDebt', 0)/1e9:.2f}B")

# Balance sheet
bs = t2.balance_sheet
if bs is not None and not bs.empty:
    print("\n--- Balance Sheet (most recent years) ---")
    for col in bs.columns[:3]:
        yr = col.strftime("%Y") if hasattr(col, 'strftime') else str(col)
        print(f"\n  --- {yr} ---")
        for row_name in ['Total Debt', 'Long Term Debt', 'Short Term Debt', 
                         'Cash And Cash Equivalents', 'Total Assets',
                         'Current Debt', 'Other Current Liabilities']:
            if row_name in bs.index:
                v = bs.loc[row_name, col]
                print(f"    {row_name}: ${float(v)/1e9:.2f}B")
