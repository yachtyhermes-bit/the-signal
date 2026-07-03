import yfinance as yf, json

# Deeper checks for LHX revenue and other specific claims

# LHX - check quarterly/annual revenue
print("===== LHX Deep Dive =====")
tk = yf.Ticker("LHX")
try:
    qinc = tk.quarterly_financials
    if qinc is not None and 'Total Revenue' in qinc.index:
        revs = qinc.loc['Total Revenue']
        print(f"Quarterly Revenues: {[f'{x/1e9:.2f}B' for x in revs.iloc[:4]]}")
        ttm = revs.iloc[0:4].sum()
        print(f"TTM Revenue: {ttm/1e9:.2f}B")
except Exception as e:
    print(f"Quarterly error: {e}")

try:
    inc = tk.income_stmt
    if inc is not None and 'Total Revenue' in inc.index:
        annual_revs = inc.loc['Total Revenue']
        print(f"Annual Revenues: {[f'{x/1e9:.2f}B' for x in annual_revs.iloc[:3]]}")
except Exception as e:
    print(f"Annual error: {e}")

try:
    cf = tk.cashflow
    if cf is not None and 'Free Cash Flow' in cf.index:
        fcf = cf.loc['Free Cash Flow']
        print(f"Annual FCF: {[f'{x/1e9:.2f}B' for x in fcf.iloc[:2]]}")
except Exception as e:
    print(f"Cashflow error: {e}")

try:
    bs = tk.balance_sheet
    if bs is not None and 'Total Debt' in bs.index:
        debt = bs.loc['Total Debt']
        print(f"Total Debt: {[f'{x/1e9:.2f}B' for x in debt.iloc[:2]]}")
except Exception as e:
    print(f"BS error: {e}")

# AVGO - check net income
print("\n===== AVGO Deep Dive =====")
tk = yf.Ticker("AVGO")
try:
    qinc = tk.quarterly_financials
    if qinc is not None and 'Net Income' in qinc.index:
        ni = qinc.loc['Net Income']
        print(f"Quarterly Net Income: {[f'{x/1e9:.2f}B' for x in ni.iloc[:4]]}")
        ttm_ni = ni.iloc[0:4].sum()
        print(f"TTM Net Income: {ttm_ni/1e9:.2f}B")
except Exception as e:
    print(f"Error: {e}")

# ANET - check net income
print("\n===== ANET Deep Dive =====")
tk = yf.Ticker("ANET")
try:
    qinc = tk.quarterly_financials
    if qinc is not None and 'Net Income' in qinc.index:
        ni = qinc.loc['Net Income']
        print(f"Quarterly Net Income: {[f'{x/1e9:.2f}B' for x in ni.iloc[:4]]}")
        ttm_ni = ni.iloc[0:4].sum()
        print(f"TTM Net Income: {ttm_ni/1e9:.2f}B")
except Exception as e:
    print(f"Error: {e}")

try:
    # Check growth rate - 27.7% on what base?
    inc = tk.income_stmt
    if inc is not None and 'Total Revenue' in inc.index:
        revs = inc.loc['Total Revenue']
        if len(revs) >= 3:
            fy2023 = revs.iloc[2] if len(revs) > 2 else None
            fy2024 = revs.iloc[1]
            fy2025 = revs.iloc[0]
            print(f"FY2023 Rev: {fy2023/1e9:.2f}B")
            print(f"FY2024 Rev: {fy2024/1e9:.2f}B")
            print(f"FY2025 Rev: {fy2025/1e9:.2f}B")
            print(f"FY2024->FY2025 growth: {(fy2025-fy2024)/fy2024*100:.1f}%")
            if fy2023:
                print(f"FY2023->FY2024 growth: {(fy2024-fy2023)/fy2023*100:.1f}%")
except Exception as e:
    print(f"Error: {e}")

# MRVL growth rate check
print("\n===== MRVL Deep Dive =====")
tk = yf.Ticker("MRVL")
try:
    qinc = tk.quarterly_financials
    if qinc is not None and 'Total Revenue' in qinc.index:
        revs = qinc.loc['Total Revenue']
        # Last 4 quarters TTM
        current_ttm = revs.iloc[0:4].sum()
        # Prior 4 quarters TTM
        prior_ttm = revs.iloc[4:8].sum() if len(revs) >= 8 else None
        print(f"Current TTM: {current_ttm/1e9:.2f}B")
        if prior_ttm:
            print(f"Prior TTM: {prior_ttm/1e9:.2f}B")
            print(f"TTM Growth: {(current_ttm-prior_ttm)/prior_ttm*100:.1f}%")
except Exception as e:
    print(f"Error: {e}")

# NVDA check revenue detail
print("\n===== NVDA Deep Dive =====")
tk = yf.Ticker("NVDA")
try:
    inc = tk.income_stmt
    if inc is not None and 'Total Revenue' in inc.index:
        revs = inc.loc['Total Revenue']
        print(f"Annual Revenues: {[f'{x/1e9:.2f}B' for x in revs.iloc[:4]]}")
        # FY2026 growth
        if len(revs) >= 2:
            growth = (revs.iloc[0] - revs.iloc[1]) / revs.iloc[1] * 100
            print(f"FY2026 growth YoY: {growth:.1f}%")
except Exception as e:
    print(f"Error: {e}")
