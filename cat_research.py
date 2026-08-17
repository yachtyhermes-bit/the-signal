import yfinance as yf
import json

t = yf.Ticker("CAT")

info = t.info
keys = [
    "currentPrice", "regularMarketPrice", "previousClose", "marketCap",
    "trailingPE", "forwardPE", "trailingEps", "forwardEps",
    "totalRevenue", "revenueGrowth", "grossMargins", "operatingMargins", "profitMargins",
    "freeCashflow", "operatingCashflow", "capitalExpenditures",
    "totalDebt", "totalCash", "debtToEquity", "currentRatio",
    "sector", "industry", "market", "exchange",
    "fiftyTwoWeekHigh", "fiftyTwoWeekLow", "targetMeanPrice", "targetHighPrice", "targetLowPrice",
    "recommendationKey", "numberOfAnalystOpinions", "dividendYield", "dividendRate",
    "earningsQuarterlyGrowth", "earningsGrowth", "profitMargins", "beta",
    "enterpriseValue", "priceToBook", "bookValue", "returnOnEquity", "returnOnAssets",
    "sharesOutstanding", "floatShares",
]
out = {}
for k in keys:
    v = info.get(k)
    if v is not None:
        out[k] = v

print("=== INFO ===")
print(json.dumps(out, indent=2, default=str))

print("\n=== EARNINGS (quarterly) ===")
try:
    print(t.earnings_dates.head(8).to_string())
except Exception as e:
    print("earnings_dates error:", e)

print("\n=== QUARTERLY INCOME (last 6q) ===")
try:
    qi = t.quarterly_income_stmt
    cols = qi.columns[:6]
    print(qi[cols].to_string())
except Exception as e:
    print("income error:", e)

print("\n=== ANNUAL INCOME ===")
try:
    print(t.income_stmt.iloc[:, :3].to_string())
except Exception as e:
    print("annual income error:", e)

print("\n=== BALANCE SHEET (total debt rows) ===")
try:
    bs = t.balance_sheet
    for row in ["Total Debt", "Total Non Current Debt", "Current Debt", "Cash And Cash Equivalents", "Stockholders Equity"]:
        if row in bs.index:
            print(row, "->", bs.loc[row].iloc[:3].to_dict())
except Exception as e:
    print("bs error:", e)

print("\n=== CASHFLOW (annual, first 3) ===")
try:
    cf = t.cashflow
    for row in ["Free Cash Flow", "Operating Cash Flow", "Capital Expenditure"]:
        if row in cf.index:
            print(row, "->", cf.loc[row].iloc[:3].to_dict())
except Exception as e:
    print("cf error:", e)

print("\n=== PRICE (1mo) ===")
try:
    h = t.history(period="1mo")
    print(h[["Close", "Volume"]].to_string())
except Exception as e:
    print("history error:", e)
