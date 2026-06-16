#!/usr/bin/env python3
"""Fetch live yfinance data for all 6 Signal Highlight tickers.
Writes data/signal-highlights.json — read by build.js to generate cards.
Run BEFORE build.js so cards reflect current prices."""
import json, os, sys

try:
    import yfinance as yf
except ImportError:
    os.system(f"{sys.executable} -m pip install yfinance -q --break-system-packages")
    import yfinance as yf

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(ROOT, 'data')
os.makedirs(DATA_DIR, exist_ok=True)

TICKERS = ['KTOS', 'CRWV', 'AXON', 'MSFT', 'SOFI', 'ZS', 'NVDA', 'AVGO']

# Stable metadata (names, fair value methodology, analyst breakdowns)
META = {
    'KTOS': {'name': 'Kratos Defense & Security', 'analystConsensus': 'Strong Buy', 'analystBuys': 15, 'analystHolds': 5, 'analystSells': 0},
    'CRWV': {'name': 'CoreWeave Inc.', 'analystConsensus': 'Buy', 'analystBuys': 15, 'analystHolds': 16, 'analystSells': 0},
    'AXON': {'name': 'Axon Enterprise Inc.', 'analystConsensus': 'Strong Buy', 'analystBuys': 12, 'analystHolds': 8, 'analystSells': 0},
    'MSFT': {'name': 'Microsoft Corporation', 'analystConsensus': 'Strong Buy', 'analystBuys': 36, 'analystHolds': 4, 'analystSells': 0},
    'SOFI': {'name': 'SoFi Technologies Inc.', 'analystConsensus': 'Buy', 'analystBuys': 11, 'analystHolds': 7, 'analystSells': 0},
    'ZS':   {'name': 'Zscaler Inc.', 'analystConsensus': 'Strong Buy', 'analystBuys': 24, 'analystHolds': 6, 'analystSells': 0},
    'NVDA': {'name': 'NVIDIA Corporation', 'analystConsensus': 'Strong Buy', 'analystBuys': 49, 'analystHolds': 2, 'analystSells': 1},
    'AVGO': {'name': 'Broadcom Inc.', 'analystConsensus': 'Strong Buy', 'analystBuys': 28, 'analystHolds': 3, 'analystSells': 0},
}

LAST_KNOWN = {
    'KTOS': {'currentPrice': 56.18, 'targetPrice': 111.95, 'revTtm': '$1.42B', 'revGrowth': '+18.5%', 'netIncome': '$29.4M', 'peRatio': '330.5x', 'psRatio': '7.4x'},
    'CRWV': {'currentPrice': 105.49, 'targetPrice': 138.90, 'revTtm': '$6.23B', 'revGrowth': '+167.9%', 'netIncome': '-$1.59B', 'peRatio': 'N/A', 'psRatio': '9.2x'},
    'AXON': {'currentPrice': 482.96, 'targetPrice': 662.04, 'revTtm': '$2.98B', 'revGrowth': '+33.5%', 'netIncome': '$205.99M', 'peRatio': '156.5x', 'psRatio': '10.6x'},
    'MSFT': {'currentPrice': 460.77, 'targetPrice': 560.63, 'revTtm': '$318.27B', 'revGrowth': '+14.9%', 'netIncome': '$125.22B', 'peRatio': '35.2x', 'psRatio': '11.3x'},
    'SOFI': {'currentPrice': 18.62, 'targetPrice': 21.00, 'revTtm': '$3.91B', 'revGrowth': '+38.3%', 'netIncome': '$576.93M', 'peRatio': '58.2x', 'psRatio': '6.8x'},
    'ZS':   {'currentPrice': 154.07, 'targetPrice': 194.46, 'revTtm': '$3.17B', 'revGrowth': '+23.3%', 'netIncome': '-$77.39M', 'peRatio': 'N/A', 'psRatio': '11.5x'},
}

def fmt_b(v):
    if v is None: return 'N/A'
    v = float(v)
    if abs(v) >= 1e12: return f'${v/1e12:.2f}T'
    if abs(v) >= 1e9:  return f'${v/1e9:.2f}B'
    if abs(v) >= 1e6:  return f'${v/1e6:.2f}M'
    return f'${v:,.2f}'

def fetch_one(ticker):
    info = {}
    try:
        t = yf.Ticker(ticker)
        info = t.info or {}
    except Exception as e:
        print(f'  ⚠️  yfinance failed for {ticker}: {e}', file=sys.stderr)

    price = info.get('currentPrice') or info.get('regularMarketPrice')
    prev_close = info.get('regularMarketPreviousClose') or info.get('previousClose')
    change_pct = ((price - prev_close) / prev_close * 100) if price and prev_close else 0
    target = info.get('targetMeanPrice') or info.get('targetMedianPrice')
    revenue = info.get('totalRevenue')
    rev_growth = info.get('revenueGrowth')
    if rev_growth is not None: rev_growth *= 100
    net_income = info.get('netIncomeToCommon')
    pe = info.get('trailingPE')
    ps = info.get('priceToSalesTrailing12Months')

    meta = META[ticker]
    fallback = LAST_KNOWN.get(ticker, {})

    current_price = round(float(price), 2) if price else fallback.get('currentPrice', 0)
    target_price = round(float(target), 2) if target else fallback.get('targetPrice', 0)
    upside = round(((target_price - current_price) / current_price * 100), 1) if current_price and target_price else 0

    return {
        'ticker': ticker,
        'name': meta['name'],
        'currentPrice': current_price,
        'changePercent': round(float(change_pct), 2),
        'changeDirection': 'up' if change_pct >= 0 else 'down',
        'fairValue': {
            'status': 'Undervalued' if upside > 5 else ('Overvalued' if upside < -5 else 'Fairly Valued'),
            'price': target_price,
            'upside': f'+{upside}%' if upside >= 0 else f'{upside}%',
        },
        'earnings': {
            'revTtm': fmt_b(revenue) if revenue else fallback.get('revTtm', 'N/A'),
            'revGrowth': f'+{rev_growth:.1f}%' if rev_growth else fallback.get('revGrowth', 'N/A'),
            'netIncome': fmt_b(net_income) if net_income else fallback.get('netIncome', 'N/A'),
            'peRatio': f'{pe:.1f}x' if pe else fallback.get('peRatio', 'N/A'),
            'psRatio': f'{ps:.1f}x' if ps else fallback.get('psRatio', 'N/A'),
        },
        'analyst': {
            'consensus': meta['analystConsensus'],
            'target': target_price,
            'buys': meta['analystBuys'],
            'holds': meta['analystHolds'],
            'sells': meta['analystSells'],
        },
    }

def main():
    print('📊 Refreshing Signal Highlights data from yfinance...')
    results = []
    for ticker in TICKERS:
        entry = fetch_one(ticker)
        results.append(entry)
        status = '✓' if entry['earnings']['revGrowth'] != 'N/A' else '⚠️'
        print(f'  {status} {ticker}: ${entry["currentPrice"]} ({entry["changePercent"]:+.2f}%), Target ${entry["fairValue"]["price"]}, {entry["fairValue"]["upside"]} upside')

    outpath = os.path.join(DATA_DIR, 'signal-highlights.json')
    with open(outpath, 'w') as f:
        json.dump(results, f, indent=2)
    print(f'  ✅ Written to {outpath}')

if __name__ == '__main__':
    main()
