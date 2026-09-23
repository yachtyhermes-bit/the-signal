#!/usr/bin/env python3
"""Research data pull for QBTS (D-Wave Quantum) — The Signal research brief. v2 resilient."""
import json
import datetime
import yfinance as yf

OUT = {}

def clean(obj):
    """Convert dict keys to str, datetimes to iso, keep floats/ints."""
    if isinstance(obj, dict):
        return {str(k): clean(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [clean(v) for v in obj]
    if isinstance(obj, (datetime.date, datetime.datetime)):
        return obj.isoformat()
    if isinstance(obj, float) and (obj != obj):  # NaN
        return None
    return obj

t = yf.Ticker("QBTS")

# --- Quote / fast stats ---
try:
    fi = t.fast_info
    OUT["fast_info"] = {
        "last_price": fi.last_price,
        "previous_close": fi.previous_close,
        "market_cap": fi.market_cap,
        "year_high": fi.year_high,
        "year_low": fi.year_low,
        "currency": getattr(fi, "currency", None),
        "exchange": getattr(fi, "exchange", None),
        "shares": getattr(fi, "shares", None),
    }
except Exception as e:
    OUT["fast_info_error"] = str(e)

try:
    info = t.info
    keys = [
        "currentPrice", "regularMarketPrice", "previousClose", "marketCap",
        "sharesOutstanding", "floatShares", "trailingPE", "forwardPE",
        "trailingEps", "forwardEps", "totalRevenue", "revenueGrowth",
        "totalCash", "totalDebt", "totalCashPerShare", "debtToEquity",
        "fiftyTwoWeekLow", "fiftyTwoWeekHigh", "fiftyTwoWeekChange",
        "recommendationKey", "recommendationMean", "targetMeanPrice",
        "targetHighPrice", "targetLowPrice", "numberOfAnalystOpinions",
        "grossMargins", "operatingMargins", "profitMargins", "enterpriseValue",
        "bookValue", "priceToBook", "beta", "shortPercentOfFloat",
        "heldPercentInstitutions", "industry", "sector", "longName",
        "website", "address1", "city", "country", "exchange", "currency",
        "earningsQuarterlyGrowth", "operatingCashflow", "freeCashflow",
    ]
    OUT["info"] = {k: info.get(k) for k in keys}
except Exception as e:
    OUT["info_error"] = str(e)

# --- Income statement (annual + quarterly) ---
for name, fn in [
    ("income_stmt_annual", lambda: t.income_stmt),
    ("income_stmt_quarterly", lambda: t.quarterly_income_stmt),
    ("balance_sheet_annual", lambda: t.balance_sheet),
    ("cashflow_quarterly", lambda: t.quarterly_cashflow),
    ("cashflow_annual", lambda: t.cashflow),
]:
    try:
        df = fn()
        if df is not None and not df.empty:
            OUT[name] = clean(df.to_dict())
        else:
            OUT[name] = None
    except Exception as e:
        OUT[name + "_error"] = str(e)

# --- Price history (last ~6 months) ---
try:
    hist = t.history(period="6mo", interval="1d")
    if len(hist):
        first = hist.iloc[0]
        last = hist.iloc[-1]
        OUT["price_history_6mo"] = {
            "start_date": str(hist.index[0].date()),
            "end_date": str(hist.index[-1].date()),
            "start_close": float(first["Close"]),
            "end_close": float(last["Close"]),
            "pct_change_6mo": float((last["Close"] / first["Close"] - 1) * 100),
            "high_6mo": float(hist["High"].max()),
            "low_6mo": float(hist["Low"].min()),
            "n_days": int(len(hist)),
        }
        monthly = hist["Close"].resample("ME").last()
        OUT["price_history_monthly_closes"] = {
            str(k.date()): float(v) for k, v in monthly.items()
        }
        # last 10 daily closes for recent trend
        OUT["price_history_last10"] = [
            {"date": str(i.date()), "close": float(r["Close"]), "open": float(r["Open"])}
            for i, r in hist.tail(10).iterrows()
        ]
except Exception as e:
    OUT["price_history_error"] = str(e)

# --- Analysts ---
try:
    rec = t.recommendations
    if rec is not None and len(rec):
        OUT["recommendations_last"] = clean(rec.tail(10).to_dict())
except Exception as e:
    OUT["recommendations_error"] = str(e)

try:
    su = t.sustainability
    OUT["sustainability"] = clean(su.to_dict()) if su is not None else None
except Exception as e:
    OUT["sustainability_error"] = str(e)

with open("/home/chino/thesignal/qbts_yf_out.json", "w") as f:
    json.dump(clean(OUT), f, indent=2, default=str)

print("DONE")
print("FAST_INFO:", json.dumps(OUT.get("fast_info", {}), indent=2, default=str))
print("INFO:", json.dumps(OUT.get("info", {}), indent=2, default=str)[:2000])
print("PRICE HIST:", json.dumps(OUT.get("price_history_6mo", {}), indent=2, default=str))
print("LAST10:", json.dumps(OUT.get("price_history_last10", []), indent=2, default=str))
