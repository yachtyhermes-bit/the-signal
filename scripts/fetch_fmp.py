#!/usr/bin/env python3
"""
FMP enrichment for ticker financial data.
Fetches annual income statement and balance sheet from FMP API,
falling back to yfinance annual data when FMP is unavailable.

Exports: enrich_ticker_data(ticker_symbol, ticker_data) -> ticker_data
"""

import json
import os
import sys
from datetime import datetime

import requests
import yfinance as yf


def _load_fmp_key():
    """Load FMP API key from environment or .env.local"""
    key = os.environ.get('FMP_API_KEY', '').strip()
    if key:
        return key

    # Try .env.local
    env_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        '.env.local'
    )
    if os.path.exists(env_path):
        with open(env_path) as f:
            for line in f:
                line = line.strip()
                if line.startswith('FMP_API_KEY='):
                    key = line.split('=', 1)[1].strip().strip('"').strip("'")
                    if key:
                        return key
    return None


def _fetch_fmp(endpoint, ticker, api_key, limit=5):
    """Fetch data from FMP API. Returns list of dicts or None on failure."""
    url = f'https://financialmodelingprep.com/api/v3/{endpoint}/{ticker}'
    params = {'apikey': api_key, 'limit': limit}
    try:
        resp = requests.get(url, params=params, timeout=30)
        if resp.status_code == 200:
            data = resp.json()
            if isinstance(data, list):
                return data
        # 403 = legacy endpoint not available, 429 = rate limit
        return None
    except Exception:
        return None


def _safe_float(v):
    """Safely convert to float, return None for NaN."""
    if v is None:
        return None
    try:
        fv = float(v)
        if fv != fv:  # NaN check
            return None
        return fv
    except (ValueError, TypeError):
        return None


def enrich_ticker_data(ticker_symbol, ticker_data):
    """
    Enrich ticker_data with fmpIncome and fmpBalance from FMP API,
    falling back to yfinance annual data.

    Returns enriched ticker_data dict.
    """
    fmp_income = []
    fmp_balance = []

    # ── Try FMP API first ──
    api_key = _load_fmp_key()
    fmp_worked = False

    if api_key:
        # Income statement
        raw_income = _fetch_fmp('income-statement', ticker_symbol, api_key, limit=5)
        if raw_income:
            for entry in raw_income:
                fmp_income.append({
                    'date': entry.get('date', ''),
                    'revenue': _safe_float(entry.get('revenue')),
                    'grossProfit': _safe_float(entry.get('grossProfit')),
                    'netIncome': _safe_float(entry.get('netIncome')),
                })
            fmp_worked = True

        # Balance sheet
        raw_balance = _fetch_fmp('balance-sheet-statement', ticker_symbol, api_key, limit=5)
        if raw_balance:
            for entry in raw_balance:
                fmp_balance.append({
                    'date': entry.get('date', ''),
                    'totalAssets': _safe_float(entry.get('totalAssets')),
                    'totalLiabilities': _safe_float(entry.get('totalLiabilities')),
                })

    # ── Fallback to yfinance annual data ──
    if not fmp_income or not fmp_balance:
        print(f'  ⚠️  FMP unavailable, falling back to yfinance annual data for {ticker_symbol}')
        try:
            ticker = yf.Ticker(ticker_symbol)

            # Annual income statement
            if not fmp_income:
                is_annual = ticker.income_stmt
                if is_annual is not None and not is_annual.empty:
                    for col in is_annual.columns[:8]:
                        date_str = col.strftime('%Y-%m-%d') if hasattr(col, 'strftime') else str(col)[:10]
                        rev = _safe_float(is_annual.loc['Total Revenue', col] if 'Total Revenue' in is_annual.index else None)
                        gp = _safe_float(is_annual.loc['Gross Profit', col] if 'Gross Profit' in is_annual.index else None)
                        ni = _safe_float(is_annual.loc['Net Income', col] if 'Net Income' in is_annual.index else None)
                        # Skip entries where all values are None
                        if rev is None and gp is None and ni is None:
                            continue
                        fmp_income.append({
                            'date': date_str,
                            'revenue': rev,
                            'grossProfit': gp,
                            'netIncome': ni,
                        })
                    if fmp_income:
                        print(f'  ✓ fmpIncome: {len(fmp_income)} annual entries from yfinance')

            # Annual balance sheet
            if not fmp_balance:
                bs_annual = ticker.balance_sheet
                if bs_annual is not None and not bs_annual.empty:
                    for col in bs_annual.columns[:8]:
                        date_str = col.strftime('%Y-%m-%d') if hasattr(col, 'strftime') else str(col)[:10]
                        ta = _safe_float(bs_annual.loc['Total Assets', col] if 'Total Assets' in bs_annual.index else None)
                        tl = _safe_float(bs_annual.loc['Total Liabilities Net Minority Interest', col] if 'Total Liabilities Net Minority Interest' in bs_annual.index else None)
                        if tl is None:
                            tl = _safe_float(bs_annual.loc['Total Liabilities', col] if 'Total Liabilities' in bs_annual.index else None)
                        if ta is None and tl is None:
                            continue
                        fmp_balance.append({
                            'date': date_str,
                            'totalAssets': ta,
                            'totalLiabilities': tl,
                        })
                    if fmp_balance:
                        print(f'  ✓ fmpBalance: {len(fmp_balance)} annual entries from yfinance')

        except Exception as e:
            print(f'  ⚠️  yfinance fallback failed: {e}')

    # ── Store results ──
    if fmp_income:
        ticker_data['fmpIncome'] = fmp_income
    if fmp_balance:
        ticker_data['fmpBalance'] = fmp_balance

    return ticker_data
