#!/usr/bin/env python3
"""Fetch TTD fundamentals via yfinance."""
import json
import yfinance as yf

t = yf.Ticker("TTD")
info = t.info

keys = [
    "currentPrice", "previousClose", "marketCap", "trailingPE", "forwardPE",
    "priceToBook", "priceToSalesTrailing12Months", "enterpriseValue",
    "totalRevenue", "trailingEps", "forwardEps", "targetMeanPrice",
    "targetHighPrice", "targetLowPrice", "numberOfAnalystOpinions",
    "recommendationKey", "totalCash", "totalDebt", "totalCashPerShare",
    "freeCashflow", "operatingCashflow", "grossMargins", "operatingMargins",
    "profitMargins", "ebitdaMargins", "ebitda", "revenueGrowth",
    "earningsGrowth", "returnOnEquity", "returnOnAssets", "beta",
    "sharesOutstanding", "floatShares", "fiftyTwoWeekHigh", "fiftyTwoWeekLow",
    "fiftyTwoWeekChange", "ytdReturn", "bookValue", "pegRatio", "debtToEquity",
    "currentRatio", "quickRatio", "totalRevenueGrowth", "grossProfits",
    "revenuePerShare", "dividendYield", "sector", "industry",
    "longBusinessSummary", "shortName", "longName", "exchange", "website",
]

out = {}
for k in keys:
    v = info.get(k)
    if isinstance(v, float):
        v = round(v, 4)
    out[k] = v

print(json.dumps(out, indent=2, default=str))

# Financials
print("\n--- INCOME STATEMENT (annual, last 2) ---")
try:
    print(t.income_stmt.iloc[:, :2].to_string())
except Exception as e:
    print("ERR", e)

print("\n--- BALANCE SHEET (annual, last 2) ---")
try:
    print(t.balance_sheet.iloc[:, :2].to_string())
except Exception as e:
    print("ERR", e)

print("\n--- CASHFLOW (annual, last 2) ---")
try:
    print(t.cashflow.iloc[:, :2].to_string())
except Exception as e:
    print("ERR", e)

print("\n--- ANALYST RECOMMENDATIONS ---")
try:
    print(t.recommendations.head(10).to_string())
except Exception as e:
    print("ERR", e)

print("\n--- EARNINGS DATES ---")
try:
    print(t.get_earnings_dates(limit=6).to_string())
except Exception as e:
    print("ERR", e)
