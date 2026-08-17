#!/usr/bin/env python3
"""Pull HWM fundamentals via yfinance for The Signal research."""
import json
import yfinance as yf

t = yf.Ticker("HWM")

info = t.info
keys = [
    "longName", "sector", "industry", "marketCap", "trailingPE", "forwardPE",
    "priceToSalesTrailing12Months", "priceToBook", "trailingEps", "forwardEps",
    "totalRevenue", "revenuePerShare", "revenueGrowth", "grossMargins",
    "operatingMargins", "profitMargins", "freeCashflow", "operatingCashflow",
    "totalDebt", "totalCash", "debtToEquity", "currentRatio", "returnOnEquity",
    "returnOnAssets", "dividendYield", "beta", "sharesOutstanding", "floatShares",
    "fiftyTwoWeekHigh", "fiftyTwoWeekLow", "currentPrice", "targetMeanPrice",
    "targetHighPrice", "targetLowPrice", "recommendationMean", "recommendationKey",
    "numberOfAnalystOpinions", "enterpriseValue", "ebitda", "totalCashPerShare",
    "earningsGrowth", "earningsQuarterlyGrowth", "profitMargins",
    "grossProfit", "totalRevenue", "bookValue", "pegRatio", "heldPercentInstitutions",
]
print("=== INFO (selected) ===")
for k in keys:
    if k in info:
        print(f"{k}: {info[k]}")

print("\n=== INCOME STATEMENT (annual, 4 years) ===")
try:
    inc = t.income_stmt
    print(inc.iloc[:, :4].to_string())
except Exception as e:
    print("ERR:", e)

print("\n=== INCOME STATEMENT (quarterly, 8 quarters) ===")
try:
    incq = t.quarterly_income_stmt
    print(incq.iloc[:, :8].to_string())
except Exception as e:
    print("ERR:", e)

print("\n=== BALANCE SHEET (annual) ===")
try:
    bs = t.balance_sheet
    print(bs.iloc[:, :3].to_string())
except Exception as e:
    print("ERR:", e)

print("\n=== CASH FLOW (annual) ===")
try:
    cf = t.cashflow
    print(cf.iloc[:, :4].to_string())
except Exception as e:
    print("ERR:", e)

print("\n=== QUARTERLY REVENUE + GROWTH ===")
try:
    q = t.quarterly_income_stmt
    rev = q.loc["Total Revenue"] if "Total Revenue" in q.index else None
    if rev is None:
        # try alternate row names
        for r in q.index:
            if "Revenue" in str(r):
                rev = q.loc[r]
                print("rev row:", r)
                break
    if rev is not None:
        for dt, v in rev.items():
            print(dt.date(), round(v/1e9, 3), "B")
except Exception as e:
    print("ERR:", e)

print("\n=== ANALYST RECOMMENDATIONS (recent) ===")
try:
    rec = t.recommendations
    print(rec.head(15).to_string())
except Exception as e:
    print("ERR:", e)

print("\n=== MAJOR HOLDERS ===")
try:
    mh = t.major_holders
    print(mh.to_string())
except Exception as e:
    print("ERR:", e)

print("\n=== INSTITUTIONAL HOLDERS (top) ===")
try:
    ih = t.institutional_holders
    print(ih.head(10).to_string())
except Exception as e:
    print("ERR:", e)
