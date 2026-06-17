#!/bin/bash
# The Signal — Stock Page Refresh Pipeline
# Fetches fresh data, rebuilds stock pages (deployed with main site to readthesignal.net).
#
# Usage: ./scripts/refresh-stock-page.sh [--price-only] [--no-fmp]
#   --price-only  Only refresh prices (skip yfinance + FMP + moat)
#   --no-fmp      Skip FMP enrichment

set -euo pipefail
cd "$(dirname "$0")/.."

# SAFETY: reset design-only files to committed state before building
# Prevents uncommitted CSS/JS/template changes from poisoning the deploy
git checkout -- _backup_dist/ public/css/ public/js/ 2>/dev/null || true

LOG="scripts/refresh-stock-page.log"
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')
echo "=== $TIMESTAMP ===" | tee -a "$LOG"

# All tickers to process (all public — yfinance/fetch-fmp for all)
PUBLIC_TICKERS="NVDA TSLA PLTR RKLB AMZN KTOS CRWV AXON MSFT SOFI ZS AVGO GOOGL SPCX"
ALL_TICKERS="NVDA TSLA PLTR RKLB AMZN KTOS CRWV AXON MSFT SOFI ZS AVGO GOOGL SPCX"

PRICE_ONLY=false
NO_FMP=false
for arg in "${@}"; do
  case "$arg" in
    --price-only) PRICE_ONLY=true ;;
    --no-fmp) NO_FMP=true ;;
  esac
done

# ── Step 1: Fetch fresh prices (Yahoo Finance, free, no API key needed) ──
echo "[1] Fetching prices..." | tee -a "$LOG"
node scripts/fetch-prices.js >> "$LOG" 2>&1 || echo "  ⚠️  Price fetch failed (continuing)" | tee -a "$LOG"

if ! $PRICE_ONLY; then
  # ── Step 2: Fetch financials from yfinance for each public ticker ──
  for TICKER in $PUBLIC_TICKERS; do
    echo "  Fetching $TICKER financials from yfinance..." | tee -a "$LOG"
    python3 scripts/fetch-financials.py $TICKER >> "$LOG" 2>&1 || echo "  ⚠️  $TICKER yfinance fetch failed (continuing)" | tee -a "$LOG"
  done

  # Map SPCX → SPACEX in financials.json (real ticker SPCX, internal key SPACEX)
  python3 -c "
import json
with open('data/financials.json') as f: d = json.load(f)
if 'SPCX' in d:
    d['SPACEX'] = d.pop('SPCX')
    with open('data/financials.json', 'w') as f: json.dump(d, f, indent=2)
    print('  Mapped SPCX → SPACEX in financials.json')
" >> "$LOG" 2>&1 || true

  # ── Step 3: Enrich with FMP data ──
  if ! $NO_FMP; then
    echo "  Enriching with FMP data for all public tickers..." | tee -a "$LOG"
    python3 scripts/fetch-fmp.py $PUBLIC_TICKERS >> "$LOG" 2>&1 || echo "  ⚠️  FMP enrichment failed (continuing)" | tee -a "$LOG"
  fi
fi

# ── Step: Morningstar Moat Assessment (weekly — Sundays only) ──
if [ "$(date +%u)" = "7" ]; then
  echo "  Running Morningstar moat assessment (weekly)..." | tee -a "$LOG"
  for TICKER in $ALL_TICKERS; do
    python3 scripts/generate-moat.py $TICKER > data/moat-$TICKER.json 2>>"$LOG" || {
      echo "  ⚠️  $TICKER moat assessment failed (continuing with defaults)" | tee -a "$LOG"
      echo '{"rating":"None","stars":1,"confidence":"Low","sources":[],"analysis":"Assessment unavailable."}' > data/moat-$TICKER.json
    }
  done
fi

# ── Step (last): Rebuild all stock pages into dist/stocks/ ──
echo "Rebuilding stock pages..." | tee -a "$LOG"
node scripts/build-stock-page.js >> "$LOG" 2>&1 || {
  echo "  ❌ Stock page build FAILED" | tee -a "$LOG"
  exit 1
}

echo "  ✅ Stock pages rebuilt into dist/stocks/" | tee -a "$LOG"
echo "  🌐 Deployed with main site to https://readthesignal.net/stocks/NVDA/" | tee -a "$LOG"

echo "=== Done at $(date '+%Y-%m-%d %H:%M:%S') ===" | tee -a "$LOG"
echo "" >> "$LOG"
