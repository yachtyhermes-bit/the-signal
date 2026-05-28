#!/bin/bash
# Phase 4: Fetch real images for placeholder articles
# Reads /tmp/placeholder-articles.txt and tries to source real images
set -e
cd /home/chino/thesignal

PH_FILE="/tmp/placeholder-articles.txt"
REBUILD=false

if [ ! -s "$PH_FILE" ]; then
  echo '  📋 No placeholder articles to fix — skipping'
  exit 0
fi

echo '  Reading placeholder articles...'
SLUGS=$(cat "$PH_FILE" | tr '\n' ' ')
echo "  Articles needing images: $SLUGS"

# Try to find real images for each article
for slug in $SLUGS; do
  JSON="articles/posts/${slug}.json"
  if [ ! -f "$JSON" ]; then continue; fi

  TICKER=$(python3 -c "import json; print(json.load(open('$JSON')).get('ticker',''))")
  TITLE=$(python3 -c "import json; print(json.load(open('$JSON')).get('title',''))")
  echo "    🔍 Searching for $TICKER — ${TITLE:0:60}..."

  # Strategy 1: Check if YouTube video thumbnail exists for this article
  VIDEO_URL=$(python3 -c "
import json
a = json.load(open('$JSON'))
vids = a.get('videos', [])
if vids:
    url = vids[0].get('url', '')
    if 'v=' in url:
        print(url.split('v=')[-1].split('&')[0])
" 2>/dev/null)

  FOUND=false

  if [ -n "$VIDEO_URL" ]; then
    # Try YouTube maxresdefault thumbnail
    YT_PATH="public/img/articles/${slug}.jpg"
    YT_WEBP="public/img/articles/${slug}.webp"
    if curl -sL -o "$YT_PATH" -w "%{http_code}" "https://img.youtube.com/vi/${VIDEO_URL}/maxresdefault.jpg" 2>/dev/null | grep -q "200"; then
      python3 -c "
from PIL import Image
import sys
try:
    img = Image.open('$YT_PATH')
    img = img.convert('RGB')
    # Crop to 1200x675
    w, h = img.size
    want = 1200/675
    cur = w/h
    if abs(cur - want) > 0.01:
        if cur > want:
            nw = int(h * want)
            x = (w - nw)//2
            img = img.crop((x, 0, x+nw, h))
        else:
            nh = int(w / want)
            y = (h - nh)//2
            img = img.crop((0, y, w, y+nh))
    img = img.resize((1200, 675), Image.LANCZOS)
    img.save('$YT_PATH', 'JPEG', quality=90)
    img.save('$YT_WEBP', 'WEBP', quality=90)
    print('saved')
except Exception as e:
    print(f'err: {e}')
" 2>/dev/null | grep -q "saved" && { echo "      ✅ YouTube thumbnail → saved"; FOUND=true; REBUILD=true; }
    fi
  fi

  # Strategy 2: Google Image search fallback
  if [ "$FOUND" = false ]; then
    python3 << 'PYEOF' 2>/dev/null
import json, os, sys, urllib.request, urllib.parse, re
slug = os.path.basename("'"$slug"'")
ticker = "'"$TICKER"'"
title = "'"$TITLE"'"
query = urllib.parse.quote(f"{ticker} stock company logo news 2026")
url = f"https://www.google.com/search?tbm=isch&q={query}"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
try:
    resp = urllib.request.urlopen(req, timeout=10)
    html = resp.read().decode('utf-8', errors='replace')
    # Extract first image URL from Google Images result
    imgs = re.findall(r'imgurl=([^&]+)', html)
    if imgs:
        img_url = urllib.parse.unquote(imgs[0])
        img_path = f'public/img/articles/{slug}.jpg'
        webp_path = f'public/img/articles/{slug}.webp'
        req2 = urllib.request.Request(img_url, headers={'User-Agent': 'Mozilla/5.0'})
        resp2 = urllib.request.urlopen(req2, timeout=15)
        data = resp2.read()
        if len(data) > 10000:
            with open(img_path, 'wb') as f: f.write(data)
            from PIL import Image
            img = Image.open(img_path).convert('RGB')
            w, h = img.size
            want = 1200/675
            cur = w/h
            if abs(cur - want) > 0.01:
                if cur > want:
                    nw = int(h * want)
                    x = (w - nw)//2
                    img = img.crop((x, 0, x+nw, h))
                else:
                    nh = int(w / want)
                    y = (h - nh)//2
                    img = img.crop((0, y, w, y+nh))
            img = img.resize((1200, 675), Image.LANCZOS)
            img.save(img_path, 'JPEG', quality=90)
            img.save(webp_path, 'WEBP', quality=90)
            sys.exit(0)
    sys.exit(1)
except: sys.exit(1)
PYEOF
    if [ $? -eq 0 ]; then
      echo "      ✅ Google Image found → saved"
      REBUILD=true
    else
      echo "      ⚠️  No real image found — keeping placeholder"
    fi
  fi
done

# If we found any real images, rebuild and redeploy
if [ "$REBUILD" = true ]; then
  echo ''
  echo '  🔄 Real images found — rebuilding and redeploying...'
  node build.js && echo '  ✅ Rebuild success' || { echo '  ❌ Rebuild failed'; exit 1; }
  vercel --prod --token "$(cat /home/chino/.vercel/token 2>/dev/null)" && echo '  ✅ Redeployed to https://readthesignal.net' || { echo '  ❌ Redeploy failed'; exit 1; }
  echo '  ✅ Placeholder images replaced with real images'
else
  echo '  ℹ️  No new real images sourced — placeholders remain'
fi

# Clean up tracking file
rm -f "$PH_FILE"
