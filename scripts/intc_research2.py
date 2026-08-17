import yfinance as yf
import json

t = yf.Ticker("INTC")

h = t.history(period="1y", interval="1d")

def chg(a, b):
    return (b/a - 1) * 100

print("=== JULY / EARNINGS MOVE ===")
for label, d1, d2 in [("July (Jul1->Jul31)", '2026-07-01', '2026-07-31'),
                      ("Earnings day (Jul23->Jul24)", '2026-07-23', '2026-07-24'),
                      ("Post-earnings (Jul23->Jul31)", '2026-07-23', '2026-07-31'),
                      ("Jun30 peak -> Aug7", '2026-06-30', '2026-08-07')]:
    s = h.loc[:d1]['Close'].iloc[-1]
    e = h.loc[:d2]['Close'].iloc[-1]
    print(f"{label}: {s:.2f} -> {e:.2f} = {chg(s,e):.1f}%")

print("\n=== BALANCE SHEET detail (2026-06-30) ===")
try:
    qbs = t.quarterly_balance_sheet
    col = qbs.columns[0]
    for idx in ['Cash And Cash Equivalents','Short Term Investments','Cash Cash Equivalents And Short Term Investments','Total Debt','Long Term Debt','Current Debt','Stockholders Equity','Total Assets']:
        if idx in qbs.index:
            print(idx, ":", qbs.loc[idx, col])
except Exception as e:
    print("ERR:", e)

print("\n=== ANALYST PRICE TARGETS ===")
try:
    apt = t.analyst_price_targets
    print(apt.to_dict())
except Exception as e:
    print("ERR apt:", e)

print("\n=== EARNINGS ESTIMATE (fwd) ===")
try:
    ee = t.earnings_estimate
    print(ee.to_string())
except Exception as e:
    print("ERR ee:", e)

print("\n=== REVENUE ESTIMATE (fwd) ===")
try:
    re = t.revenue_estimate
    print(re.to_string())
except Exception as e:
    print("ERR re:", e)

print("\n=== GROWTH ESTIMATES ===")
try:
    ge = t.growth_estimates
    print(ge.to_string())
except Exception as e:
    print("ERR ge:", e)

print("\n=== RECOMMENDATIONS ===")
try:
    rec = t.recommendations_summary
    print(rec.to_string())
except Exception as e:
    print("ERR rec:", e)

print("\n=== DIVIDENDS ===")
try:
    dv = t.dividends.tail(4)
    print(dv.to_string())
except Exception as e:
    print("ERR dv:", e)

print("\n=== SHORT RATIO / SPLITS ===")
try:
    print("shortRatio:", t.info.get('shortRatio'))
    print("sharesShort:", t.info.get('sharesShort'))
    print("splits:", t.splits.tail(3).to_dict())
except Exception as e:
    print("ERR:", e)
