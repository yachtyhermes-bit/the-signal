#!/bin/bash
# Refresh Signal Highlight prices from yfinance and redeploy
# Called by cron every 2 hours during market hours
set -e
cd /home/chino/thesignal

echo "[$(date)] Refreshing Signal Highlight prices..."
python3 scripts/refresh-signal-highlights.py

echo "[$(date)] Rebuilding site..."
node build.js

echo "[$(date)] Deploying to Vercel..."
npx vercel --prod --token "$(cat /home/chino/.vercel/token)" --force 2>&1 | tail -5

echo "[$(date)] Done."
