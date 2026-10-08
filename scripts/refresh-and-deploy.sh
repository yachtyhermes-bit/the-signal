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

# Scorecard: refresh the data AND render it into the homepage design file.
# The section used to be hand-baked into _backup_dist/index.html and went stale for months
# because nothing rendered data/scorecard.json. Both steps are guarded so a failure keeps
# the previous values instead of aborting the deploy.
echo "[$(date)] Refreshing scorecard data + injecting section..."
python3 scripts/refresh-scorecard.py || echo "  [WARN] scorecard refresh failed — previous data kept"
python3 scripts/inject-scorecard.py || echo "  [WARN] scorecard inject failed — previous section kept"

echo "[$(date)] Rebuilding site..."
node build.js

echo "[$(date)] Deploying to Vercel..."
signal_deploy "readthesignal.net"

echo "[$(date)] Done."
