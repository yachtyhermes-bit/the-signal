#!/usr/bin/env python3
"""Fact-check prices and key financials for 5 most recent articles."""
import json, sys

articles_info = [
    ('ge-aftermarket-moat-2026', 'GE', 348.83),
    ('coreweave-ai-factory-moat-2026', 'CRWV', 73.21),
    ('panw-ai-security-cash-flow-machine-2026', 'PANW', 359.39),
    ('net-cloudflare-precursor-agentic-internet-2026', 'NET', 277.66),
    ('arm-agi-cpu-custom-silicon-bet-2026', 'ARM', 267),
]

import yfinance as yf

for slug, ticker, article_price in articles_info:
    print(f'=== {slug} ({ticker}) ===')
    with open(f'articles/posts/{slug}.json') as f:
        article = json.load(f)
    
    t = yf.Ticker(ticker)
    info = t.info
    
    live_price = info.get('currentPrice') or info.get('previousClose') or info.get('regularMarketPrice')
    mcap = info.get('marketCap')
    high52 = info.get('fiftyTwoWeekHigh')
    fpe = info.get('forwardPE')
    
    print(f'  Article price: ${article_price}')
    print(f'  Live price:    ${live_price}')
    if live_price:
        pct_diff = abs(live_price - article_price) / article_price * 100
        print(f'  Diff:          {pct_diff:.1f}%')
        if pct_diff > 5:
            print(f'  ⚠️ SIGNIFICANT mismatch (>5%)')
        elif pct_diff > 2:
            print(f'  ⚠️ Minor drift >2%')
        else:
            print(f'  ✅ Price in range')
    
    print(f'  Market cap:    ${mcap/1e9:.1f}B' if mcap else '  Market cap: N/A')
    print(f'  52-week high:  ${high52}')
    print(f'  Forward P/E:   {fpe}')
    
    # Check revenue if available
    try:
        inc = t.income_stmt
        if inc is not None and 'Total Revenue' in inc.index:
            rev_cols = inc.loc['Total Revenue'].dropna()
            if len(rev_cols) > 0:
                latest_rev = rev_cols.iloc[0]
                print(f'  Latest annual rev: ${latest_rev/1e9:.2f}B')
    except:
        pass
    
    # Check TTM FCF from quarterly cashflow
    try:
        q_cf = t.quarterly_cashflow
        if q_cf is not None and 'Free Cash Flow' in q_cf.index:
            ttm_fcf = q_cf.loc['Free Cash Flow'].iloc[0:4].sum()
            print(f'  TTM FCF: ${ttm_fcf/1e9:.2f}B')
        elif q_cf is not None and 'Operating Cash Flow' in q_cf.index and 'Capital Expenditure' in q_cf.index:
            ttm_ocf = q_cf.loc['Operating Cash Flow'].iloc[0:4].sum()
            ttm_capex = q_cf.loc['Capital Expenditure'].iloc[0:4].sum()
            ttm_fcf = ttm_ocf + ttm_capex
            print(f'  TTM FCF (calc): ${ttm_fcf/1e9:.2f}B')
    except:
        pass
    
    # Check net income / EPS
    try:
        ni = info.get('netIncomeToCommon')
        if ni:
            print(f'  Net income: ${ni/1e9:.2f}B')
        eps = info.get('trailingEps')
        if eps:
            print(f'  Trailing EPS: ${eps}')
    except:
        pass
    
    # Check gross margin / profit margin
    try:
        gm = info.get('grossMargins')
        pm = info.get('profitMargins')
        if gm: print(f'  Gross margin: {gm*100:.1f}%')
        if pm: print(f'  Profit margin: {pm*100:.1f}%')
    except:
        pass
    
    print()
