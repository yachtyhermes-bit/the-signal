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

# NOTE: We no longer auto-revert CSS/JS/design files before builds.
# That caused fixes to vanish within 4h if not committed.
# If you see uncommitted changes, commit them manually.

LOG="scripts/refresh-stock-page.log"
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')
echo "=== $TIMESTAMP ===" | tee -a "$LOG"

# All tickers to process (all public — yfinance/fetch-fmp for all)
PUBLIC_TICKERS="NVDA TSLA PLTR RKLB AMZN KTOS CRWV AXON MSFT SOFI ZS AVGO GOOGL SPCX MU MRVL AMD ANET AMAT META RTX NFLX RBRK AVAV"
ALL_TICKERS="NVDA TSLA PLTR RKLB AMZN KTOS CRWV AXON MSFT SOFI ZS AVGO GOOGL SPCX MU MRVL AMD ANET AMAT META RTX NFLX RBRK AVAV"

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

# ── Step: Copy rebuilt stock pages into dist/stocks/ for readthesignal.net ──
stockSrc="dist/stock/stock"
stockDst="dist/stocks"
if [ -d "$stockSrc" ]; then
  rm -rf "$stockDst"
  cp -r "$stockSrc" "$stockDst"
  echo "  ✅ Fresh stock pages copied to dist/stocks/" | tee -a "$LOG"
fi
# Copy stock CSS/JS
if [ -d "dist/stock/css" ]; then
  cp dist/stock/css/*.css dist/css/ 2>/dev/null || true
fi
if [ -d "dist/stock/js" ]; then
  cp dist/stock/js/*.js dist/js/ 2>/dev/null || true
fi

echo "  🌐 Stock pages ready at dist/stocks/"

# ── Step: Deploy if requested ──
if $DEPLOY; then
  echo "Deploying to Vercel..." | tee -a "$LOG"
  cd /home/chino/thesignal && . scripts/deploy-helper.sh && signal_deploy "readthesignal.net" 2>&1 | tee -a "$LOG" || {
    echo "  ❌ Deploy FAILED" | tee -a "$LOG"
    exit 1
  }
  echo "  ✅ Deployed to Vercel" | tee -a "$LOG"
fi

echo "=== Done at $(date '+%Y-%m-%d %H:%M:%S') ===" | tee -a "$LOG"
echo "" >> "$LOG"
