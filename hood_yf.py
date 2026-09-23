#!/usr/bin/env python3
"""yfinance data pull for HOOD — research brief for hood-tokenized-stocks-2026."""
import json, sys
import yfinance as yf

t = yf.Ticker("HOOD")
info = t.info

out = {}

# --- price history (last 10 sessions) ---
hist = t.history(period="10d")
out["history"] = {str(k.date()): {"open": float(v["Open"]), "high": float(v["High"]),
                                   "low": float(v["Low"]), "close": float(v["Close"]),
                                   "volume": int(v["Volume"])}
                  for k, v in hist.iterrows()}

# --- info fields ---
keys = ["sector", "industry", "marketCap", "totalRevenue", "revenueGrowth",
        "forwardPE", "trailingPE", "freeCashflow", "totalCash", "totalCashPerShare",
        "totalDebt", "fiftyTwoWeekHigh", "fiftyTwoWeekLow", "fiftyTwoWeekChange",
        "recommendationKey", "targetMeanPrice", "targetHighPrice", "targetLowPrice",
        "sharesOutstanding", "sharesShort", "shortPercentOfFloat", "beta",
        "currentPrice", "previousClose", "regularMarketPrice", "regularMarketPreviousClose",
        "earningsGrowth", "profitMargins", "operatingMargins", "grossMargins",
        "enterpriseValue", "priceToBook", "pegRatio", "dividendYield",
        "longName", "website", "exchange", "currency", "financialCurrency",
        "numberOfAnalystOpinions", "totalCash"]
for k in keys:
    v = info.get(k)
    if v is not None:
        out[k] = v

# --- quarterly cash flow (for FCF fallback) ---
try:
    qcf = t.quarterly_cashflow
    qcf_rows = {}
    for col in qcf.columns:
        qcf_rows[str(col.date())] = {k: (None if v is None else float(v)) for k, v in qcf[col].items()}
    out["quarterly_cashflow"] = qcf_rows
except Exception as e:
    out["quarterly_cashflow_error"] = str(e)

# --- quarterly income statement (revenue TTM cross-check) ---
try:
    qi = t.quarterly_income_stmt
    qi_rows = {}
    for col in qi.columns:
        qi_rows[str(col.date())] = {k: (None if v is None else float(v)) for k, v in qi[col].items()}
    out["quarterly_income"] = qi_rows
except Exception as e:
    out["quarterly_income_error"] = str(e)

print(json.dumps(out, indent=1, default=str))
