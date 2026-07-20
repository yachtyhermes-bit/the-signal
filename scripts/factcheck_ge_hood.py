#!/usr/bin/env python3
"""Verify GE FCF claims and check HOOD broken link."""
import yfinance as yf
import json

# ===== GE FCF =====
print("=== GE FCF Verification ===")
t = yf.Ticker("GE")

# Annual cash flow
cf = t.cashflow
if cf is not None and not cf.empty:
    print("\nAnnual Cash Flow:")
    for row_name in ['Capital Expenditure', 'Free Cash Flow', 'Operating Cash Flow']:
        if row_name in cf.index:
            print(f"\n{row_name}:")
            for col in cf.columns[:3]:
                v = cf.loc[row_name, col]
                yr = col.strftime("%Y") if hasattr(col, 'strftime') else str(col)
                print(f"  {yr}: ${float(v)/1e9:.2f}B")

# Quarterly cash flow
q_cf = t.quarterly_cashflow
if q_cf is not None and not q_cf.empty:
    print("\nQuarterly FCF (last 4 quarters):")
    if 'Free Cash Flow' in q_cf.index:
        vals = q_cf.loc['Free Cash Flow'].iloc[:4]
        for i, (idx, v) in enumerate(vals.items()):
            yr = idx.strftime("%Y-%m") if hasattr(idx, 'strftime') else str(i)
            print(f"  {yr}: ${float(v)/1e9:.2f}B")
        print(f"  TTM: ${float(vals.sum())/1e9:.2f}B")
    
    if 'Operating Cash Flow' in q_cf.index:
        vals = q_cf.loc['Operating Cash Flow'].iloc[:4]
        print(f"\nQuarterly OCF (TTM): ${float(vals.sum())/1e9:.2f}B")
    
    if 'Capital Expenditure' in q_cf.index:
        vals = q_cf.loc['Capital Expenditure'].iloc[:4]
        print(f"Quarterly Capex (TTM): ${float(vals.sum())/1e9:.2f}B")

# ===== HOOD broken link =====
print("\n\n=== HOOD Broken Link Check ===")
# The current broken link:
bad_url = "https://investors.robinhood.com/news-events/press-releases/detail/48/robinhood-reports-first-quarter-2026-results"
print(f"Bad URL: {bad_url}")

# Try common patterns - Q1 2026 results
import urllib.request
alternatives = [
    "https://investors.robinhood.com/news-events/press-releases/detail/52/robinhood-reports-first-quarter-2026-results",
    "https://investors.robinhood.com/news-events/press-releases/robinhood-reports-first-quarter-2026-results",
    "https://investors.robinhood.com/news/news-details/2026/Robinhood-Reports-First-Quarter-2026-Results/",
    "https://investors.robinhood.com/news-events/press-releases/",
]
for alt_url in alternatives:
    try:
        req = urllib.request.Request(alt_url, method='HEAD')
        with urllib.request.urlopen(req, timeout=10) as resp:
            print(f"  {resp.status} | {alt_url}")
    except urllib.error.HTTPError as e:
        print(f"  {e.code} | {alt_url}")
    except Exception as e:
        print(f"  error | {alt_url}: {e}")

# Check SHOP yPal context
print("\n\n=== SHOP 'yPal' check ===")
with open('articles/posts/shopify-ai-commerce-moat-ecosystem-2026.json') as f:
    shop = json.load(f)
body = shop['bodyHtml']
import re
for m in re.finditer(r'yPal', body):
    ctx = body[max(0, m.start()-30):m.end()+30]
    print(f"Context: ...{ctx}...")
