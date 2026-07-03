#!/bin/bash
# Refresh Signal Highlight prices from yfinance and redeploy
# Called by cron every 2 hours during market hours
set -e
cd /home/chino/thesignal

# Source deploy helper
. scripts/deploy-helper.sh

# SAFETY: reset design-only files to committed state before building
# Prevents uncommitted CSS/JS/template changes from poisoning the deploy
git checkout -- _backup_dist/ public/css/ public/js/ 2>/dev/null || true

echo "[$(date)] Refreshing Signal Highlight prices..."
python3 scripts/refresh-signal-highlights.py

echo "[$(date)] Rebuilding site..."
node build.js

echo "[$(date)] Deploying to Vercel..."
signal_deploy "readthesignal.net"

echo "[$(date)] Done."
