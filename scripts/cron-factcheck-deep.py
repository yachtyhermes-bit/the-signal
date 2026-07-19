#!/usr/bin/env python3
"""Deep fact-check specific claims from articles."""
import json, sys
import yfinance as yf

# === GE: Verify deferred revenue, FCF FY2025, ROE ===
print("=== GE Deep Check ===")
t = yf.Ticker('GE')

cf = t.cashflow
if 'Free Cash Flow' in cf.index:
    fcf = cf.loc['Free Cash Flow']
    print(f"FCF by year: { {str(k)[:10]: f'${v/1e9:.2f}B' for k,v in fcf.items()} }")

bs = t.balance_sheet
for idx in bs.index:
    if 'Deferred' in str(idx):
        print(f"{idx}: { {str(k)[:10]: f'${v/1e9:.2f}B' for k,v in bs.loc[idx].items()} }")

info = t.info
ni = info.get('netIncomeToCommon')
bve = info.get('bookValue')
shares = info.get('sharesOutstanding')
print(f"Net income: ${ni/1e9}B, Book value/sh: ${bve}, Shares: {shares}")
if ni and bve and shares:
    equity = bve * shares
    roe = ni / equity * 100
    print(f"Calc ROE: {roe:.1f}%")

# Q2 2026 EPS
eps = info.get('trailingEps')
print(f"Trailing EPS: ${eps}")

print()

# === PANW: Verify $3.79B TTM FCF, $177M GAAP loss, $3B revenue ===
print("=== PANW Deep Check ===")
t = yf.Ticker('PANW')
q_cf = t.quarterly_cashflow
if 'Free Cash Flow' in q_cf.index:
    ttm_fcf = q_cf.loc['Free Cash Flow'].iloc[0:4].sum()
    print(f"TTM FCF: ${ttm_fcf/1e9:.3f}B")
    print(f"Q FCF: {[f'${v/1e9:.3f}B' for v in list(q_cf.loc['Free Cash Flow'].iloc[0:4])]}")

q_inc = t.quarterly_income_stmt
if 'Net Income' in q_inc.index:
    q_ni = q_inc.loc['Net Income'].iloc[0:4]
    print(f"Q NI: {[f'${v/1e6:.0f}M' for v in q_ni]}")
    print(f"Latest Q NI: ${q_ni.iloc[0]/1e6:.0f}M")
if 'Total Revenue' in q_inc.index:
    q_rev = q_inc.loc['Total Revenue'].iloc[0:4]
    print(f"Q Rev: {[f'${v/1e9:.2f}B' for v in q_rev]}")
    print(f"Latest Q Rev: ${q_rev.iloc[0]/1e9:.2f}B")

info = t.info
print(f"Forward PE: {info.get('forwardPE')}")
print(f"Trailing PE: {info.get('trailingPE')}")

print()

# === NET: Verify $2.33B TTM revenue, $755M FCF ===
print("=== NET Deep Check ===")
t = yf.Ticker('NET')
q_inc = t.quarterly_income_stmt
if 'Total Revenue' in q_inc.index:
    ttm_rev = q_inc.loc['Total Revenue'].iloc[0:4].sum()
    print(f"TTM Revenue: ${ttm_rev/1e9:.3f}B")
    print(f"Q Rev: {list(q_inc.loc['Total Revenue'].iloc[0:4])}")

q_cf = t.quarterly_cashflow
if 'Free Cash Flow' in q_cf.index:
    fcf_data = q_cf.loc['Free Cash Flow'].iloc[0:4]
    ttm_fcf = fcf_data.sum()
    print(f"TTM FCF: ${ttm_fcf/1e6:.0f}M")
    print(f"Q FCF: {[f'${v/1e6:.0f}M' for v in fcf_data]}")
elif 'Operating Cash Flow' in q_cf.index and 'Capital Expenditure' in q_cf.index:
    ttm_ocf = q_cf.loc['Operating Cash Flow'].iloc[0:4].sum()
    ttm_capex = q_cf.loc['Capital Expenditure'].iloc[0:4].sum()
    ttm_fcf = ttm_ocf + ttm_capex
    print(f"TTM OCF: ${ttm_ocf/1e6:.0f}M")
    print(f"TTM Capex: ${ttm_capex/1e6:.0f}M")
    print(f"Calc TTM FCF: ${ttm_fcf/1e6:.0f}M")

# Annual FCF
cf = t.cashflow
if 'Free Cash Flow' in cf.index:
    fcf_a = cf.loc['Free Cash Flow']
    print(f"Annual FCF: { {str(k)[:10]: f'${v/1e6:.0f}M' for k,v in fcf_a.items()} }")

print()

# === ARM: Verify revenue ===
print("=== ARM Deep Check ===")
t = yf.Ticker('ARM')
inc = t.income_stmt
if 'Total Revenue' in inc.index:
    rev = inc.loc['Total Revenue']
    print(f"Revenue: { {str(k)[:10]: f'${v/1e9:.2f}B' for k,v in rev.items()} }")
info = t.info
print(f"Gross margin: {info.get('grossMargins')*100:.1f}%")
print(f"Profit margin: {info.get('profitMargins')*100:.1f}%")

print()

# === CRWV: Quick check ===
print("=== CRWV Deep Check ===")
t = yf.Ticker('CRWV')
info = t.info
print(f"FY2026 guidance range: check estimates")
est = t.earnings_estimate
if est is not None:
    print(f"Earnings estimate: {est}")
print(f"Revenue estimate: {t.revenue_estimate}")
