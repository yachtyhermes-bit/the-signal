import yfinance as yf, json, math, datetime

t = yf.Ticker("CDNS")
out = {}

def safe(fn, label):
    try:
        return fn()
    except Exception as e:
        return f"ERR {label}: {e}"

info = t.info
keys = ["currentPrice","previousClose","regularMarketPrice","regularMarketChangePercent",
        "marketCap","sharesOutstanding","impliedSharesOutstanding","trailingPE","forwardPE",
        "trailingEps","forwardEps","totalRevenue","grossMargins","operatingMargins",
        "profitMargins","totalDebt","totalCash","freeCashflow","operatingCashflow",
        "fiftyTwoWeekHigh","fiftyTwoWeekLow","recommendationKey","recommendationMean",
        "numberOfAnalystOpinions","targetMeanPrice","targetHighPrice","targetLowPrice",
        "currentRatio","returnOnEquity","beta","enterpriseValue","revenueGrowth","earningsGrowth"]
out["info"] = {k: info.get(k) for k in keys}

# quarterly income statement
try:
    qf = t.quarterly_income_stmt
    out["q_income_cols"] = [str(c.date()) for c in qf.columns]
    for row in ["Total Revenue","Gross Profit","Operating Income","Net Income","Diluted EPS","Basic EPS"]:
        if row in qf.index:
            out.setdefault("q_income", {})[row] = [None if (isinstance(v,float) and math.isnan(v)) else float(v) for v in qf.loc[row].tolist()]
except Exception as e:
    out["q_income_err"] = str(e)

try:
    qc = t.quarterly_cashflow
    out["q_cf_cols"] = [str(c.date()) for c in qc.columns]
    for row in ["Operating Cash Flow","Capital Expenditure","Free Cash Flow"]:
        if row in qc.index:
            out.setdefault("q_cf", {})[row] = [None if (isinstance(v,float) and math.isnan(v)) else float(v) for v in qc.loc[row].tolist()]
except Exception as e:
    out["q_cf_err"] = str(e)

try:
    qb = t.quarterly_balance_sheet
    out["q_bs_cols"] = [str(c.date()) for c in qb.columns]
    for row in ["Cash And Cash Equivalents","Cash Cash Equivalents And Short Term Investments","Total Debt","Long Term Debt","Current Debt"]:
        if row in qb.index:
            out.setdefault("q_bs", {})[row] = [None if (isinstance(v,float) and math.isnan(v)) else float(v) for v in qb.loc[row].tolist()]
except Exception as e:
    out["q_bs_err"] = str(e)

# price history
h = t.history(start="2026-09-01", end="2026-10-28", auto_adjust=False)
rows = []
for idx, r in h.iterrows():
    rows.append({"date": str(idx.date()), "open": round(float(r["Open"]),2), "high": round(float(r["High"]),2),
                 "low": round(float(r["Low"]),2), "close": round(float(r["Close"]),2),
                 "adj": round(float(r["Adj Close"]),2), "vol": int(r["Volume"])})
out["hist"] = rows

# 52 week from Oct 27 2025
h52 = t.history(start="2025-10-27", end="2026-10-28", auto_adjust=False)
cl = h52["Close"]
out["52w"] = {"start": str(cl.index[0].date()), "end": str(cl.index[-1].date()),
              "high_close": round(float(cl.max()),2), "high_close_date": str(cl.idxmax().date()),
              "low_close": round(float(cl.min()),2), "low_close_date": str(cl.idxmin().date()),
              "intraday_high": round(float(h52["High"].max()),2), "intraday_low": round(float(h52["Low"].min()),2),
              "n": len(cl)}

# analyst targets
try:
    out["analyst_price_targets"] = t.analyst_price_targets
except Exception as e:
    out["apt_err"] = str(e)

print(json.dumps(out, indent=1, default=str))
