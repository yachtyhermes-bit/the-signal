#!/usr/bin/env python3
"""Verify SMCI forward PE claim and other edge cases."""
import yfinance as yf, json

t = yf.Ticker('SMCI')
info = t.info

print("=== SMCI Forward PE ===")
print(f"  forwardPE: {info.get('forwardPE')}")
print(f"  trailingPE: {info.get('trailingPE')}")
print(f"  currentPrice: {info.get('currentPrice')}")
print(f"  article price: $25.89")

# Check earnings estimate
try:
    est = t.earnings_estimate
    print(f"\n  Earnings estimates:")
    print(f"  {est}")
except Exception as e:
    print(f"  No earnings estimate: {e}")

# Current FY estimate
try:
    print(f"\n  Earnings estimate columns: {est.columns.tolist() if est is not None else 'none'}")
    if est is not None:
        print(f"  Index: {est.index.tolist()}")
except:
    pass

# Short float
print(f"\n  shortPercentOfFloat: {info.get('shortPercentOfFloat')}")
print(f"  shortRatio: {info.get('shortRatio')}")

# PANW quarterly revenue
print(f"\n=== PANW Quarterly Revenue ===")
t2 = yf.Ticker('PANW')
q_inc = t2.quarterly_income_stmt
if q_inc is not None and 'Total Revenue' in q_inc.index:
    print(f"  Quarterly revenue (last 4):")
    for i, (idx, val) in enumerate(q_inc.loc['Total Revenue'].dropna().head(4).items()):
        q_date = idx.strftime('%b %Y') if hasattr(idx, 'strftime') else str(idx)
        print(f"    {q_date}: ${val/1e9:.2f}B")

# PANW net income quarterly
if q_inc is not None and 'Net Income' in q_inc.index:
    print(f"  Quarterly net income:")
    for i, (idx, val) in enumerate(q_inc.loc['Net Income'].dropna().head(4).items()):
        q_date = idx.strftime('%b %Y') if hasattr(idx, 'strftime') else str(idx)
        print(f"    {q_date}: ${val/1e9:.2f}B")

# Check PANW article content more carefully
with open('/home/chino/thesignal/articles/posts/panw-ai-security-cash-flow-machine-2026.json') as f:
    pa = json.load(f)
body = pa['bodyHtml']
import re
body_clean = re.sub(r'<[^>]+>', ' ', body)
print(f"\n=== PANW Article - margin/FCF claims ===")
for s in body_clean.split('.'):
    if 'margin' in s.lower() or 'revenue' in s.lower() or 'FCF' in s or 'cash flow' in s.lower():
        s = s.strip()
        if s:
            print(f"  {s[:150]}")
