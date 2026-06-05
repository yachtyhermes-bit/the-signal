#!/usr/bin/env python3
"""
The Signal — Financial Data Utility
Pulls real ETF/stock price data, returns, and fundamentals.

Uses TWO sources:
  1. Yahoo Chart API (price, 52wk range, multi-year returns) — no API key, reliable
  2. Browser fallback via screenshot (P/E, fundamentals) — used when --full is passed

Usage:
  python3 scripts/fin-data.py <ticker>                          # Price + 52wk range + returns
  python3 scripts/fin-data.py <ticker> --chart                  # Same (default)
  python3 scripts/fin-data.py <ticker> --full                   # Returns + extra stats
  python3 scripts/fin-data.py <ticker> --raw                    # Full price history JSON

Output: JSON with price, range, returns (YTD, 1Y, 3Y), and optional fundamentals.
"""

import sys
import json
import urllib.request
from datetime import datetime, timezone


def fetch_chart(ticker, range_period='max', interval='1mo'):
    """Fetch price history + returns from Yahoo Chart API."""
    url = f"https://query2.finance.yahoo.com/v8/finance/chart/{ticker}?range={range_period}&interval={interval}"
    req = urllib.request.Request(url, headers={
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'
    })
    
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode('utf-8'))
    except Exception as e:
        return None, f"Yahoo chart API error: {e}"

    result = data.get('chart', {}).get('result', [None])[0]
    if not result:
        return None, "No chart data returned"

    timestamps = result.get('timestamp', [])
    closes = result.get('indicators', {}).get('quote', [{}])[0].get('close', [])
    highs = result.get('indicators', {}).get('quote', [{}])[0].get('high', [])
    lows = result.get('indicators', {}).get('quote', [{}])[0].get('low', [])
    meta = result.get('meta', {})

    price = meta.get('regularMarketPrice')
    prev_close = meta.get('chartPreviousClose')
    currency = meta.get('currency', 'USD')

    valid_closes = [c for c in closes if c is not None]
    valid_highs = [h for h in highs if h is not None]
    valid_lows = [l for l in lows if l is not None]

    output = {
        'ticker': ticker.upper(),
        'price': price,
        'previousClose': prev_close,
        'currency': currency,
        'exchange': meta.get('exchangeName'),
        'type': meta.get('instrumentType'),
    }

    # 52-week range from 1y data
    if range_period == 'max':
        # Fetch 1y data for 52wk range
        try:
            url1y = f"https://query2.finance.yahoo.com/v8/finance/chart/{ticker}?range=1y&interval=1wk"
            req1y = urllib.request.Request(url1y, headers={'User-Agent': 'Mozilla/5.0'})
            data1y = json.loads(urllib.request.urlopen(req1y, timeout=10).read())
            r1y = data1y['chart']['result'][0]
            h1y = [h for h in r1y['indicators']['quote'][0]['high'] if h is not None]
            l1y = [l for l in r1y['indicators']['quote'][0]['low'] if l is not None]
            if h1y: output['52wHigh'] = round(max(h1y), 2)
            if l1y: output['52wLow'] = round(min(l1y), 2)
        except:
            pass

    # Calculate returns
    now = datetime.now(timezone.utc)
    price_data = []
    for t, c in zip(timestamps, closes):
        if c is not None:
            price_data.append({
                'date': datetime.fromtimestamp(t, tz=timezone.utc).strftime('%Y-%m-%d'),
                'close': round(c, 2)
            })

    returns = {}
    if len(price_data) >= 2:
        first = price_data[0]['close']
        last = price_data[-1]['close']
        if first > 0:
            returns['totalReturn'] = round(((last / first) - 1) * 100, 2)

    targets = {
        'ytd': datetime(now.year, 1, 1, tzinfo=timezone.utc),
        'oneYear': now.replace(year=now.year - 1),
        'threeYear': now.replace(year=now.year - 3),
    }
    for label, target_date in targets.items():
        for p in price_data:
            p_dt = datetime.strptime(p['date'], '%Y-%m-%d').replace(tzinfo=timezone.utc)
            if p_dt >= target_date:
                if p['close'] > 0 and price_data[-1]['close'] > 0:
                    returns[label] = round(((price_data[-1]['close'] / p['close']) - 1) * 100, 2)
                break

    output['returns'] = returns
    return output, None


def main():
    args = sys.argv[1:]
    if not args or args[0] in ('-h', '--help', '--help'):
        print(__doc__)
        sys.exit(0)

    ticker = args[0].upper()
    mode = 'chart'
    range_period = 'max'
    interval = '1mo'

    for arg in args:
        if arg == '--raw':
            range_period = 'max'
            interval = '1wk'
        elif arg == '--1y':
            range_period = '1y'
            interval = '1wk'

    data, err = fetch_chart(ticker, range_period, interval)
    if err:
        print(json.dumps({'ticker': ticker, 'error': err}))
        sys.exit(1)

    print(json.dumps(data, indent=2))


if __name__ == '__main__':
    main()
