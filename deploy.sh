#!/bin/bash
# deploy.sh — Full Signal deploy: Jenny TTS pre-generation → build → Vercel deploy
set -e
cd "$(dirname "$0")"

echo "═══════════════════════════════════════════"
echo "🚀 The Signal Deploy Pipeline"
echo "═══════════════════════════════════════════"

# Source env vars for R2 access
if [ -f .dev.vars ]; then
  set -a; source .dev.vars; set +a
  echo "📦 Env vars loaded from .dev.vars"
fi

# Step 1: Pre-generate missing Jenny TTS for recently modified articles
echo ""
echo "━━━ Step 1: Jenny TTS pre-generation (recent articles) ━━━"
python3 -u scripts/prebuild-tts.py --recent 48
echo ""

# Step 2: Build
echo "━━━ Step 2: Build ━━━"
node build.js
echo ""

# Step 3: Deploy
echo "━━━ Step 3: Deploy to Vercel ━━━"
npx vercel --prod --token "$(cat /home/chino/.vercel/token)" --force
echo ""
echo "═══════════════════════════════════════════"
echo "✅ Deploy complete — https://readthesignal.net"
echo "═══════════════════════════════════════════"
