#!/usr/bin/env python3
"""Pull MPWR data from yfinance for The Signal article research."""
import json
import yfinance as yf

t = yf.Ticker("MPWR")
info = t.info

def g(*keys):
    for k in keys:
        if k in info and info[k] is not None:
            return info[k]
    return None

out = {}

# Price data
hist = t.history(period="5d")
out["last_close"] = float(hist["Close"].iloc[-1]) if len(hist) else None
out["last_date"] = str(hist.index[-1].date()) if len(hist) else None
out["prev_close"] = float(hist["Close"].iloc[-2]) if len(hist) > 1 else None
out["day_change_pct"] = round((out["last_close"]/out["prev_close"] - 1) * 100, 2) if out.get("prev_close") else None

# Key stats
out["current_price"] = g("currentPrice", "regularMarketPrice")
out["market_cap"] = g("marketCap")
out["pe_trailing"] = g("trailingPE", "peRatio")
out["pe_forward"] = g("forwardPE")
out["peg"] = g("pegRatio")
out["eps_trailing"] = g("trailingEps")
out["eps_forward"] = g("forwardEps")
out["beta"] = g("beta")
out["target_mean"] = g("targetMeanPrice")
out["target_high"] = g("targetHighPrice")
out["target_low"] = g("targetLowPrice")
out["recommendation"] = g("recommendationKey")
out["num_analysts"] = g("numberOfAnalystOpinions")
out["short_pct_float"] = g("shortPercentOfFloat")
out["shares_outstanding"] = g("sharesOutstanding")
out["float_shares"] = g("floatShares")
out["dividend_yield"] = g("dividendYield")
out["payout_ratio"] = g("payoutRatio")

# Financials
fin = t.financials  # annual income statement
if fin is not None and not fin.empty:
    cols = list(fin.columns)
    out["income_stmt_cols"] = [str(c) for c in cols[:3]]
    for row in ["Total Revenue", "Operating Income", "Net Income", "EBITDA"]:
        if row in fin.index:
            out[f"annual_{row}"] = {str(c): fin.loc[row, c] for c in cols[:3]}

qfin = t.quarterly_financials
if qfin is not None and not qfin.empty:
    qcols = list(qfin.columns)
    out["quarterly_income_cols"] = [str(c) for c in qcols[:4]]
    for row in ["Total Revenue", "Operating Income", "Net Income"]:
        if row in qfin.index:
            out[f"quarterly_{row}"] = {str(c): qfin.loc[row, c] for c in qcols[:4]}

# Balance sheet (debt)
bs = t.balance_sheet
if bs is not None and not bs.empty:
    bcols = list(bs.columns)
    out["bs_cols"] = [str(c) for c in bcols[:3]]
    for row in ["Total Debt", "Cash And Cash Equivalents", "Net Debt", "Stockholders Equity"]:
        if row in bs.index:
            out[f"bs_{row}"] = {str(c): bs.loc[row, c] for c in bcols[:3]}

# Cash flow (FCF)
cf = t.cashflow
if cf is not None and not cf.empty:
    ccols = list(cf.columns)
    out["cf_cols"] = [str(c) for c in ccols[:3]]
    for row in ["Operating Cash Flow", "Capital Expenditure", "Free Cash Flow"]:
        if row in cf.index:
            out[f"cf_{row}"] = {str(c): cf.loc[row, c] for c in ccols[:3]}

# Margins
out["gross_margin"] = g("grossMargins")
out["op_margin"] = g("operatingMargins")
out["profit_margin"] = g("profitMargins")
out["roe"] = g("returnOnEquity")
out["roa"] = g("returnOnAssets")

# Revenue growth
out["revenue_growth"] = g("revenueGrowth")
out["earnings_growth"] = g("earningsGrowth")

# Sector info
out["sector"] = g("sector")
out["industry"] = g("industry")

print(json.dumps(out, indent=2, default=str))
