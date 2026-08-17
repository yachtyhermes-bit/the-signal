import yfinance as yf
import json, datetime

t = yf.Ticker("INTC")

# Price history
h = t.history(period="1y", interval="1d")
print("=== PRICE HISTORY ===")
print("Last close:", h['Close'].iloc[-1], "| Date:", h.index[-1].date())
print("52w low:", h['Low'].min(), "| 52w high:", h['High'].max())
ytd = h[h.index >= '2026-01-01']
if len(ytd):
    start = ytd['Close'].iloc[0]
    end = ytd['Close'].iloc[-1]
    print(f"YTD 2026: start {start:.2f} -> end {end:.2f} = {(end/start-1)*100:.1f}%")
jul = h[(h.index >= '2026-06-30') & (h.index <= '2026-08-07')]
if len(jul):
    jstart = jul['Close'].iloc[0]
    jend = jul['Close'].iloc[-1]
    jmax = jul['Close'].max()
    print(f"Since Jun 30: start {jstart:.2f} -> end {jend:.2f} = {(jend/jstart-1)*100:.1f}% | max close {jmax:.2f}")

print("\n=== QUARTERLY INCOME (last 5 quarters) ===")
try:
    qinc = t.quarterly_income_stmt
    cols = [c for c in qinc.columns[:5]]
    for idx in ['Total Revenue','Net Income','Diluted EPS','Gross Profit','Operating Income']:
        if idx in qinc.index:
            row = {str(c.date()): qinc.loc[idx, c] for c in cols}
            print(idx, ":", json.dumps(row, default=str))
except Exception as e:
    print("ERR income:", e)

print("\n=== QUARTERLY CASHFLOW (last 4) ===")
try:
    qcf = t.quarterly_cashflow
    cols = [c for c in qcf.columns[:4]]
    for idx in ['Operating Cash Flow','Capital Expenditure','Free Cash Flow']:
        if idx in qcf.index:
            row = {str(c.date()): qcf.loc[idx, c] for c in cols}
            print(idx, ":", json.dumps(row, default=str))
except Exception as e:
    print("ERR cf:", e)

print("\n=== BALANCE SHEET (last 2) ===")
try:
    qbs = t.quarterly_balance_sheet
    cols = [c for c in qbs.columns[:2]]
    for idx in ['Cash And Cash Equivalents','Short Term Investments','Total Debt','Stockholders Equity']:
        if idx in qbs.index:
            row = {str(c.date()): qbs.loc[idx, c] for c in cols}
            print(idx, ":", json.dumps(row, default=str))
except Exception as e:
    print("ERR bs:", e)

print("\n=== EARNINGS DATES ===")
try:
    ed = t.earnings_dates.head(6)
    print(ed.to_string())
except Exception as e:
    print("ERR ed:", e)

print("\n=== ANALYST ESTIMATES ===")
try:
    est = t.estimates
    if est is not None:
        print(est.to_string())
except Exception as e:
    print("ERR est:", e)

print("\n=== NEWS (top 5) ===")
try:
    for n in t.news[:5]:
        print("-", n.get('providerPublishTime'), "|", n.get('title'))
except Exception as e:
    print("ERR news:", e)
