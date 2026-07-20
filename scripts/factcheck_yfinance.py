#!/usr/bin/env python3
"""Verify key financial claims for fact-checking 5 articles."""
import yfinance as yf
import json

tickers = ['GE', 'TSM', 'SHOP', 'HOOD', 'RTX']

for ticker in tickers:
    t = yf.Ticker(ticker)
    info = t.info
    price = info.get('currentPrice') or info.get('regularMarketPrice') or info.get('previousClose')
    
    print(f"\n=== {ticker} ===")
    print(f"Price: ${price}")
    print(f"Market Cap: ${info.get('marketCap', 0)/1e9:.1f}B")
    print(f"Forward PE: {info.get('forwardPE', 'N/A')}")
    print(f"Trailing PE: {info.get('trailingPE', 'N/A')}")
    print(f"ROE: {info.get('returnOnEquity', 'N/A')}")
    print(f"Revenue Growth: {info.get('revenueGrowth', 'N/A')}")
    print(f"Op Margin: {info.get('operatingMargins', 'N/A')}")
    print(f"Profit Margin: {info.get('profitMargins', 'N/A')}")
    print(f"Debt/Equity: {info.get('debtToEquity', 'N/A')}")
    print(f"Total Cash: ${info.get('totalCash', 0)/1e9:.1f}B")
    print(f"Total Debt: ${info.get('totalDebt', 0)/1e9:.1f}B")
    print(f"52W High: ${info.get('fiftyTwoWeekHigh', 'N/A')}")
    print(f"52W Low: ${info.get('fiftyTwoWeekLow', 'N/A')}")
    print(f"FCF (info): ${info.get('freeCashflow', 0)/1e9:.2f}B")
    print(f"Revenue TTM: ${info.get('totalRevenue', 0)/1e9:.1f}B")
    print(f"Gross Margins: {info.get('grossMargins', 'N/A')}")
    print(f"Recommendation: {info.get('recommendationKey', 'N/A')}")
    print(f"Target Mean: ${info.get('targetMeanPrice', 'N/A')}")
    print(f"Target High: ${info.get('targetHighPrice', 'N/A')}")
    print(f"Target Low: ${info.get('targetLowPrice', 'N/A')}")
    print(f"# Analyst Opinions: {info.get('numberOfAnalystOpinions', 'N/A')}")
    print(f"EPS (trailing): {info.get('trailingEps', 'N/A')}")
    
    # Get quarterly data for deeper checks
    try:
        q_is = t.quarterly_financials
        if q_is is not None and not q_is.empty:
            print("\n-- Quarterly Financials (last 4 quarters) --")
            cols = q_is.columns[:4]
            for col in cols:
                print(f"  {col.strftime('%Y-%m-%d') if hasattr(col, 'strftime') else col}")
            if 'Total Revenue' in q_is.index:
                revs = q_is.loc['Total Revenue'].iloc[:4]
                print(f"  Quarterly Revs: {[f'${v/1e9:.2f}B' for v in revs]}")
                print(f"  TTM Revenue: ${revs.sum()/1e9:.1f}B")
            if 'Net Income' in q_is.index:
                nis = q_is.loc['Net Income'].iloc[:4]
                print(f"  TTM Net Income: ${nis.sum()/1e9:.2f}B")
    except Exception as e:
        print(f"  Q Financials error: {e}")
    
    # Annual income statement
    try:
        is_stmt = t.income_stmt
        if is_stmt is not None and not is_stmt.empty:
            print("\n-- Annual Income Statement --")
            cols = is_stmt.columns[:3]
            for col in cols:
                print(f"  {col.strftime('%Y') if hasattr(col, 'strftime') else col}")
            if 'Total Revenue' in is_stmt.index:
                for col in cols:
                    v = is_stmt.loc['Total Revenue', col]
                    print(f"  Revenue: ${v/1e9:.2f}B")
            if 'Net Income' in is_stmt.index:
                for col in cols:
                    v = is_stmt.loc['Net Income', col]
                    print(f"  Net Income: ${v/1e9:.2f}B")
    except Exception as e:
        print(f"  Income stmt error: {e}")
    
    # Cash flow for FCF verification
    try:
        q_cf = t.quarterly_cashflow
        if q_cf is not None and not q_cf.empty:
            print("\n-- Quarterly Cash Flow (last 4 quarters) --")
            if 'Free Cash Flow' in q_cf.index:
                fcf = q_cf.loc['Free Cash Flow'].iloc[:4]
                print(f"  TTM FCF: ${fcf.sum()/1e9:.2f}B")
            if 'Operating Cash Flow' in q_cf.index:
                ocf = q_cf.loc['Operating Cash Flow'].iloc[:4]
                print(f"  TTM OCF: ${ocf.sum()/1e9:.2f}B")
            if 'Capital Expenditure' in q_cf.index:
                capex = q_cf.loc['Capital Expenditure'].iloc[:4]
                print(f"  TTM Capex: ${capex.sum()/1e9:.2f}B")
    except Exception as e:
        print(f"  Cash flow error: {e}")
    
    # Earnings history - check recent beats
    try:
        ed = t.earnings_dates
        if ed is not None and not ed.empty:
            print(f"\n-- Recent Earnings Dates (last 3) --")
            for idx, row in ed.head(3).iterrows():
                est = row.get('EPS Estimate', 'N/A')
                actual = row.get('EPS Actual', 'N/A')
                print(f"  {idx.strftime('%Y-%m-%d') if hasattr(idx, 'strftime') else idx}: Est={est}, Actual={actual}")
    except Exception as e:
        print(f"  Earnings dates error: {e}")
