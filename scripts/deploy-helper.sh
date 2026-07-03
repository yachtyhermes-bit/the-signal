#!/bin/bash
# deploy-helper.sh — Vercel deploy with R2 architecture (strip/restore pattern)
# Source this: source scripts/deploy-helper.sh
# Then call: signal_deploy
#
# Architecture: images/audio/video/cf-worker live on Cloudflare R2, NOT in dist/.
# Vercel has a 100MB cap. We strip large assets before deploy, restore after.
#
# For R2 uploads (images/audio), use the separate helper:
#   python3 scripts/r2_upload.py hero <slug>
#   python3 scripts/r2_upload.py tts <slug>
#   python3 scripts/r2_upload.py file <local_path> <r2_key>

set -e

SIGNAL_ROOT="/home/chino/thesignal"
BAK="/tmp/_signal_bak"

signal_strip() {
  cd "$SIGNAL_ROOT"
  echo "  [STRIP] Before deploy..."
  [ -d public/audio ]  && mv public/audio  "${BAK}_audio" 2>/dev/null
  [ -d public/img ]    && mv public/img    "${BAK}_img"   2>/dev/null
  [ -d public/video ]  && mv public/video  "${BAK}_video" 2>/dev/null
  [ -d cf-worker ]     && mv cf-worker     "${BAK}_cfw"   2>/dev/null
  echo "  [STRIP] Done"
}

signal_restore() {
  cd "$SIGNAL_ROOT"
  echo "  [RESTORE] After deploy..."
  [ -d "${BAK}_audio" ]  && mv "${BAK}_audio"  public/audio 2>/dev/null
  [ -d "${BAK}_img" ]    && mv "${BAK}_img"    public/img   2>/dev/null
  [ -d "${BAK}_video" ]  && mv "${BAK}_video"  public/video 2>/dev/null
  [ -d "${BAK}_cfw" ]    && mv "${BAK}_cfw"    cf-worker   2>/dev/null
  echo "  [RESTORE] Done"
}

signal_deploy() {
  local ALIAS="$1"  # optional: "readthesignal.net"
  signal_strip
  trap signal_restore EXIT

  if [ ! -d dist ]; then
    echo "  [BUILD] Rebuilding..."
    node build.js
  fi

  rm -rf /tmp/signal-dist
  cp -r dist /tmp/signal-dist
  cd /tmp/signal-dist

  echo "  [DEPLOY] Vercel prod..."
  local OUT=$(npx vercel --prod --yes 2>&1)
  echo "$OUT" | tail -5

  if [ -n "$ALIAS" ]; then
    local URL=$(echo "$OUT" | grep -oP 'https://[a-z0-9-]+\.vercel\.app' | head -1)
    if [ -n "$URL" ]; then
      echo "  [ALIAS] $ALIAS"
      npx vercel alias set "$URL" "$ALIAS" 2>&1 | tail -3
    fi
  fi

  cd "$SIGNAL_ROOT"
  echo "  [DEPLOY] Complete"
}

# R2 upload — delegates to Python helper
signal_upload_hero() {
  python3 "$SIGNAL_ROOT/scripts/r2_upload.py" hero "$1"
}

signal_upload_tts() {
  python3 "$SIGNAL_ROOT/scripts/r2_upload.py" tts "$1"
}

signal_upload_file() {
  python3 "$SIGNAL_ROOT/scripts/r2_upload.py" file "$1" "$2"
}

echo "[deploy-helper] Loaded: signal_deploy, signal_upload_hero, signal_upload_tts, signal_upload_file"
