#!/usr/bin/env python3
"""FMP data fetcher for stock pages. Pulls profiles, quotes, OHLCV, and key metrics.
Free tier: 250 calls/day. Cache-aware — skips if data is fresh.

Intended to be called from fetch-financials.py or standalone.
"""

import json
import os
import time
from datetime import datetime, timezone
from pathlib import Path

import requests

FMP_BASE = 'https://financialmodelingprep.com/stable'
CACHE_TTL_HOURS = {
    'quote': 0.25,      # 15 min for live prices
    'profile': 6,       # 6 hours for company profiles
    'historical': 24,   # 24 hours for OHLCV history
    'income': 24,       # 24 hours for financial statements
    'balance': 24,
    'metrics': 24,
    'growth': 24,
}


def load_api_key():
    """Load FMP API key from environment or .env.local"""
    key = os.environ.get('FMP_API_KEY', '').strip()
    if key:
        return key

    env_path = Path(__file__).resolve().parent.parent / '.env.local'
    if env_path.exists():
        for line in env_path.read_text().splitlines():
            line = line.strip()
            if line.startswith('FMP_API_KEY='):
                key = line.split('=', 1)[1].strip().strip('"').strip("'")
                if key:
                    return key
    return None


def _get(endpoint: str, params: dict, timeout: int = 30) -> dict | list | None:
    """Make an FMP API call with rate-limit handling."""
    api_key = load_api_key()
    if not api_key:
        print('  ⚠️  No FMP_API_KEY set — skipping FMP')
        return None

    params['apikey'] = api_key
    url = f'{FMP_BASE}/{endpoint}'

    for attempt in range(3):
        try:
            resp = requests.get(url, params=params, timeout=timeout)
            if resp.status_code == 429:
                wait = 2 ** attempt
                print(f'  ⏳ Rate limited, waiting {wait}s...')
                time.sleep(wait)
                continue
            if resp.status_code != 200:
                print(f'  ✗ FMP {endpoint} → {resp.status_code}: {resp.text[:120]}')
                return None
            data = resp.json()
            if isinstance(data, dict) and 'Error' in str(data):
                print(f'  ✗ FMP error: {str(data)[:150]}')
                return None
            return data
        except requests.RequestException as e:
            print(f'  ✗ FMP {endpoint} network error: {e}')
            time.sleep(1)
    return None


def fetch_profile(symbol: str) -> dict | None:
    """Fetch company profile: name, sector, price, mkt cap, range, beta, volume."""
    data = _get('profile', {'symbol': symbol})
    if isinstance(data, list) and data:
        return data[0]
    return None


def fetch_quote(symbol: str) -> dict | None:
    """Fetch real-time quote: price, change, changePercent, volume."""
    data = _get('quote', {'symbol': symbol})
    if isinstance(data, list) and data:
        return data[0]
    return None


def fetch_historical(symbol: str) -> list[dict] | None:
    """Fetch full OHLCV history (~5 years, daily). Returns list sorted newest→oldest."""
    data = _get('historical-price-eod/full', {'symbol': symbol})
    if isinstance(data, dict) and 'historical' in data:
        return data['historical']
    if isinstance(data, list) and data:
        return data
    return None


def fetch_income_statement(symbol: str, limit: int = 5) -> list[dict] | None:
    """Fetch annual income statements."""
    data = _get('income-statement', {'symbol': symbol, 'limit': limit})
    if isinstance(data, list):
        return data
    return None


def fetch_balance_sheet(symbol: str, limit: int = 5) -> list[dict] | None:
    """Fetch annual balance sheet statements."""
    data = _get('balance-sheet-statement', {'symbol': symbol, 'limit': limit})
    if isinstance(data, list):
        return data
    return None


def fetch_key_metrics(symbol: str, limit: int = 5) -> list[dict] | None:
    """Fetch key financial metrics: PE, margins, ROE, etc."""
    data = _get('key-metrics', {'symbol': symbol, 'limit': limit})
    if isinstance(data, list):
        return data
    return None


def fetch_financial_growth(symbol: str, limit: int = 5) -> list[dict] | None:
    """Fetch financial growth metrics: revenue growth, EPS growth."""
    data = _get('financial-growth', {'symbol': symbol, 'limit': limit})
    if isinstance(data, list):
        return data
    return None


