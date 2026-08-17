#!/usr/bin/env python3
"""Pull ZS + competitor financials via yfinance for deep research brief."""
import json, sys
import yfinance as yf

TICKERS = ["ZS", "PANW", "FTNT", "CRWD", "NET"]
out = {}

for t in TICKERS:
    try:
        tk = yf.Ticker(t)
        info = tk.info or {}
        fin = tk.financials          # annual income statement
        qfin = tk.quarterly_financials
        bs = tk.balance_sheet
        cf = tk.cashflow
        qcf = tk.quarterly_cashflow

        def g(df, row, col_idx=0):
            try:
                v = df.loc[row]
                vals = [x for x in v.values if x == x]  # drop NaN
                return vals[col_idx] if vals else None
            except Exception:
                return None

        def rev_history(df):
            """Return list of (period_end_label, revenue) for last N periods."""
            try:
                row = df.loc["Total Revenue"] if "Total Revenue" in df.index else df.loc["Operating Revenue"]
                items = list(row.items())
                return [(str(k.date()), float(v)) for k, v in items[:6] if v == v]
            except Exception as e:
                return [("ERR", str(e))]

        out[t] = {
            "name": info.get("shortName") or info.get("longName"),
            "price": info.get("currentPrice") or info.get("regularMarketPrice"),
            "marketCap": info.get("marketCap"),
            "enterpriseValue": info.get("enterpriseValue"),
            "trailingPE": info.get("trailingPE"),
            "forwardPE": info.get("forwardPE"),
            "priceToSalesTrailing12Months": info.get("priceToSalesTrailing12Months"),
            "EVToRevenue": info.get("enterpriseToRevenue"),
            "EVToEBITDA": info.get("enterpriseToEbitda"),
            "grossMargins": info.get("grossMargins"),
            "operatingMargins": info.get("operatingMargins"),
            "profitMargins": info.get("profitMargins"),
            "totalCash": info.get("totalCash"),
            "totalDebt": info.get("totalDebt"),
            "totalCashPerShare": info.get("totalCashPerShare"),
            "freeCashflow": info.get("freeCashflow"),
            "operatingCashflow": info.get("operatingCashflow"),
            "sharesOutstanding": info.get("sharesOutstanding"),
            "floatShares": info.get("floatShares"),
            "shortPercentOfFloat": info.get("shortPercentOfFloat"),
            "beta": info.get("beta"),
            "52WeekChange": info.get("52WeekChange"),
            "recommendationMean": info.get("recommendationMean"),
            "numberOfAnalystOpinions": info.get("numberOfAnalystOpinions"),
            "targetMeanPrice": info.get("targetMeanPrice"),
            "targetHighPrice": info.get("targetHighPrice"),
            "targetLowPrice": info.get("targetLowPrice"),
            "annualRevenueHistory": rev_history(fin),
            "quarterlyRevenueHistory": rev_history(qfin),
            "ttmRevenue": info.get("totalRevenue"),
            "ttmGrossProfit": info.get("grossProfit"),
            "ttmNetIncome": info.get("netIncomeToCommon"),
        }
    except Exception as e:
        out[t] = {"ERROR": str(e)}

print(json.dumps(out, indent=2, default=str))
