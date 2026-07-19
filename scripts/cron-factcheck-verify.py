#!/usr/bin/env python3
"""Verify NET FCF claim ($755M vs actual ~$292M) and CRWV net loss."""
import yfinance as yf

# === NET: Check all FCF sources ===
print("=== NET FCF Investigation ===")
t = yf.Ticker('NET')
info = t.info

# Check info.freeCashflow
fcf_info = info.get('freeCashflow')
print(f"info.freeCashflow: ${fcf_info/1e6:.0f}M" if fcf_info else "info.freeCashflow: None")

# Operating cash flow from cashflow statement
cf = t.cashflow
if 'Operating Cash Flow' in cf.index:
    ocf = cf.loc['Operating Cash Flow']
    print(f"Annual OCF: { {str(k)[:10]: f'${v/1e6:.0f}M' for k,v in ocf.items()} }")
if 'Free Cash Flow' in cf.index:
    fcf_a = cf.loc['Free Cash Flow']
    print(f"Annual FCF: { {str(k)[:10]: f'${v/1e6:.0f}M' for k,v in fcf_a.items()} }")

# Quarterly OCF
q_cf = t.quarterly_cashflow
if 'Operating Cash Flow' in q_cf.index:
    q_ocf = q_cf.loc['Operating Cash Flow'].iloc[0:4]
    print(f"Q OCF: {[f'${v/1e6:.0f}M' for v in q_ocf]}")
    print(f"TTM OCF: ${q_ocf.sum()/1e6:.0f}M")
if 'Capital Expenditure' in q_cf.index:
    q_capex = q_cf.loc['Capital Expenditure'].iloc[0:4]
    print(f"Q Capex: {[f'${v/1e6:.0f}M' for v in q_capex]}")
    print(f"TTM Capex: ${q_capex.sum()/1e6:.0f}M")
if 'Free Cash Flow' in q_cf.index:
    q_fcf = q_cf.loc['Free Cash Flow'].iloc[0:4]
    print(f"Q FCF: {[f'${v/1e6:.0f}M' for v in q_fcf]}")
    print(f"TTM FCF from quarterly: ${q_fcf.sum()/1e6:.0f}M")

print()

# === CRWV: Check GAAP net loss ===
print("=== CRWV Net Loss Investigation ===")
t = yf.Ticker('CRWV')
inc = t.income_stmt
if 'Net Income' in inc.index:
    ni = inc.loc['Net Income']
    print(f"Annual Net Income: { {str(k)[:10]: f'${v/1e9:.2f}B' for k,v in ni.items()} }")
    fy2025_ni = ni.iloc[0] if len(ni) > 0 else None
    print(f"FY2025 Net Income: ${fy2025_ni/1e9:.2f}B")

# Also check Q data for depreciation/interest claims
q_inc = t.quarterly_income_stmt
if 'Depreciation And Amortization' in q_inc.index:
    da = q_inc.loc['Depreciation And Amortization'].iloc[0:4]
    print(f"Q D&A: {[f'${v/1e6:.0f}M' for v in da]}")
    print(f"TTM D&A: ${da.sum()/1e9:.2f}B")
if 'Interest Expense' in q_inc.index:
    ie = q_inc.loc['Interest Expense'].iloc[0:4]
    print(f"Q Interest: {[f'${v/1e6:.0f}M' for v in ie]}")
    print(f"TTM Interest: ${ie.sum()/1e9:.2f}B")

info = t.info
print(f"info.netIncomeToCommon: ${info.get('netIncomeToCommon')/1e9:.2f}B" if info.get('netIncomeToCommon') else "N/A")

# Check FY2025 net income from quarterly sum
q_ni = q_inc.loc['Net Income'].iloc[0:4] if 'Net Income' in q_inc.index else None
if q_ni is not None:
    ttm_ni = q_ni.sum()
    print(f"TTM Net Income (4Q sum): ${ttm_ni/1e9:.2f}B")
    print(f"Q NI: {[f'${v/1e6:.0f}M' for v in q_ni]}")

print()

# === PANW: Check FCF margin ===
print("=== PANW FCF Margin Check ===")
t = yf.Ticker('PANW')
info = t.info
fcf_info = info.get('freeCashflow')
print(f"info.freeCashflow: ${fcf_info/1e9:.2f}B" if fcf_info else "N/A")
