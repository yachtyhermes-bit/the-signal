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
  # dist/audio and dist/img hold file-level symlinks into public/{audio,img}, which
  # signal_strip has just moved away. Copied verbatim they are dangling, and the Vercel
  # archiver dies on them with
  #   ENOENT: no such file or directory, lstat '/tmp/signal-dist/audio/<file>.mp3'
  # — after "[DEPLOY] Complete" is printed, so the deploy silently never happens and the
  # domain keeps serving the previous build. Strip the broken links from the COPY only;
  # dist/ itself is left alone.
  find /tmp/signal-dist -xtype l -delete 2>/dev/null || true
  # vercel.json MUST ship with every deploy — it carries the SEO legacy 301
  # redirects (/stock/, /art/, /hiv) + trailingSlash canonical enforcement.
  # Deploying dist alone silently drops routes (deploy-race, see
  # references/deploy-races.md) and re-opens duplicate-URL indexing.
  if [ -f "$SIGNAL_ROOT/vercel.json" ]; then
    cp "$SIGNAL_ROOT/vercel.json" /tmp/signal-dist/vercel.json
  fi
  cd /tmp/signal-dist

  # Ensure we deploy to the correct Vercel project (not auto-created signal-dist)
  rm -rf .vercel
  npx vercel link --project the-signal --yes > /dev/null 2>&1

  echo "  [DEPLOY] Vercel prod..."
  # `local OUT=$(...)` swallows the exit status, so capture it explicitly: without this a
  # failed Vercel run still printed "[DEPLOY] Complete" and exited 0 while the alias never
  # moved (silent failure — the live site kept serving the previous build).
  local OUT
  if ! OUT=$(npx vercel --prod --archive=tgz --yes 2>&1); then
    echo "$OUT" | tail -8
    echo "  [DEPLOY] FAILED: vercel exited non-zero — nothing was published."
    cd "$SIGNAL_ROOT"
    return 1
  fi
  echo "$OUT" | tail -5

  if [ -n "$ALIAS" ]; then
    local URL=$(echo "$OUT" | grep -oP 'https://[a-z0-9-]+\.vercel\.app' | head -1)
    if [ -z "$URL" ]; then
      echo "  [DEPLOY] FAILED: no deployment URL in vercel output."
      cd "$SIGNAL_ROOT"
      return 1
    fi
    echo "  [ALIAS] $ALIAS"
    local ALIASOUT=$(npx vercel alias set "$URL" "$ALIAS" 2>&1)
    echo "$ALIASOUT" | tail -3
    if ! echo "$ALIASOUT" | grep -qi 'success'; then
      echo "  [DEPLOY] FAILED: alias $ALIAS was not moved — $URL is live but the domain still serves the old build."
      cd "$SIGNAL_ROOT"
      return 1
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
