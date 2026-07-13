#!/bin/bash
# Refresh Signal Highlight prices from yfinance and redeploy
# Called by cron every 2 hours during market hours
set -e
cd /home/chino/thesignal

# Source deploy helper
. scripts/deploy-helper.sh

# NOTE: We no longer auto-revert CSS/JS/design files before deploys.
# That caused fixes to vanish within 4h if not committed.
# If you see uncommitted changes, commit them manually.

echo "[$(date)] Refreshing Signal Highlight prices..."
python3 scripts/refresh-signal-highlights.py

echo "[$(date)] Rebuilding site..."
node build.js

echo "[$(date)] Deploying to Vercel..."
signal_deploy "readthesignal.net"

echo "[$(date)] Done."
