import yfinance as yf
import json

t = yf.Ticker('LMT')
i = t.info
keys = ['currentPrice','previousClose','regularMarketPrice','marketCap','forwardPE','trailingPE',
        'totalRevenue','fiftyTwoWeekLow','fiftyTwoWeekHigh','recommendationKey','targetMeanPrice',
        'targetHighPrice','targetLowPrice','freeCashflow','totalDebt','totalCash','sharesOutstanding',
        'sector','industry','recommendationMean','numberOfAnalystOpinions','pegRatio','priceToBook',
        'enterpriseValue','grossMargins','operatingMargins','profitMargins','revenueGrowth','earningsGrowth',
        'bookValue','trailingEps','forwardEps','dividendYield','payoutRatio','beta','longName','website']
out = {k: i.get(k) for k in keys}
print(json.dumps(out, indent=1, default=str))

# quarterly results context
print("=== QUARTERLY ===")
try:
    q = t.quarterly_financials
    print(q.head(4).to_string())
except Exception as e:
    print("quarterly err", e)
print("=== INCOME STATEMENT (annual) ===")
try:
    inc = t.income_stmt
    print(inc.head(2).to_string())
except Exception as e:
    print("inc err", e)
print("=== CASHFLOW (annual) ===")
try:
    cf = t.cashflow
    print(cf.head(2).to_string())
except Exception as e:
    print("cf err", e)
print("=== RECOMMENDATIONS ===")
try:
    rec = t.recommendations
    print(rec.tail(3).to_string())
except Exception as e:
    print("rec err", e)
