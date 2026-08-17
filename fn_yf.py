#!/usr/bin/env python3
"""Pull Fabrinet (FN) data via yfinance for research brief."""
import json, datetime
import yfinance as yf

t = yf.Ticker("FN")
out = {}

# --- Info ---
info = t.info
keys = ["longName","shortName","sector","industry","exchange","marketCap","sharesOutstanding",
        "trailingPE","forwardPE","trailingEps","forwardEps","fiftyTwoWeekHigh","fiftyTwoWeekLow",
        "grossMargins","operatingMargins","profitMargins","totalDebt","totalCash","freeCashflow",
        "totalRevenue","revenueGrowth","earningsGrowth","bookValue","priceToBook","currentPrice",
        "previousClose","fiftyDayAverage","twoHundredDayAverage","targetMeanPrice","targetHighPrice",
        "targetLowPrice","recommendationMean","recommendationKey","numberOfAnalystOpinions",
        "enterpriseValue","debtToEquity","totalCashPerShare","beta","dividendYield","ebitda",
        "operatingCashflow","returnOnEquity","returnOnAssets","totalAssets","totalLiabilities",
        "currentPrice","regularMarketPrice","regularMarketPreviousClose","currency","quoteType"]
out["info"] = {k: info.get(k) for k in keys if k in info}

# --- Price history: last 30 trading days ---
hist = t.history(period="3mo", interval="1d", auto_adjust=False)
hist = hist[["Open","High","Low","Close","Volume"]]
out["history_last30"] = json.loads(hist.tail(30).to_json(date_format="iso"))
out["last_close_date"] = str(hist.index[-1].date()) if len(hist) else None

# --- Earnings dates ---
try:
    ed = t.get_earnings_dates(limit=8)
    out["earnings_dates"] = json.loads(ed.to_json(date_format="iso"))
except Exception as e:
    out["earnings_dates_err"] = str(e)

# --- Quarterly financials (most recent 6 quarters) ---
try:
    qf = t.quarterly_financials
    out["quarterly_financials"] = json.loads(qf.iloc[:, :6].to_json())
except Exception as e:
    out["quarterly_financials_err"] = str(e)

try:
    qc = t.quarterly_cashflow
    out["quarterly_cashflow"] = json.loads(qc.iloc[:, :6].to_json())
except Exception as e:
    out["quarterly_cashflow_err"] = str(e)

try:
    qb = t.quarterly_balance_sheet
    out["quarterly_balance_sheet"] = json.loads(qb.iloc[:, :6].to_json())
except Exception as e:
    out["quarterly_balance_sheet_err"] = str(e)

# --- Annual financials (last 3 FY) ---
try:
    af = t.financials
    out["annual_financials"] = json.loads(af.iloc[:, :3].to_json())
except Exception as e:
    out["annual_financials_err"] = str(e)

print(json.dumps(out, indent=1, default=str))
