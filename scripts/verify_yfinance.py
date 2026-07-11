#!/usr/bin/env python3
"""Verify article claims against live yfinance data."""

import yfinance as yf
import json, os

tickers = {
    'CRDO': {'article_price': 268.00, 'fiscal_year_end': 'May'},  # FY2026 ends May
    'SMCI': {'article_price': 28.17, 'fiscal_year_end': 'June'},
    'VRT':  {'article_price_q1': 327.25, 'article_price': 316.65},
    'COIN': {'article_price': 163.51},
    'CRWV': {'article_price': 85.00, 'fiscal_year_end': 'Dec'},
    'KTOS': {'article_price': 50.34},
    'AXON': {'article_price': 622.35},
    'AMAT': {'article_price': 534.71, 'fiscal_year_end': 'Oct'},
    'NOW':  {'article_price': 112.99},
}

for sym, meta in tickers.items():
    print(f"\n{'='*70}")
    print(f"  {sym}")
    print(f"{'='*70}")
    try:
        t = yf.Ticker(sym)
        info = t.info
        
        price = info.get('currentPrice') or info.get('previousClose') or info.get('regularMarketPrice', 'N/A')
        print(f"  Current Price:          {price}")
        print(f"  Article Price:          {meta.get('article_price', 'N/A')}")
        
        high52 = info.get('fiftyTwoWeekHigh', 'N/A')
        print(f"  52-Week High:           {high52}")
        
        low52 = info.get('fiftyTwoWeekLow', 'N/A')
        print(f"  52-Week Low:            {low52}")
        
        market_cap = info.get('marketCap', 'N/A')
        if market_cap != 'N/A':
            print(f"  Market Cap:             ${market_cap/1e9:.2f}B")
        
        trailing_pe = info.get('trailingPE', 'N/A')
        forward_pe = info.get('forwardPE', 'N/A')
        print(f"  Trailing P/E:           {trailing_pe}")
        print(f"  Forward P/E:            {forward_pe}")
        
        rev = info.get('totalRevenue', 'N/A')
        if rev != 'N/A':
            print(f"  Total Revenue:          ${rev/1e9:.2f}B")
        
        gross_margin = info.get('grossMargins', 'N/A')
        if gross_margin != 'N/A':
            print(f"  Gross Margin:           {gross_margin*100:.1f}%")
        
        op_margin = info.get('operatingMargins', 'N/A')
        if op_margin != 'N/A':
            print(f"  Operating Margin:       {op_margin*100:.1f}%")
        
        profit_margin = info.get('profitMargins', 'N/A')
        if profit_margin != 'N/A':
            print(f"  Profit Margin:          {profit_margin*100:.1f}%")
        
        ytd_change = info.get('ytdReturn', 'N/A')
        print(f"  YTD Return:             {ytd_change}")
        
        short_ratio = info.get('shortRatio', 'N/A')
        short_pct = info.get('shortPercentOfFloat', 'N/A')
        print(f"  Short % Float:          {short_pct}")
        
        debt = info.get('totalDebt', 'N/A')
        cash = info.get('totalCash', 'N/A')
        if debt != 'N/A' and cash != 'N/A':
            print(f"  Total Cash:             ${cash/1e9:.2f}B")
            print(f"  Total Debt:             ${debt/1e9:.2f}B")
        
        free_cf = info.get('freeCashflow', 'N/A')
        if free_cf != 'N/A':
            print(f"  Free Cash Flow:         ${free_cf/1e9:.2f}B")
        
        print(f"  Sector:                 {info.get('sector', 'N/A')}")
        print(f"  Industry:               {info.get('industry', 'N/A')}")
        
        # Check if article price is close to actual
        actual_price = price
        article_price = meta.get('article_price', 0)
        if actual_price and article_price:
            diff_pct = abs(actual_price - article_price) / max(actual_price, article_price) * 100
            if diff_pct > 3:
                print(f"  ⚠️ PRICE MISMATCH: Article says ${article_price}, actual ${actual_price} ({diff_pct:.1f}% off)")
            else:
                print(f"  ✓ Price within {diff_pct:.1f}% of current")
                
        # Verify 52-week high claim
        if high52 != 'N/A' and actual_price:
            pct_from_high = (high52 - actual_price) / high52 * 100
            print(f"  % from 52wk high:       {pct_from_high:.1f}%")
                
    except Exception as e:
        print(f"  ERROR: {e}")
