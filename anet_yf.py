#!/usr/bin/env python3
"""Pull ANET fundamentals from yfinance for Signal research."""
import json, warnings
warnings.filterwarnings("ignore")
import yfinance as yf

t = yf.Ticker("ANET")
info = t.info

def g(*keys):
    for k in keys:
        if k in info and info[k] is not None:
            return info[k]
    return None

out = {
    "ticker": g("symbol", "ticker"),
    "shortName": g("shortName"),
    "longName": g("longName"),
    "sector": g("sector"),
    "industry": g("industry"),
    "lastClose": g("regularMarketPrice", "previousClose", "currentPrice"),
    "prevClose": g("previousClose"),
    "marketCap": g("marketCap"),
    "enterpriseValue": g("enterpriseValue"),
    "trailingPE": g("trailingPE"),
    "forwardPE": g("forwardPE"),
    "peRatioTTM": g("peRatio"),
    "epsTrailing": g("trailingEps"),
    "epsForward": g("forwardEps"),
    "revenueTTM": g("totalRevenue"),
    "revenueGrowth": g("revenueGrowth"),
    "grossMargins": g("grossMargins"),
    "operatingMargins": g("operatingMargins"),
    "profitMargins": g("profitMargins"),
    "freeCashflow": g("freeCashflow"),
    "operatingCashflow": g("operatingCashflow"),
    "totalDebt": g("totalDebt"),
    "totalCash": g("totalCash"),
    "netDebt": g("netDebt"),
    "debtToEquity": g("debtToEquity"),
    "totalCashPerShare": g("totalCashPerShare"),
    "currentRatio": g("currentRatio"),
    "quickRatio": g("quickRatio"),
    "returnOnEquity": g("returnOnEquity"),
    "returnOnAssets": g("returnOnAssets"),
    "beta": g("beta"),
    "fiftyTwoWeekHigh": g("fiftyTwoWeekHigh"),
    "fiftyTwoWeekLow": g("fiftyTwoWeekLow"),
    "targetMeanPrice": g("targetMeanPrice"),
    "targetHighPrice": g("targetHighPrice"),
    "targetLowPrice": g("targetLowPrice"),
    "recommendationKey": g("recommendationKey"),
    "numberOfAnalystOpinions": g("numberOfAnalystOpinions"),
    "earningsDate": g("earningsDate"),
    "exchange": g("exchange"),
    "currency": g("currency"),
    "quoteType": g("quoteType"),
}
print(json.dumps(out, indent=2, default=str))

# Quarterly financials
print("\n=== QUARTERLY INCOME (last 6q) ===")
try:
    qf = t.quarterly_income_stmt
    cols = qf.columns[:6]
    for c in cols:
        print(f"\n--- {c.date()} ---")
        for idx in ["Total Revenue", "Gross Profit", "Operating Income", "Net Income", "Diluted EPS", "Research And Development", "Operating Expense"]:
            if idx in qf.index:
                v = qf.loc[idx, c]
                print(f"  {idx}: {v}")
except Exception as e:
    print("ERR", e)

print("\n=== BALANCE SHEET (annual, latest) ===")
try:
    bs = t.balance_sheet
    c = bs.columns[0]
    print(f"--- {c.date()} ---")
    for idx in ["Total Debt", "Cash And Cash Equivalents", "Current Debt", "Long Term Debt", "Total Assets", "Stockholders Equity"]:
        if idx in bs.index:
            print(f"  {idx}: {bs.loc[idx, c]}")
except Exception as e:
    print("ERR", e)

print("\n=== CASHFLOW (annual, latest) ===")
try:
    cf = t.cashflow
    c = cf.columns[0]
    print(f"--- {c.date()} ---")
    for idx in ["Operating Cash Flow", "Free Cash Flow", "Capital Expenditure"]:
        if idx in cf.index:
            print(f"  {idx}: {cf.loc[idx, c]}")
except Exception as e:
    print("ERR", e)
