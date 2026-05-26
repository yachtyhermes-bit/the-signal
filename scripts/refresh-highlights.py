#!/usr/bin/env python3
"""Pull real yfinance metrics for Signal Highlights stocks (KTOS, CRWV) and write data/highlights.json.
Run BEFORE build.js so the build reads live data instead of hardcoded values."""

import json, os, sys

try:
    import yfinance as yf
except ImportError:
    os.system(f"{sys.executable} -m pip install yfinance -q --break-system-packages")
    import yfinance as yf

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(ROOT, 'data')
os.makedirs(DATA_DIR, exist_ok=True)

def fmt_b(v):
    if v is None: return 'N/A'
    v = float(v)
    if abs(v) >= 1e12: return f'${v/1e12:.2f}T'
    if abs(v) >= 1e9: return f'${v/1e9:.2f}B'
    if abs(v) >= 1e6: return f'${v/1e6:.2f}M'
    return f'${v:.2f}'

def fetch_highlights():
    """Fetch financial data for Signal Highlights stocks."""
    # Hardcoded metadata (analyst breakdown is stable, not in yfinance info)
    metadata = {
        'KTOS': {
            'name': 'Kratos Defense & Security',
            'fairValue': {'status': 'Undervalued', 'upside': '+99.3%'},
            'analyst': {'consensus': 'Strong Buy', 'buys': 15, 'holds': 5, 'sells': 0},
        },
        'CRWV': {
            'name': 'CoreWeave Inc.',
            'fairValue': {'status': 'Undervalued', 'upside': '+31.7%'},
            'analyst': {'consensus': 'Buy', 'buys': 15, 'holds': 16, 'sells': 0},
        }
    }

    results = []
    for ticker in ['KTOS', 'CRWV']:
        try:
            t = yf.Ticker(ticker)
            info = t.info or {}
            annual = t.financials

            # Revenue TTM
            revenue = info.get('totalRevenue')

            # Rev Growth YoY
            rev_growth_yoy = None
            if annual is not None and not annual.empty:
                if 'Total Revenue' in annual.index:
                    rev_vals = annual.loc['Total Revenue'].dropna()
                    if len(rev_vals) >= 2:
                        rev_growth_yoy = ((float(rev_vals.iloc[0]) - float(rev_vals.iloc[1])) / float(rev_vals.iloc[1])) * 100
            if rev_growth_yoy is None:
                rg = info.get('revenueGrowth')
                if rg is not None:
                    rev_growth_yoy = rg * 100

            # Net Income
            net_income = info.get('netIncomeToCommon')

            # P/E
            pe = info.get('trailingPE')

            # P/S
            ps = info.get('priceToSalesTrailing12Months')

            # Price and target
            current_price = info.get('currentPrice') or info.get('regularMarketPrice')
            target = info.get('targetMeanPrice') or info.get('targetMedianPrice')

            # Build result
            meta = metadata[ticker]
            entry = {
                'ticker': ticker,
                'name': meta['name'],
                'currentPrice': round(float(current_price), 2) if current_price else 0,
                'fairValue': {
                    'status': meta['fairValue']['status'],
                    'price': round(float(target), 2) if target else 0,
                    'upside': meta['fairValue']['upside'],
                },
                'earnings': {
                    'revTtm': fmt_b(revenue),
                    'revGrowth': f'+{rev_growth_yoy:.1f}%' if rev_growth_yoy else 'N/A',
                    'netIncome': fmt_b(net_income),
                    'peRatio': f'{pe:.1f}x' if pe else 'N/A',
                    'psRatio': f'{ps:.1f}x' if ps else 'N/A',
                },
                'analyst': {
                    'consensus': meta['analyst']['consensus'],
                    'target': round(float(target), 2) if target else 0,
                    'buys': meta['analyst']['buys'],
                    'holds': meta['analyst']['holds'],
                    'sells': meta['analyst']['sells'],
                },
            }
            results.append(entry)
            print(f'  ✓ {ticker}: Rev {entry["earnings"]["revGrowth"]}, PE {entry["earnings"]["peRatio"]}, PS {entry["earnings"]["psRatio"]}')

        except Exception as e:
            print(f'  ⚠️  Failed to fetch {ticker}: {e}', file=sys.stderr)
            # Fallback to last known good values
            meta = metadata[ticker]
            fallback = {
                'KTOS': {
                    'currentPrice': 56.18,
                    'fairValue': {'status': 'Undervalued', 'price': 111.95, 'upside': '+99.3%'},
                    'earnings': {'revTtm': '$1.42B', 'revGrowth': '+18.5%', 'netIncome': '$29.4M', 'peRatio': '330.5x', 'psRatio': '7.4x'},
                    'analyst': {'consensus': 'Strong Buy', 'target': 111.95, 'buys': 15, 'holds': 5, 'sells': 0},
                },
                'CRWV': {
                    'currentPrice': 105.49,
                    'fairValue': {'status': 'Undervalued', 'price': 138.90, 'upside': '+31.7%'},
                    'earnings': {'revTtm': '$6.23B', 'revGrowth': '+167.9%', 'netIncome': '-$1.59B', 'peRatio': 'N/A', 'psRatio': '9.2x'},
                    'analyst': {'consensus': 'Buy', 'target': 138.90, 'buys': 15, 'holds': 16, 'sells': 0},
                },
            }
            entry = {'ticker': ticker, 'name': meta['name']}
            entry.update(fallback[ticker])
            results.append(entry)
            print(f'  ⚠️  Using fallback for {ticker}')

    return results

if __name__ == '__main__':
    print('📊 Refreshing Signal Highlights data from yfinance...')
    data = fetch_highlights()

    outpath = os.path.join(DATA_DIR, 'highlights.json')
    with open(outpath, 'w') as f:
        json.dump(data, f, indent=2)

    print(f'  ✅ Written to {outpath}')
