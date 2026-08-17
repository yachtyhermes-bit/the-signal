#!/usr/bin/env python3
"""Fetch AMAT data from yfinance for earnings preview research."""
import json
import yfinance as yf

t = yf.Ticker("AMAT")
info = t.info

keys = [
    "currentPrice", "regularMarketPrice", "marketCap", "forwardPE", "trailingPE",
    "totalRevenue", "totalCash", "totalDebt", "freeCashflow", "operatingCashflow",
    "fiftyTwoWeekHigh", "fiftyTwoWeekLow", "fiftyTwoWeekChange",
    "recommendationKey", "recommendationMean", "numberOfAnalystOpinions",
    "targetMeanPrice", "targetHighPrice", "targetLowPrice", "targetMedianPrice",
    "sharesOutstanding", "enterpriseValue", "bookValue", "priceToBook",
    "profitMargins", "grossMargins", "revenueGrowth", "earningsGrowth",
    "longName", "sector", "industry", "exchange", "currency", "shortName",
]

out = {}
for k in keys:
    v = info.get(k)
    if v is not None:
        out[k] = v

# Fallback for current price
if "currentPrice" not in out and "regularMarketPrice" in out:
    out["currentPrice"] = out["regularMarketPrice"]

print(json.dumps(out, indent=2, default=str))

# Also try analysts data
try:
    rec = t.recommendations
    if rec is not None and not rec.empty:
        print("\n--- RECOMMENDATIONS (last 3) ---")
        print(rec.tail(3).to_string())
except Exception as e:
    print(f"\nrec error: {e}")

try:
    su = t.get_sustainability()
except Exception as e:
    print(f"sustain error: {e}")
