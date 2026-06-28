#!/bin/bash
# The Signal — Stock Page Refresh Pipeline
# Fetches fresh data, rebuilds stock pages (deployed with main site to readthesignal.net).
#
# Usage: ./scripts/refresh-stock-page.sh [--price-only] [--no-fmp] [--deploy]
#   --price-only  Only refresh prices (skip yfinance + FMP + moat)
#   --no-fmp      Skip FMP enrichment
#   --deploy      Deploy to Vercel after building

set -euo pipefail
cd "$(dirname "$0")/.."

# SAFETY: reset design-only files to committed state before building
# Prevents uncommitted CSS/JS/template changes from poisoning the deploy
git checkout -- _backup_dist/ public/css/ public/js/ 2>/dev/null || true

LOG="scripts/refresh-stock-page.log"
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')
echo "=== $TIMESTAMP ===" | tee -a "$LOG"

# All tickers to process (all public — yfinance/fetch-fmp for all)
PUBLIC_TICKERS="NVDA TSLA PLTR RKLB AMZN KTOS CRWV AXON MSFT SOFI ZS AVGO GOOGL SPCX MU MRVL AMD ANET AMAT"
ALL_TICKERS="NVDA TSLA PLTR RKLB AMZN KTOS CRWV AXON MSFT SOFI ZS AVGO GOOGL SPCX MU MRVL AMD ANET AMAT"

PRICE_ONLY=false
NO_FMP=false
DEPLOY=false
for arg in "${@}"; do
  case "$arg" in
    --price-only) PRICE_ONLY=true ;;
    --no-fmp) NO_FMP=true ;;
    --deploy) DEPLOY=true ;;
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
echo "  ✅ Individual stock pages rebuilt" | tee -a "$LOG"

# ── Step: Rebuild stocks index page ──
echo "Rebuilding stocks index..." | tee -a "$LOG"
node scripts/build-stocks-index.js >> "$LOG" 2>&1 || {
  echo "  ❌ Stocks index build FAILED" | tee -a "$LOG"
  exit 1
}
echo "  ✅ Stocks index rebuilt" | tee -a "$LOG"

echo "  🌐 Stock pages ready at dist/stocks/" | tee -a "$LOG"

# ── Step: Deploy if requested ──
if $DEPLOY; then
  echo "Deploying to Vercel..." | tee -a "$LOG"
  VERCEL_ARGS="--prod --yes"
  if [ -f "$HOME/.vercel/token" ]; then
    VERCEL_ARGS="$VERCEL_ARGS --token $(cat $HOME/.vercel/token)"
  fi
  npx vercel $VERCEL_ARGS >> "$LOG" 2>&1 || {
    echo "  ❌ Vercel deploy FAILED" | tee -a "$LOG"
    exit 1
  }
  echo "  ✅ Deployed to Vercel" | tee -a "$LOG"
fi

echo "=== Done at $(date '+%Y-%m-%d %H:%M:%S') ===" | tee -a "$LOG"
echo "" >> "$LOG"
