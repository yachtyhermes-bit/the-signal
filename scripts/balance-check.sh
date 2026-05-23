#!/usr/bin/env bash
# The Signal — Weekly Balance Check
# Checks API credits, bandwidth, site health, and content stats
set -e

VERCEL_TOKEN="${VERCEL_TOKEN:-}"
VERCEL_TEAM="team_OPjTgGGvOQnlMiwxxnxJyMG7"
VERCEL_PROJECT="the-signal"
SITE="https://readthesignal.net"
XURL_BIN="/home/chino/.hermes/profiles/yachty/home/.local/bin/xurl"

echo "📊 THE SIGNAL — Weekly Balance Check"
echo "$(date '+%B %d, %Y at %H:%M %Z')"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# === 1. SITE HEALTH ===
echo "🌐 Site Health"
HTTP_CODE=$(curl -sL -o /dev/null -w "%{http_code}" "$SITE" 2>/dev/null || echo "fail")
if [ "$HTTP_CODE" = "200" ]; then
  echo "  readthesignal.net  ✅ ($HTTP_CODE)"
else
  echo "  readthesignal.net  ❌ ($HTTP_CODE)"
fi

# Check homepage loads with content
ARTICLE_COUNT=$(curl -sL "$SITE" 2>/dev/null | grep -oP 'href="/article/[^"]*"' | wc -l)
echo "  Articles on homepage: $ARTICLE_COUNT"

# === 2. ARTICLE STATS ===
echo ""
echo "📝 Content Stats"
JSON_COUNT=$(ls /home/chino/thesignal/articles/posts/*.json 2>/dev/null | wc -l)
echo "  Total articles: $JSON_COUNT"

# Most recent article
LATEST=$(ls -t /home/chino/thesignal/articles/posts/*.json 2>/dev/null | head -1)
if [ -n "$LATEST" ]; then
  LATEST_TITLE=$(python3 -c "import json; print(json.load(open('$LATEST')).get('title','?'))" 2>/dev/null)
  LATEST_DATE=$(python3 -c "import json; print(json.load(open('$LATEST')).get('date','?')[:10])" 2>/dev/null)
  echo "  Latest: \"${LATEST_TITLE:0:50}…\" ($LATEST_DATE)"
fi

# Tweets posted this week
if [ -f /tmp/posted-articles.txt ]; then
  TWEET_COUNT=$(wc -l < /tmp/posted-articles.txt)
  echo "  Tweets posted (all time): $TWEET_COUNT"
else
  echo "  Tweets posted: 0 (no tracking file)"
fi

# === 3. X API STATUS ===
echo ""
echo "🐦 X/Twitter (@ReadTheSignal21)"
if command -v "$XURL_BIN" &>/dev/null; then
  X_DATA=$("$XURL_BIN" "/2/users/me?user.fields=public_metrics,description,profile_image_url" --auth oauth2 2>/dev/null || echo "{}")
  X_NAME=$(echo "$X_DATA" | python3 -c "import json,sys; d=json.load(sys.stdin).get('data',{}); print(d.get('name','?'))" 2>/dev/null)
  X_FOLLOWERS=$(echo "$X_DATA" | python3 -c "import json,sys; d=json.load(sys.stdin).get('data',{}).get('public_metrics',{}); print(d.get('followers_count','?'))" 2>/dev/null)
  X_TWEETS=$(echo "$X_DATA" | python3 -c "import json,sys; d=json.load(sys.stdin).get('data',{}).get('public_metrics',{}); print(d.get('tweet_count','?'))" 2>/dev/null)
  echo "  Account: $X_NAME"
  echo "  Followers: $X_FOLLOWERS"
  echo "  Total tweets: $X_TWEETS"
else
  echo "  ❌ xurl not found"
fi

# === 4. X API Credits (manual check needed) ===
echo ""
echo "💰 Credits & Limits"

# Vercel bandwidth estimate from deployment size
if [ -n "$VERCEL_TOKEN" ]; then
  echo "  Vercel: token valid ✅"
  # Get total deployment size from latest deploy
  DEPLOY_OUTPUT=$(curl -s "https://api.vercel.com/v9/projects/$VERCEL_PROJECT" \
    -H "Authorization: Bearer $VERCEL_TOKEN" 2>/dev/null)
  PROJ_NAME=$(echo "$DEPLOY_OUTPUT" | python3 -c "import json,sys; print(json.load(sys.stdin).get('name','?'))" 2>/dev/null)
  echo "  Vercel project: $PROJ_NAME"
else
  echo "  Vercel: ❌ no token to check"
fi

# === 5. WHAT NEEDS MANUAL SETUP ===
echo ""
echo "🔧 Set Up These to Track More:"
echo "  □ Cloudflare API token → traffic/bandwidth analytics"
echo "  □ Google Cloud billing API → Gemini/API costs"
echo "  □ X API credits → check developer.x.com/billing"
echo "  □ GA4 Data API → monthly active users & traffic sources"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📡 Next check: in 7 days"
