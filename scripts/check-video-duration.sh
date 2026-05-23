#!/bin/bash
# check-video-duration.sh
# Verifies a YouTube video is under 20 minutes before embedding in The Signal
# Usage: bash scripts/check-video-duration.sh VIDEO_ID
# Returns: exit 0 + "OK: Video <title> is 4m12s" | exit 1 + "REJECT: ..."

VIDEO_ID="$1"
MAX_SECONDS=1200  # 20 minutes

if [ -z "$VIDEO_ID" ]; then
  echo "Usage: $0 VIDEO_ID"
  echo "Example: $0 h6MuGS51Iic"
  exit 1
fi

# Fetch the watch page and extract lengthSeconds from YouTube's embedded data
HTML=$(curl -s "https://www.youtube.com/watch?v=$VIDEO_ID" 2>/dev/null)

# Extract duration from ytInitialPlayerResponse
DURATION=$(echo "$HTML" | grep -oP '"lengthSeconds":"\K[0-9]+' | head -1)

# Fallback: try ytInitialData
if [ -z "$DURATION" ]; then
  DURATION=$(echo "$HTML" | grep -oP '"approxDurationMs":"\K[0-9]+' | head -1)
  if [ -n "$DURATION" ]; then
    DURATION=$((DURATION / 1000))
  fi
fi

# Fallback: extract from meta itemprop="duration"
if [ -z "$DURATION" ]; then
  ISO_DURATION=$(echo "$HTML" | grep -oP 'itemprop="duration" content="\K[^"]+' | head -1)
  if [ -n "$ISO_DURATION" ]; then
    # Parse ISO 8601 duration like PT16M20S or PT1H3M
    HOURS=0; MINUTES=0; SECONDS=0
    [[ "$ISO_DURATION" =~ ([0-9]+)H ]] && HOURS="${BASH_REMATCH[1]}"
    [[ "$ISO_DURATION" =~ ([0-9]+)M ]] && MINUTES="${BASH_REMATCH[1]}"
    [[ "$ISO_DURATION" =~ ([0-9]+)S ]] && SECONDS="${BASH_REMATCH[1]}"
    DURATION=$((HOURS * 3600 + MINUTES * 60 + SECONDS))
  fi
fi

# Get title for output
TITLE=$(echo "$HTML" | grep -oP '<title>\K[^<]+' | head -1 | sed 's/ - YouTube//')

if [ -z "$DURATION" ]; then
  # If we can't parse duration, check the title for clues
  if echo "$TITLE" | grep -qiP '(keynote|full show|full episode|podcast|marathon)'; then
    echo "REJECT: Cannot determine duration but title suggests long content: '$TITLE'"
    exit 1
  fi
  echo "WARN: Could not determine duration for $VIDEO_ID ('$TITLE') — verify manually"
  exit 2
fi

# Format for display
MIN=$((DURATION / 60))
SEC=$((DURATION % 60))
FORMATTED="${MIN}m${SEC}s"

if [ "$DURATION" -gt "$MAX_SECONDS" ]; then
  MINS=$((DURATION / 60))
  echo "REJECT: Video '$TITLE' is ${FORMATTED} (${MINS}min) — exceeds ${MAX_SECONDS}s max (20 min)"
  exit 1
elif [ "$DURATION" -lt 120 ]; then
  echo "REJECT: Video '$TITLE' is only ${FORMATTED} — too short, needs at least 2 min"
  exit 1
else
  echo "OK: Video '$TITLE' is ${FORMATTED} ✅"
  exit 0
fi
