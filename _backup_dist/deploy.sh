#!/bin/bash
# One-command deploy: build → sync → push to Vercel
# Source of truth is _backup_dist/ for CSS/JS

set -e
cd "$(dirname "$0")"

echo "🔨 Building from _backup_dist/..."
node build.js

echo "📦 Syncing dist/ → /tmp/vercel-deploy/..."
rm -rf /tmp/vercel-deploy
cp -r dist /tmp/vercel-deploy

# Copy Vercel project config so it deploys to correct project (the-signal)
if [ -d ".vercel" ] && [ -f ".vercel/project.json" ]; then
  cp -r .vercel /tmp/vercel-deploy/.vercel
  echo "  ✅ .vercel/ project config copied"
fi
if [ -f "vercel.json" ]; then
  cp vercel.json /tmp/vercel-deploy/vercel.json
  echo "  ✅ vercel.json copied"
fi

echo "🚀 Deploying to Vercel (production)..."
cd /tmp/vercel-deploy
vercel --prod --yes --archive=tgz

echo "✅ Deployed to https://readthesignal.net"
