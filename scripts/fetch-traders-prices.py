#!/usr/bin/env python3
"""The Signal — Trader Holdings Price Fetcher (yfinance)

Reads data/traders.json, collects every unique holding ticker across all six
investor pages (buffett, pelosi, cathie, ackman, nvidia, cohen), fetches the
current price + 1-day % change for each via yfinance, and writes "price" /
"change" back into every holding object.

Per-ticker try/except: tickers with no public data (e.g. private GENB,
delisted BBBY) fail gracefully and keep null → the page renders '—' for them,
which is the expected outcome (private holding / exited position).

Usage:  .venv/bin/python3 scripts/fetch-traders-prices.py
"""

import json
import sys
from pathlib import Path

import yfinance as yf

ROOT = Path(__file__).resolve().parent.parent
DATA_PATH = ROOT / "data" / "traders.json"

TIMEOUT = 15  # seconds per ticker (yfinance history() timeout kwarg)

# Tickers that must ALWAYS stay null → the page renders '—' for them.
# GENB (Generate:Biomedicines) is a private company — no public quote.
# BBBY (Bed Bath & Beyond) is delisted — exited position, no live data.
NO_DATA_TICKERS = {"GENB", "BBBY"}


def fetch_quote(ticker):
    """Return (price, change_pct) or (None, None) on any failure."""
    if ticker in NO_DATA_TICKERS:
        return None, None
    try:
        t = yf.Ticker(ticker)
        hist = t.history(
            period="5d", interval="1d", auto_adjust=False, timeout=TIMEOUT
        )
        if hist is None or hist.empty or "Close" not in hist.columns:
            return None, None
        closes = hist["Close"].dropna()
        if len(closes) < 1:
            return None, None
        price = float(closes.iloc[-1])
        change = None
        if len(closes) >= 2:
            prev = float(closes.iloc[-2])
            if prev:
                change = (price - prev) / prev * 100.0
        return price, change
    except Exception:
        return None, None


def main():
    if not DATA_PATH.exists():
        print(f"✗ data/traders.json not found at {DATA_PATH}")
        sys.exit(1)

    traders = json.loads(DATA_PATH.read_text("utf-8"))
    investors = traders.get("investors", [])
    if not investors:
        print("✗ no investors in data/traders.json")
        sys.exit(1)

    # Collect unique tickers (first-appearance order) + every holding slot
    seen = {}
    slots = []
    for inv in investors:
        for h in inv.get("holdings", []):
            ticker = str(h.get("ticker", "")).strip().upper()
            if not ticker:
                continue
            slots.append((inv.get("slug"), h))
            if ticker not in seen:
                seen[ticker] = 1

    unique = list(seen.keys())
    print(f"ℹ  {len(unique)} unique tickers across {len(investors)} investors "
          f"({len(slots)} holding slots)\n")

    results = {}
    for i, ticker in enumerate(unique, 1):
        price, change = fetch_quote(ticker)
        results[ticker] = (price, change)
        if price is not None:
            chg = f"{change:+.2f}%" if change is not None else "n/a"
            print(f"  [{i:>2}/{len(unique)}] {ticker:<6} ${price:>10.2f}  {chg}")
        else:
            print(f"  [{i:>2}/{len(unique)}] {ticker:<6} FAILED → null (page shows '—')")

    # Write price/change back into every holding slot
    populated = 0
    failed = 0
    for slug, h in slots:
        ticker = str(h.get("ticker", "")).strip().upper()
        price, change = results.get(ticker, (None, None))
        if price is not None:
            # Round to cents / 2 decimals to keep the JSON tidy
            h["price"] = round(price, 2)
            h["change"] = round(change, 4) if change is not None else None
            populated += 1
        else:
            h["price"] = None
            h["change"] = None
            failed += 1

    DATA_PATH.write_text(json.dumps(traders, indent=2, ensure_ascii=False), "utf-8")

    print(f"\n✓ saved {DATA_PATH}")
    print(f"✓ {populated}/{len(slots)} holding slots populated "
          f"({failed} left null — private/delisted tickers)")


if __name__ == "__main__":
    main()
