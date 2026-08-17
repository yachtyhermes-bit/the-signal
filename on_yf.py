#!/usr/bin/env python3
"""Pull ON Semiconductor (ON) data from yfinance."""
import json
import yfinance as yf

t = yf.Ticker("ON")
info = t.info

keys = [
    "currentPrice", "previousClose", "open", "dayHigh", "dayLow",
    "marketCap", "enterpriseValue", "trailingPE", "forwardPE",
    "trailingEps", "forwardEps", "priceToBook", "priceToSalesTrailing12Months",
    "totalRevenue", "revenueGrowth", "grossMargins", "operatingMargins", "profitMargins",
    "freeCashflow", "operatingCashflow", "totalCash", "totalDebt", "totalCashPerShare",
    "currentRatio", "debtToEquity", "returnOnEquity", "returnOnAssets",
    "fiftyTwoWeekHigh", "fiftyTwoWeekLow", "fiftyTwoWeekChange",
    "targetHighPrice", "targetLowPrice", "targetMeanPrice", "targetMedianPrice",
    "recommendationKey", "recommendationMean", "numberOfAnalystOpinions",
    "earningsGrowth", "earningsQuarterlyGrowth", "revenuePerShare",
    "sharesOutstanding", "sharesShort", "shortRatio", "beta",
    "dividendYield", "payoutRatio", "bookValue", "sector", "industry",
    "longName", "website", "earningsDate", "exDividendDate",
]

out = {}
for k in keys:
    try:
        out[k] = info.get(k)
    except Exception as e:
        out[k] = f"ERR: {e}"

# Earnings history (quarterly)
try:
    q = t.quarterly_income_stmt
    out["quarterly_income_stmt"] = {str(c): q[c].to_dict() for c in q.columns[:4]}
except Exception as e:
    out["quarterly_income_stmt"] = f"ERR: {e}"

try:
    c = t.cashflow
    out["cashflow_annual"] = {str(c): c[c].to_dict() for c in c.columns[:3]}
except Exception as e:
    out["cashflow_annual"] = f"ERR: {e}"

try:
    b = t.balance_sheet
    out["balance_sheet"] = {str(b): b[b].to_dict() for b in b.columns[:2]}
except Exception as e:
    out["balance_sheet"] = f"ERR: {e}"

# Recent price action
try:
    h = t.history(period="3mo")
    out["recent_close"] = {str(d.date()): round(float(r["Close"]), 2) for d, r in h.iterrows()}
except Exception as e:
    out["recent_close"] = f"ERR: {e}"

print(json.dumps(out, indent=2, default=str))
