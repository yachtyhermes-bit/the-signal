import yfinance as yf
import json

t = yf.Ticker("PATH")
info = t.info

keys = [
    "ticker", "shortName", "longName", "sector", "industry", "marketCap",
    "trailingPE", "forwardPE", "priceToSalesTrailing12Months",
    "totalRevenue", "trailingEps", "forwardEps", "targetMeanPrice",
    "targetHighPrice", "targetLowPrice", "recommendationKey",
    "numberOfAnalystOpinions", "freeCashflow", "totalDebt", "totalCash",
    "totalCashPerShare", "currentPrice", "previousClose", "fiftyTwoWeekLow",
    "fiftyTwoWeekHigh", "fiftyTwoWeekChange", "grossMargins", "operatingMargins",
    "profitMargins", "revenueGrowth", "earningsGrowth", "enterpriseValue",
    "totalRevenue", "revenuePerShare", "bookValue", "returnOnEquity",
    "debtToEquity", "currentRatio", "quickRatio", "beta", "sharesOutstanding",
    "floatShares", "dividendYield", "payoutRatio", "financialCurrency",
    "exchange", "website", "longBusinessSummary",
]

out = {}
for k in keys:
    v = info.get(k)
    if isinstance(v, float):
        v = round(v, 4)
    out[k] = v

print(json.dumps(out, indent=2, default=str))
