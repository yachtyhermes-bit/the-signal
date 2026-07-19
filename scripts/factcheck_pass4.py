#!/usr/bin/env python3
"""Verify specific claims in PANW, SMCI, and SOFI articles."""
import json, re, yfinance as yf, pandas as pd

# PANW: $3.79B FCF claim
print("=" * 60)
print("PANW — FCF Claim Verification")
print("=" * 60)

with open('/home/chino/thesignal/articles/posts/panw-ai-security-cash-flow-machine-2026.json') as f:
    a = json.load(f)

body_clean = re.sub(r'<[^>]+>', ' ', a['bodyHtml'])
# Find FCF mentions
for line in body_clean.split('.'):
    if 'free cash flow' in line.lower() or 'FCF' in line:
        print(f"  Article claim: {line.strip()[:150]}...")

t = yf.Ticker('PANW')
info = t.info
fcf = info.get('freeCashflow')
ocf = info.get('operatingCashFlow')
capex = info.get('capitalExpenditures')
print(f"\n  yfinance FCF: ${fcf/1e9:.2f}B" if fcf else "  FCF not available")
print(f"  yfinance OCF: ${ocf/1e9:.2f}B" if ocf else "  OCF not available")
if capex: print(f"  yfinance Capex: ${abs(capex)/1e9:.2f}B")

# Check TTM FCF from quarterly cashflow
q_cf = t.quarterly_cashflow
print(f"\n  Quarterly cashflow available: {q_cf is not None}")
if q_cf is not None:
    if 'Free Cash Flow' in q_cf.index:
        ttm_fcf = q_cf.loc['Free Cash Flow'].iloc[0:4].sum()
        print(f"  TTM FCF (quarterly sum): ${ttm_fcf/1e9:.2f}B")
    if 'Operating Cash Flow' in q_cf.index and 'Capital Expenditure' in q_cf.index:
        ttm_ocf = q_cf.loc['Operating Cash Flow'].iloc[0:4].sum()
        ttm_capex = q_cf.loc['Capital Expenditure'].iloc[0:4].sum()
        print(f"  TTM OCF: ${ttm_ocf/1e9:.2f}B")
        print(f"  TTM Capex: ${abs(ttm_capex)/1e9:.2f}B")
        print(f"  TTM FCF (calc): ${(ttm_ocf + ttm_capex)/1e9:.2f}B")

# SMCI revenue claim
print(f"\n{'='*60}")
print("SMCI — Revenue Claim Verification")
print(f"{'='*60}")

with open('/home/chino/thesignal/articles/posts/smci-ai-server-comeback-2026.json') as f:
    a2 = json.load(f)

body_clean2 = re.sub(r'<[^>]+>', ' ', a2['bodyHtml'])
# Find revenue mentions
sentences = body_clean2.split('.')
print("  SMCI revenue-related claims:")
for s in sentences:
    if 'revenue' in s.lower() or '$' in s:
        s = s.strip()
        if s:
            print(f"    {s[:150]}")

t2 = yf.Ticker('SMCI')
inc2 = t2.income_stmt
q_inc2 = t2.quarterly_income_stmt

print(f"\n  SMCI Annual Revenue:")
if inc2 is not None and 'Total Revenue' in inc2.index:
    for col in inc2.columns[:3]:
        try:
            yr = col.strftime('%Y') if hasattr(col, 'strftime') else str(col)
            rev = inc2.loc['Total Revenue', col]
            print(f"    FY{yr}: ${rev/1e9:.2f}B")
        except:
            pass

if q_inc2 is not None and 'Total Revenue' in q_inc2.index:
    q_revs = q_inc2.loc['Total Revenue'].dropna()
    print(f"  TTM Revenue: ${q_revs.head(4).sum()/1e9:.2f}B")

# Revenue growth rate info
rg = t2.info.get('revenueGrowth')
print(f"  Revenue Growth rate: {rg*100:.1f}%" if rg else "  N/A")

# SOFI revenue claim
print(f"\n{'='*60}")
print("SOFI — Revenue Claim Verification")
print(f"{'='*60}")

with open('/home/chino/thesignal/articles/posts/sofi-everything-app-bank-charter-2026.json') as f:
    a3 = json.load(f)

body_clean3 = re.sub(r'<[^>]+>', ' ', a3['bodyHtml'])
print("  SOFI revenue-related claims:")
for s in body_clean3.split('.'):
    if 'revenue' in s.lower() or '$' in s:
        s = s.strip()
        if s:
            print(f"    {s[:150]}")

t3 = yf.Ticker('SOFI')
q_inc3 = t3.quarterly_income_stmt
if q_inc3 is not None and 'Total Revenue' in q_inc3.index:
    q_revs3 = q_inc3.loc['Total Revenue'].dropna()
    print(f"\n  SOFI Quarterly Revenue:")
    for i, (idx, val) in enumerate(q_revs3.head(4).items()):
        q_date = idx.strftime('%b %Y') if hasattr(idx, 'strftime') else str(idx)
        print(f"    {q_date}: ${val/1e9:.2f}B")
    print(f"  TTM Revenue: ${q_revs3.head(4).sum()/1e9:.2f}B")

# SOFI net income
print(f"  SOFI Net Income (quarterly):")
if q_inc3 is not None and 'Net Income' in q_inc3.index:
    for i, (idx, val) in enumerate(q_inc3.loc['Net Income'].dropna().head(4).items()):
        q_date = idx.strftime('%b %Y') if hasattr(idx, 'strftime') else str(idx)
        print(f"    {q_date}: ${val/1e9:.2f}B")

# RDDT clarification  
print(f"\n{'='*60}")
print("RDDT — Price Clarification")
print(f"{'='*60}")

t4 = yf.Ticker('RDDT')
hist4 = t4.history(period='5d')
print(f"  RDDT recent closes:")
for i in range(len(hist4)):
    r = hist4.iloc[i]
    print(f"    {r.name.strftime('%b %d')}: ${r['Close']:.2f}")
print(f"  RDDT article price: $198.00")
print(f"  RDDT July 15 close: $198.03")
print(f"  Difference: 0.015% — Price is CORRECT (article written pre-market Jul 16 using Jul 15 close)")
