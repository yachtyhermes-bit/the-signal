#!/usr/bin/env python3
"""Cloudflare (NET) financial research script for The Signal."""
import yfinance as yf
import json

ticker = yf.Ticker("NET")

# Get financials
info = ticker.info

# Get balance sheet for debt/cash
try:
    bs = ticker.balance_sheet
    total_debt = None
    cash = None
    if bs is not None and not bs.empty:
        # Total Debt = Long Term Debt + Current Debt
        if 'Total Debt' in bs.index:
            total_debt = bs.loc['Total Debt'].iloc[0]
        elif 'Long Term Debt' in bs.index:
            long_debt = bs.loc['Long Term Debt'].iloc[0]
            current_debt = 0
            if 'Current Debt' in bs.index:
                current_debt = bs.loc['Current Debt'].iloc[0]
            elif 'Short Long Term Debt' in bs.index:
                current_debt = bs.loc['Short Long Term Debt'].iloc[0]
            total_debt = long_debt + current_debt
        
        if 'Cash' in bs.index:
            cash = bs.loc['Cash'].iloc[0]
        elif 'Cash And Cash Equivalents' in bs.index:
            cash = bs.loc['Cash And Cash Equivalents'].iloc[0]
except Exception as e:
    print(f"Balance sheet error: {e}")

# Get income statement for revenue TTM
try:
    inc = ticker.income_stmt
    revenue_ttm = None
    if inc is not None and not inc.empty:
        if 'Total Revenue' in inc.index:
            # Sum last 4 quarters
            revs = inc.loc['Total Revenue']
            if len(revs) >= 4:
                revenue_ttm = revs.iloc[:4].sum()
            elif len(revs) > 0:
                revenue_ttm = revs.iloc[0]
except Exception as e:
    print(f"Income statement error: {e}")

# Get cash flow for FCF
try:
    cf = ticker.cashflow
    fcf_ttm = None
    if cf is not None and not cf.empty:
        if 'Free Cash Flow' in cf.index:
            fcfs = cf.loc['Free Cash Flow']
            if len(fcfs) >= 4:
                fcf_ttm = fcfs.iloc[:4].sum()
            elif len(fcfs) > 0:
                fcf_ttm = fcfs.iloc[0]
        elif 'Operating Cash Flow' in cf.index and 'Capital Expenditure' in cf.index:
            ocf = cf.loc['Operating Cash Flow']
            capex = cf.loc['Capital Expenditure']
            fcf_ttm = ocf.iloc[0] + capex.iloc[0] if len(ocf) > 0 and len(capex) > 0 else None
except Exception as e:
    print(f"Cash flow error: {e}")

# Calculate 5-year revenue CAGR if possible
try:
    if inc is not None and not inc.empty and 'Total Revenue' in inc.index:
        revs = inc.loc['Total Revenue']
        annual_revs = [r for r in revs if r == r]  # filter NaN
        if len(annual_revs) >= 5:
            rev_5yr_ago = annual_revs[-1]
            rev_recent = annual_revs[0]
            if rev_5yr_ago > 0:
                cagr = (rev_recent / rev_5yr_ago) ** (1/5) - 1
            else:
                cagr = None
        else:
            cagr = None
    else:
        cagr = None
except Exception as e:
    print(f"CAGR error: {e}")
    cagr = None

# Build output
result = {
    "ticker": info.get("symbol", "NET"),
    "shortName": info.get("shortName"),
    "currentPrice": info.get("currentPrice"),
    "previousClose": info.get("previousClose"),
    "revenueTTM": revenue_ttm if revenue_ttm else info.get("totalRevenue"),
    "trailingPE": info.get("trailingPE"),
    "forwardPE": info.get("forwardPE"),
    "freeCashFlowTTM": fcf_ttm if fcf_ttm else info.get("freeCashflow"),
    "totalDebt": total_debt if total_debt else info.get("totalDebt"),
    "cashAndEquivalents": cash if cash else info.get("totalCash"),
    "marketCap": info.get("marketCap"),
    "enterpriseValue": info.get("enterpriseValue"),
    "grossMargins": info.get("grossMargins"),
    "grossProfit": info.get("grossProfit"),
    "sector": info.get("sector"),
    "industry": info.get("industry"),
    "industryKey": info.get("industryKey"),
    "sectorKey": info.get("sectorKey"),
    "businessSummary": info.get("longBusinessSummary"),
    "revenueGrowth": info.get("revenueGrowth"),
    "earningsGrowth": info.get("earningsGrowth"),
    "operatingMargins": info.get("operatingMargins"),
    "profitMargins": info.get("profitMargins"),
    "returnOnEquity": info.get("returnOnEquity"),
    "returnOnAssets": info.get("returnOnAssets"),
    "debtToEquity": info.get("debtToEquity"),
    "currentRatio": info.get("currentRatio"),
    "quickRatio": info.get("quickRatio"),
    "dividendYield": info.get("dividendYield"),
    "payoutRatio": info.get("payoutRatio"),
    "beta": info.get("beta"),
    "fiftyTwoWeekHigh": info.get("fiftyTwoWeekHigh"),
    "fiftyTwoWeekLow": info.get("fiftyTwoWeekLow"),
    "fiftyDayAverage": info.get("fiftyDayAverage"),
    "twoHundredDayAverage": info.get("twoHundredDayAverage"),
    "averageVolume": info.get("averageVolume"),
    "recommendationMean": info.get("recommendationMean"),
    "numberOfAnalystOpinions": info.get("numberOfAnalystOpinions"),
    "targetMeanPrice": info.get("targetMeanPrice"),
    "targetHighPrice": info.get("targetHighPrice"),
    "targetLowPrice": info.get("targetLowPrice"),
    # Revenue CAGR estimated
    "revenueCagr5yr": cagr,
    "website": info.get("website"),
    "city": info.get("city"),
    "state": info.get("state"),
    "country": info.get("country"),
    "employees": info.get("fullTimeEmployees"),
    "foundedYear": info.get("foundedYear"),
    "ipoDate": info.get("ipoDate"),
}

print(json.dumps(result, indent=2, default=str))
