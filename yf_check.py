import yfinance as yf
import json

t = yf.Ticker("IFNNY")
try:
    info = t.info
except Exception as e:
    print("info error:", e)
    info = {}

keys = ["currentPrice", "previousClose", "regularMarketPrice", "marketCap", "totalRevenue",
        "trailingPE", "forwardPE", "freeCashflow", "totalDebt", "totalCash",
        "fiftyTwoWeekLow", "fiftyTwoWeekHigh", "targetMeanPrice", "targetHighPrice", "targetLowPrice",
        "recommendationKey", "sharesOutstanding", "fiftyDayAverage", "twoHundredDayAverage",
        "currency", "longName", "shortName", "exchange", "quoteType"]
for k in keys:
    print(f"{k}: {info.get(k)}")

print("---HISTORY (last 6 sessions)---")
h = t.history(period="10d")
print(h[["Close"]].tail(6).to_string())
