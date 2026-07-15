#!/bin/bash
# Parallel batch TTS generation using xargs -P
# Each article generates via edge-tts CLI

ROOT="/home/chino/thesignal"
POSTS_DIR="$ROOT/articles/posts"
TMP_DIR="/tmp/signal-tts"
VOICE="en-US-AndrewNeural"
PARALLEL=4

mkdir -p "$TMP_DIR"

echo "Building article list..." >&2

# Create a temp dir for per-article text files
TEXT_DIR="/tmp/signal-tts-texts"
mkdir -p "$TEXT_DIR"

# Build list of articles that need TTS
TODO="/tmp/signal-tts-todo.txt"
: > "$TODO"

for jf in "$POSTS_DIR"/*.json; do
    slug=$(python3 -c "import json; print(json.load(open('$jf')).get('slug',''))")
    [ -z "$slug" ] && continue
    
    out="$TMP_DIR/$slug.mp3"
    if [ -f "$out" ] && [ $(stat -c%s "$out") -gt 500 ]; then
        continue
    fi
    
    # Extract text to file for edge-tts
    text_file="$TEXT_DIR/$slug.txt"
    python3 -c "
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
with open('$text_file', 'w') as f:
    f.write(text[:5000])
" 2>/dev/null
    
    echo "$slug" >> "$TODO"
done

TOTAL=$(wc -l < "$TODO")
echo "Articles to generate: $TOTAL" >&2
if [ "$TOTAL" -eq 0 ]; then
    echo "All articles already generated!" >&2
    exit 0
fi

# Define the worker function
do_gen() {
    slug="$1"
    text_file="/tmp/signal-tts-texts/$slug.txt"
    out="/tmp/signal-tts/$slug.mp3"
    
    if [ ! -f "$text_file" ]; then
        echo "FAIL no_text $slug" >&2
        exit 1
    fi
    
    edge-tts --voice "$VOICE" -f "$text_file" --write-media "$out" 2>/dev/null
    
    if [ $? -eq 0 ] && [ -f "$out" ] && [ $(stat -c%s "$out") -gt 500 ]; then
        echo "OK $slug" >&2
        rm "$text_file"
        exit 0
    else
        [ -f "$out" ] && rm "$out"
        echo "FAIL $slug" >&2
        exit 1
    fi
}

export -f do_gen
export VOICE TMP_DIR TEXT_DIR

echo "Starting generation with $PARALLEL workers..." >&2
cat "$TODO" | xargs -P "$PARALLEL" -I{} bash -c 'do_gen "{}"' 2>&1

echo "" >&2
MP3_COUNT=$(ls "$TMP_DIR"/*.mp3 2>/dev/null | wc -l)
echo "Done! Total MP3 files: $MP3_COUNT" >&2