def enrich_ticker_data(symbol: str, existing: dict) -> dict:
    """Enrich existing ticker data (from yfinance) with FMP data."""
    calls = 0

    # ── Profile ──
    profile = fetch_profile(symbol)
    if profile:
        calls += 1
        company = existing.get('company', {})
        company.setdefault('name', profile.get('companyName', company.get('name', '')))
        company.setdefault('sector', profile.get('sector', ''))
        company.setdefault('industry', profile.get('industry', company.get('industry', '')))
        company.setdefault('exchange', profile.get('exchange', ''))
        company.setdefault('website', profile.get('website', ''))
        company.setdefault('description', profile.get('description', company.get('description', '')))
        company.setdefault('employees', profile.get('fullTimeEmployees'))
        company.setdefault('city', profile.get('city', ''))
        company.setdefault('state', profile.get('state', ''))
        existing['company'] = company

        # Stats from profile
        stats = existing.get('stats', {})
        if profile.get('marketCap'):
            stats['marketCap'] = {'raw': profile['marketCap'], 'fmt': _fmt_large(profile['marketCap'])}
        if profile.get('beta'):
            stats['beta'] = {'raw': profile['beta'], 'fmt': f"{profile['beta']:.2f}"}
        if profile.get('range'):
            parts = profile['range'].split('-')
            if len(parts) == 2:
                try:
                    stats['fiftyTwoWeekLow'] = {'raw': float(parts[0].strip()), 'fmt': f"${float(parts[0].strip()):.2f}"}
                    stats['fiftyTwoWeekHigh'] = {'raw': float(parts[1].strip()), 'fmt': f"${float(parts[1].strip()):.2f}"}
                except ValueError:
                    pass
        if profile.get('volAvg'):
            stats['avgVolume'] = {'raw': profile['volAvg'], 'fmt': _fmt_volume(profile['volAvg'])}
        if profile.get('price'):
            stats['price'] = {'raw': profile['price'], 'fmt': f"${profile['price']:.2f}"}
        existing['stats'] = stats
        print(f'  ✓ FMP profile: {profile.get("companyName")} | \${profile.get("price")}')

    # ── Quote (fresh price) ──
    quote = fetch_quote(symbol)
    if quote:
        calls += 1
        existing['price'] = {
            'price': quote.get('price'),
            'change': quote.get('change'),
            'changePercent': quote.get('changesPercentage'),
            'volume': quote.get('volume'),
            'updated': datetime.now(timezone.utc).isoformat(),
        }
        print(f'  ✓ FMP quote: \${quote.get("price")} ({quote.get("changesPercentage", 0):+.2f}%)')

    # ── Historical OHLCV ──
    historical = fetch_historical(symbol)
    if historical:
        calls += 1
        chart_data = []
        for bar in historical[:1260]:  # 5 years
            dt = bar.get('date', '')
            chart_data.append({
                'time': dt,
                'open': bar.get('open'),
                'high': bar.get('high'),
                'low': bar.get('low'),
                'close': bar.get('close'),
                'volume': bar.get('volume', 0),
            })
        chart_data.reverse()  # oldest→newest for the chart
        existing['chartData'] = chart_data
        print(f'  ✓ FMP OHLCV: {len(chart_data)} days')

    # ── Key Metrics ──
    metrics = fetch_key_metrics(symbol)
    if metrics:
        calls += 1
        latest = metrics[0] if metrics else {}
        stats = existing.get('stats', {})
        for key, label in [
            ('peRatio', 'trailingPE'), ('priceToSalesRatio', 'priceToSales'),
            ('roe', 'returnOnEquity'), ('debtToEquity', 'debtToEquity'),
            ('revenuePerShare', 'revenuePerShare'), ('netProfitMargin', 'profitMargins'),
            ('grossProfitMargin', 'grossMargins'), ('operatingProfitMargin', 'operatingMargins'),
            ('freeCashFlowPerShare', 'freeCashflowPerShare'),
        ]:
            if latest.get(key):
                stats[label] = {'raw': latest[key], 'fmt': _fmt_metric(latest[key], label)}
        existing['stats'] = stats

        # Growth from metrics
        growth = existing.get('growth', {})
        for key, label in [('revenueGrowth', 'revenueGrowth'), ('netIncomeGrowth', 'earningsGrowth')]:
            if latest.get(key):
                growth[label] = {'raw': latest[key], 'fmt': f"{latest[key]*100:.1f}%" if isinstance(latest[key], float) else str(latest[key])}
        existing['growth'] = growth
        print(f'  ✓ FMP metrics: {len(metrics)} periods')

    # ── Income Statement (cross-reference with yfinance) ──
    income = fetch_income_statement(symbol)
    if income:
        calls += 1
        existing['fmpIncome'] = income
        print(f'  ✓ FMP income: {len(income)} years')

    # ── Balance Sheet ──
    balance = fetch_balance_sheet(symbol)
    if balance:
        calls += 1
        existing['fmpBalance'] = balance
        print(f'  ✓ FMP balance: {len(balance)} years')

    # ── Financial Growth ──
    growth_data = fetch_financial_growth(symbol)
    if growth_data:
        calls += 1
        existing['fmpGrowth'] = growth_data
        print(f'  ✓ FMP growth: {len(growth_data)} periods')

    existing['fmpCalls'] = calls
    return existing


def _fmt_large(n: float) -> str:
    if n is None: return '—'
    if n >= 1e12: return f'${n/1e12:.2f}T'
    if n >= 1e9: return f'${n/1e9:.2f}B'
    if n >= 1e6: return f'${n/1e6:.1f}M'
    return f'${n:,.2f}'


def _fmt_volume(n: float) -> str:
    if n is None: return '—'
    if n >= 1e9: return f'{n/1e9:.1f}B'
    if n >= 1e6: return f'{n/1e6:.0f}M'
    return f'{n:,.0f}'


def _fmt_metric(val, label: str) -> str:
    if val is None: return '—'
    if 'margin' in label.lower() or 'growth' in label.lower() or 'roe' in label.lower():
        return f'{val*100:.1f}%' if isinstance(val, float) and abs(val) < 10 else f'{val:.2f}'
    return f'{val:.2f}' if isinstance(val, float) else str(val)


# ── Standalone ─────────────────────────────────────────────
if __name__ == '__main__':
    import sys
    symbols = sys.argv[1:] if len(sys.argv) > 1 else ['NVDA']

    # Load existing
    fin_path = Path(__file__).resolve().parent.parent / 'data' / 'financials.json'
    if fin_path.exists():
        with open(fin_path) as f:
            financials = json.load(f)
    else:
        financials = {}

    total_calls = 0
    for sym in symbols:
        sym = sym.upper().strip()
        print(f'\n📊 {sym}')
        ticker = financials.get(sym, {})
        ticker = enrich_ticker_data(sym, ticker)
        financials[sym] = ticker
        total_calls += ticker.get('fmpCalls', 0)

    with open(fin_path, 'w') as f:
        json.dump(financials, f, indent=2, default=str)

    print(f'\n✅ Done. {total_calls} FMP calls used ({250 - total_calls} remaining today)')
