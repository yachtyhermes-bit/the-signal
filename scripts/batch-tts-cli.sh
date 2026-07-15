#!/bin/bash
# Batch generate TTS for missing articles using edge-tts CLI
# Saves progress so it can be resumed

ROOT="/home/chino/thesignal"
POSTS_DIR="$ROOT/articles/posts"
TMP_DIR="/tmp/signal-tts"
PROGRESS_FILE="/tmp/signal-tts-prog.txt"
VOICE="en-US-AndrewNeural"

mkdir -p "$TMP_DIR"

START_FROM=0
if [ -f "$PROGRESS_FILE" ]; then
    START_FROM=$(cat "$PROGRESS_FILE")
fi

# Get all article JSON files
FILES=("$POSTS_DIR"/*.json)
TOTAL=${#FILES[@]}

echo "Total articles: $TOTAL, starting from index: $START_FROM" >&2

OK=0
SKIP=0
FAIL=0

for ((i=START_FROM; i<TOTAL; i++)); do
    jf="${FILES[$i]}"
    
    # Get slug
    slug=$(python3 -c "import json; print(json.load(open('$jf')).get('slug',''))")
    [ -z "$slug" ] && continue
    
    out="$TMP_DIR/$slug.mp3"
    
    # Skip if already exists and valid
    if [ -f "$out" ] && [ $(stat -c%s "$out") -gt 500 ]; then
        SKIP=$((SKIP + 1))
        continue
    fi
    
    # Extract text
    text=$(python3 -c "
import json, re
a = json.load(open('$jf'))
title = a.get('title','')
body = a.get('bodyHtml','')
if body:
    text = re.sub(r'<[^>]+>', ' ', body)
    for a,b in [('&amp;','&'),('&lt;','<'),('&gt;','>'),('&quot;','\"'),('&#39;',\"'\"),('&nbsp;',' ')]:
        text = text.replace(a,b)
    text = re.sub(r'\s+', ' ', text).strip()
    text = f'{title}. {text}'
else:
    text = f'{title}. {a.get(\"summary\",\"\")}'
print(text[:5000])
")
    
    [ ${#text} -lt 50 ] && { SKIP=$((SKIP + 1)); continue; }
    
    # Generate TTS
    echo "$text" | edge-tts --voice "$VOICE" --write-media "$out" --rate +0% 2>/dev/null
    ec=$?
    
    if [ $ec -eq 0 ] && [ -f "$out" ] && [ $(stat -c%s "$out") -gt 500 ]; then
        OK=$((OK + 1))
    else
        FAIL=$((FAIL + 1))
        [ -f "$out" ] && rm "$out"
    fi
    
    # Save progress every 5
    if [ $((i % 5)) -eq 0 ] || [ $i -eq $((TOTAL - 1)) ]; then
        echo $((i + 1)) > "$PROGRESS_FILE"
        echo "[$((i+1))/$TOTAL] ok=$OK skip=$SKIP fail=$FAIL" >&2
    fi
done

echo "DONE: OK=$OK Skip=$SKIP Fail=$FAIL" >&2
MP3_COUNT=$(ls "$TMP_DIR"/*.mp3 2>/dev/null | wc -l)
echo "Total MP3 files: $MP3_COUNT" >&2
