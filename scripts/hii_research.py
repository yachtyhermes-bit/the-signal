#!/usr/bin/env python3
"""Pull comprehensive HII data from yfinance."""
import json, sys
import yfinance as yf

t = yf.Ticker("HII")

info = t.info
keys = [
    "shortName","longName","sector","industry","marketCap","enterpriseValue",
    "trailingPE","forwardPE","priceToBook","priceToSalesTrailing12Months",
    "dividendYield","beta","fiftyTwoWeekHigh","fiftyTwoWeekLow",
    "currentPrice","targetMeanPrice","targetHighPrice","targetLowPrice",
    "recommendationKey","numberOfAnalystOpinions","totalRevenue","revenueGrowth",
    "grossMargins","operatingMargins","profitMargins","freeCashflow",
    "operatingCashflow","totalDebt","totalCash","currentRatio","debtToEquity",
    "returnOnEquity","returnOnAssets","sharesOutstanding","floatShares",
    "bookValue","earningsGrowth","earningsQuarterlyGrowth","pegRatio",
    "trailingEps","forwardEps","enterpriseToRevenue","enterpriseToEbitda",
    "totalCashPerShare","quickRatio","ebitda","ebitdaMargins",
]
out = {}
for k in keys:
    if k in info:
        out[k] = info[k]

print(json.dumps(out, indent=2, default=str))
