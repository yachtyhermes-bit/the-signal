#!/usr/bin/env python3
"""Verify article prices against historical data at publication time."""

import yfinance as yf
import json
import pandas as pd

# Check historical prices near publication date
checks = [
    ('CRDO', 268.00, '2026-07-09', 'CRDO'),
    ('SMCI', 28.17, '2026-07-09', 'SMCI'),
    ('VRT', 327.25, '2026-07-09', 'VRT (Q1 art)'),
    ('COIN', 163.51, '2026-07-08', 'COIN'),
    ('CRWV', 85.00, '2026-07-08', 'CRWV'),
    ('KTOS', 50.34, '2026-07-08', 'KTOS'),
    ('VRT', 316.65, '2026-07-08', 'VRT (infra art)'),
    ('AXON', 622.35, '2026-07-07', 'AXON'),
    ('AMAT', 534.71, '2026-07-07', 'AMAT'),
    ('NOW', 112.99, '2026-07-07', 'NOW'),
]

for sym, art_price, pub_date, label in checks:
    try:
        t = yf.Ticker(sym)
        # Get historical data around publication date
        hist = t.history(period="1mo")
        
        # Find the last close before or on pub date
        pub_dt = pd.Timestamp(pub_date).tz_localize('America/New_York')
        hist_before = hist[hist.index <= pub_dt]
        
        if len(hist_before) > 0:
            last_close = hist_before.iloc[-1]['Close']
            # Also check the current price
            current = t.info.get('currentPrice') or t.info.get('previousClose') or hist.iloc[-1]['Close']
            
            diff_from_hist = abs(art_price - last_close) / last_close * 100
            
            print(f"{label} ({sym}): art=${art_price}, hist_close=${last_close:.2f} (on/before {pub_date}), current=${current:.2f}")
            if diff_from_hist > 5:
                print(f"  ⚠️ PRICE MISMATCH vs historical: {diff_from_hist:.1f}% off from ${last_close:.2f}")
            else:
                print(f"  ✓ Price within {diff_from_hist:.1f}% of historical close")
        else:
            print(f"{label} ({sym}): No historical data for {pub_date}")
            
    except Exception as e:
        print(f"{label} ({sym}): ERROR - {e}")
