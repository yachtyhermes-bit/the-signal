#!/usr/bin/env python3
"""Collect BRK.B data via yfinance for The Signal research."""
import json
import yfinance as yf

t = yf.Ticker("BRK-B")

info = t.info
keys = [
    "shortName", "longName", "sector", "industry", "marketCap",
    "trailingPE", "forwardPE", "priceToBook", "bookValue",
    "totalRevenue", "revenueGrowth", "grossMargins", "operatingMargins",
    "profitMargins", "trailingEps", "forwardEps", "returnOnEquity",
    "debtToEquity", "totalCash", "totalDebt", "freeCashflow",
    "operatingCashflow", "currentPrice", "previousClose", "open",
    "dayHigh", "dayLow", "fiftyTwoWeekHigh", "fiftyTwoWeekLow",
    "fiftyDayAverage", "twoHundredDayAverage", "beta", "dividendYield",
    "sharesOutstanding", "floatShares", "totalCashPerShare",
    "earningsQuarterlyGrowth", "targetMeanPrice", "recommendationKey",
    "numberOfAnalystOpinions", "regularMarketPrice", "regularMarketPreviousClose",
]
out = {"info": {k: info.get(k) for k in keys}}

# Price history — last 30 trading days
hist = t.history(period="3mo", interval="1d")
out["history"] = {
    "columns": list(hist.columns),
    "recent": [
        {"date": str(idx.date()), "close": round(float(r["Close"]), 2), "volume": int(r["Volume"])}
        for idx, r in hist.tail(15).iterrows()
    ],
    "last_close": float(hist["Close"].iloc[-1]),
    "period_high": float(hist["High"].max()),
    "period_low": float(hist["Low"].min()),
}

# Quarterly financials
try:
    qf = t.quarterly_financials
    qcols = [str(c.date()) for c in qf.columns]
    qrows = {
        "Total Revenue": None,
        "Net Income": None,
        "Operating Income": None,
        "Diluted EPS": None,
    }
    out["quarterly_financials"] = {"columns": qcols, "rows": {}}
    for row_name in qrows:
        if row_name in qf.index:
            vals = {}
            for c in qf.columns:
                v = qf.loc[row_name, c]
                vals[str(c.date())] = None if v is None else float(v)
            out["quarterly_financials"]["rows"][row_name] = vals
except Exception as e:
    out["quarterly_financials_error"] = str(e)

# Balance sheet (cash)
try:
    bs = t.quarterly_balance_sheet
    out["balance_sheet"] = {"columns": [str(c.date()) for c in bs.columns]}
    for row_name in ["Cash And Cash Equivalents", "Other Short Term Investments", "Total Assets", "Stockholders Equity", "Common Stock Equity"]:
        if row_name in bs.index:
            vals = {}
            for c in bs.columns:
                v = bs.loc[row_name, c]
                vals[str(c.date())] = None if v is None else float(v)
            out["balance_sheet"][row_name] = vals
except Exception as e:
    out["balance_sheet_error"] = str(e)

# Cashflow (buybacks proxy: common stock repurchases)
try:
    cf = t.quarterly_cashflow
    out["cashflow"] = {"columns": [str(c.date()) for c in cf.columns]}
    for row_name in cf.index:
        if "Repurchase" in row_name or "repurchase" in row_name or "Buyback" in row_name:
            vals = {}
            for c in cf.columns:
                v = cf.loc[row_name, c]
                vals[str(c.date())] = None if v is None else float(v)
            out["cashflow"][row_name] = vals
except Exception as e:
    out["cashflow_error"] = str(e)

with open("/home/chino/thesignal/tmp/brk_research.json", "w") as f:
    json.dump(out, f, indent=2, default=str)

print("SAVED OK")
print("last_close:", out["history"]["last_close"])
print("market_cap:", out["info"].get("marketCap"))
print("trailingPE:", out["info"].get("trailingPE"))
print("bookValue:", out["info"].get("bookValue"))
print("priceToBook:", out["info"].get("priceToBook"))
print("totalRevenue:", out["info"].get("totalRevenue"))
print("totalCash:", out["info"].get("totalCash"))
print("52w range:", out["info"].get("fiftyTwoWeekLow"), "-", out["info"].get("fiftyTwoWeekHigh"))
