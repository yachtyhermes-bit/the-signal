import yfinance as yf

# ANET - check TTM growth rate (35%)
print("===== ANET TTM Growth =====")
tk = yf.Ticker("ANET")
try:
    q = tk.quarterly_financials
    if q is not None and 'Total Revenue' in q.index:
        revs = q.loc['Total Revenue']
        print(f"Recent 8 quarters: {[f'{x/1e9:.2f}B' for x in revs.iloc[:8]]}")
        current_ttm = revs.iloc[0:4].sum()
        prior_ttm = revs.iloc[4:8].sum() if len(revs) >= 8 else None
        print(f"Current TTM: {current_ttm/1e9:.2f}B")
        if prior_ttm:
            print(f"Prior TTM: {prior_ttm/1e9:.2f}B")
            print(f"TTM Growth: {(current_ttm-prior_ttm)/prior_ttm*100:.1f}%")
except Exception as e:
    print(f"Error: {e}")

# Check ANET stock price
ti = tk.info
print(f"ANET current price: {ti.get('currentPrice') or ti.get('previousClose')}")
print(f"ANET 52W high: {ti.get('fiftyTwoWeekHigh')}")
print(f"ANET enterprise value: {ti.get('enterpriseValue')}")
print(f"ANET debt: {ti.get('totalDebt')}")
print(f"ANET cash: {ti.get('totalCash')}")
print(f"ANET free cash flow: {ti.get('freeCashflow')}")

# MRVL - check TTM growth
print("\n===== MRVL TTM Growth =====")
tk = yf.Ticker("MRVL")
try:
    q = tk.quarterly_financials
    if q is not None and 'Total Revenue' in q.index:
        revs = q.loc['Total Revenue']
        print(f"Recent 8 quarters: {[f'{x/1e9:.2f}B' for x in revs.iloc[:8]]}")
        current_ttm = revs.iloc[0:4].sum()
        prior_ttm = revs.iloc[4:8].sum() if len(revs) >= 8 else None
        print(f"Current TTM: {current_ttm/1e9:.2f}B")
        if prior_ttm:
            print(f"Prior TTM: {prior_ttm/1e9:.2f}B")
            print(f"TTM Growth: {(current_ttm-prior_ttm)/prior_ttm*100:.1f}%")
except Exception as e:
    print(f"Error: {e}")

ti = tk.info
print(f"MRVL current price: {ti.get('currentPrice') or ti.get('previousClose')}")

# Check "the stock shed another 18.7% over the past month" - get price 1 month ago
hist = tk.history(period="1mo")
if len(hist) > 0:
    current_p = hist.iloc[-1]['Close']
    month_ago = hist.iloc[0]['Close']
    print(f"MRVL 1 month ago close: {month_ago:.2f}")
    print(f"MRVL current close: {current_p:.2f}")
    print(f"MRVL 1 month change: {(current_p - month_ago)/month_ago*100:.1f}%")

# NVDA - verify FY2026 revenue
print("\n===== NVDA Checks =====")
tk = yf.Ticker("NVDA")
ti = tk.info
print(f"NVDA current price: {ti.get('currentPrice') or ti.get('previousClose')}")
print(f"NVDA market cap: {ti.get('marketCap')/1e9:.2f}B")
print(f"NVDA forward PE: {ti.get('forwardPE')}")
print(f"NVDA trailing PE: {ti.get('trailingPE')}")
print(f"NVDA gross margin: {ti.get('grossMargins')*100 if ti.get('grossMargins') else 'N/A'}%")
hist = tk.history(period="1mo")
print(f"NVDA 1 month high: {hist['Close'].max():.2f}")
print(f"NVDA 1 month low: {hist['Close'].min():.2f}")

# Check NVDA forward PE calculation - article says 15.48x
# NVDA article price: $197.58, close from hist
print(f"NVDA latest close: {hist.iloc[-1]['Close']:.2f}")
print(f"NVDA shares outstanding: {ti.get('sharesOutstanding', 'N/A')}")
print(f"NVDA FY27 EPS estimate: {ti.get('forwardEps', 'N/A')}")
print(f"NVDA current market cap from shares: {ti.get('marketCap')/1e9:.2f}B")
