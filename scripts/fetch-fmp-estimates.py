#!/usr/bin/env python3
"""Fetch historical analyst revenue + EPS estimates from Financial Modeling Prep.
Free tier: 250 calls/day, 5 years history. Merge into financials.json.

Usage:
    python3 scripts/fetch-fmp-estimates.py [--tickers NVDA,PLTR,AVGO]

Requires FMP_API_KEY in environment or .env.local.
"""

import json
import os
import sys
import time
from datetime import datetime
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parent.parent
FINANCIALS_PATH = ROOT / 'data' / 'financials.json'
ENV_PATH = ROOT / '.env.local'

FMP_BASE = 'https://financialmodelingprep.com/api/v3'

# ── Load API key ────────────────────────────────────────────────
def load_api_key():
    """Load FMP API key from environment or .env.local"""
    key = os.environ.get('FMP_API_KEY', '').strip()
    if key:
        return key

    if ENV_PATH.exists():
        for line in ENV_PATH.read_text().splitlines():
            line = line.strip()
            if line.startswith('FMP_API_KEY='):
                key = line.split('=', 1)[1].strip().strip('"').strip("'")
                if key:
                    return key

    # Fallback: check Hermes profile .env
    hermes_env = Path(os.environ.get('HERMES_HOME', '')) / '.env'
    if hermes_env.exists():
        for line in hermes_env.read_text().splitlines():
            line = line.strip()
            if line.startswith('FMP_API_KEY='):
                key = line.split('=', 1)[1].strip().strip('"').strip("'")
                if key:
                    return key

    return None


# ── Fetch analyst estimates from FMP ────────────────────────────
def fetch_analyst_estimates(ticker: str, api_key: str) -> list[dict]:
    """Fetch quarterly analyst estimates for a ticker.
    
    Returns list of {date, estimatedRevenueAvg, estimatedEpsAvg, ...}
    Sorted oldest → newest.
    """
    url = f'{FMP_BASE}/analyst-estimates/{ticker}'
    params = {
        'period': 'quarter',
        'apikey': api_key,
        'limit': 40,  # ~10 years of quarters
    }

    resp = requests.get(url, params=params, timeout=30)
    if resp.status_code == 429:
        print(f'  ⚠️  Rate limited on {ticker}, waiting 5s...')
        time.sleep(5)
        resp = requests.get(url, params=params, timeout=30)

    if resp.status_code != 200:
        print(f'  ✗ FMP returned {resp.status_code} for {ticker}: {resp.text[:200]}')
        return []

    data = resp.json()
    if not isinstance(data, list):
        print(f'  ✗ Unexpected FMP response for {ticker}: {type(data).__name__}')
        return []

    # Sort by date ascending (oldest first)
    data.sort(key=lambda x: x.get('date', ''))

    return data


# ── Merge estimates into earnings data ──────────────────────────
def merge_estimates(earnings: list[dict], estimates: list[dict]) -> list[dict]:
    """Match FMP analyst estimates to existing earnings entries by quarter.
    
    Earnings entries have dates like '2026-05-20' (announcement date).
    FMP estimates have dates like '2026-04-30' (fiscal quarter end).
    We match by finding the closest fiscal quarter end within 60 days.
    """
    from datetime import datetime, timedelta

    # Build lookup: fiscal quarter end → {revenue est, eps est}
    est_map = {}
    for e in estimates:
        if not e.get('date'):
            continue
        try:
            est_date = datetime.strptime(e['date'], '%Y-%m-%d')
        except ValueError:
            try:
                est_date = datetime.strptime(e['date'][:10], '%Y-%m-%d')
            except ValueError:
                continue

        est_map[est_date] = {
            'revenueEstimate': e.get('estimatedRevenueAvg'),
            'epsEstimate': e.get('estimatedEpsAvg'),
            'revenueLow': e.get('estimatedRevenueLow'),
            'revenueHigh': e.get('estimatedRevenueHigh'),
            'epsLow': e.get('estimatedEpsLow'),
            'epsHigh': e.get('estimatedEpsHigh'),
        }

    # Match each earnings entry to closest fiscal quarter
    for entry in earnings:
        if not entry.get('date'):
            continue
        try:
            earn_date = datetime.strptime(entry['date'][:10], '%Y-%m-%d')
        except ValueError:
            continue

        best_match = None
        best_diff = timedelta(days=365)

        for est_date, est_data in est_map.items():
            diff = abs((est_date - earn_date).days)
            if diff < best_diff.days and diff <= 60:
                best_diff = timedelta(days=diff)
                best_match = est_data

        if best_match:
            # Only fill revenueEstimate if it's currently missing AND the FMP data is present
            if entry.get('revenueEstimate') is None and best_match.get('revenueEstimate') is not None:
                entry['revenueEstimate'] = float(best_match['revenueEstimate'])
            # Optionally backfill EPS estimate if missing (but yfinance usually has this)
            if entry.get('epsEstimate') is None and best_match.get('epsEstimate') is not None:
                entry['epsEstimate'] = float(best_match['epsEstimate'])

    return earnings


# ── Main ────────────────────────────────────────────────────────
def main():
    api_key = load_api_key()
    if not api_key:
        print('❌ FMP_API_KEY not found.')
        print('   Set it in .env.local: FMP_API_KEY=your_free_key')
        print('   Sign up: https://financialmodelingprep.com/')
        sys.exit(1)

    # Parse tickers
    tickers = []
    for i, arg in enumerate(sys.argv[1:]):
        if arg.startswith('--tickers='):
            tickers = [t.strip().upper() for t in arg.split('=', 1)[1].split(',')]
        elif arg.startswith('--ticker=') and i == 0:
            tickers = [arg.split('=', 1)[1].strip().upper()]

    if not tickers:
        # Default: all tickers in financials.json
        if FINANCIALS_PATH.exists():
            with open(FINANCIALS_PATH) as f:
                fin = json.load(f)
            tickers = list(fin.keys())
        if not tickers:
            tickers = ['NVDA']

    print(f'📊 FMP Analyst Estimates → {len(tickers)} ticker(s)')

    # Load existing financials
    if FINANCIALS_PATH.exists():
        with open(FINANCIALS_PATH) as f:
            financials = json.load(f)
    else:
        financials = {}

    updated = 0
    for ticker in tickers:
        print(f'\n  🔍 {ticker}...')
        estimates = fetch_analyst_estimates(ticker, api_key)

        if not estimates:
            print(f'    ⚠️  No estimates returned')
            continue

        print(f'    ✓ {len(estimates)} quarterly estimates from FMP')

        # Get existing earnings data
        ticker_data = financials.get(ticker, {})
        earnings = ticker_data.get('earnings', [])

        before_rev = sum(1 for e in earnings if e.get('revenueEstimate'))

        # Merge
        earnings = merge_estimates(earnings, estimates)

        after_rev = sum(1 for e in earnings if e.get('revenueEstimate'))
        filled = after_rev - before_rev

        # Save back
        if ticker not in financials:
            financials[ticker] = {}
        financials[ticker]['earnings'] = earnings

        print(f'    📈 Revenue estimates filled: {filled} (was {before_rev}, now {after_rev})')
        updated += filled

        # Rate limit: 250 calls/day, be gentle
        if ticker != tickers[-1]:
            time.sleep(0.5)

    # Write back
    with open(FINANCIALS_PATH, 'w') as f:
        json.dump(financials, f, indent=2, default=str)

    print(f'\n✅ Done. {updated} revenue estimates added across {len(tickers)} ticker(s)')
    print(f'   Calls used: {len(tickers)} / 250 daily limit')


if __name__ == '__main__':
    main()
