#!/bin/bash
set -e
cd /home/chino/thesignal
# Clear placeholder tracking
rm -f /tmp/placeholder-articles.txt

echo '=== SIGNAL DEPLOY PIPELINE ==='
echo ''

# Phase 1: Static Checks
echo '📋 Phase 1: Static Checks'
echo -n '  CJK scan... '
python3 -c "
import json, os, re
errors=[]
for f in sorted(os.listdir('articles/posts')):
    if not f.endswith('.json'): continue
    a = json.load(open(f'articles/posts/{f}'))
    body = a.get('bodyHtml', '')
    cjk = re.findall(r'[\u4e00-\u9fff\u3400-\u4dbf\uf900-\ufaff]', body)
    if cjk: errors.append(a.get('slug',f))
if errors:
    for s in errors: print(f'  CJK in {s}')
    exit(1)
" && echo '✅' || { echo '❌'; exit 1; }

echo -n '  Literal \n scan... '
python3 -c "
import json, os
errors=[]
for f in sorted(os.listdir('articles/posts')):
    if not f.endswith('.json'): continue
    a = json.load(open(f'articles/posts/{f}'))
    if '\\\\n' in a.get('bodyHtml',''): errors.append(a.get('slug',f))
if errors:
    for s in errors: print(f'  \\n in {s}')
    exit(1)
" && echo '✅' || { echo '❌'; exit 1; }

echo -n '  YouTube videos... '
errors=0
for f in articles/posts/*.json; do
  python3 -c "
import json, urllib.request, sys
a = json.load(open('$f'))
for i, v in enumerate(a.get('videos', [])):
    vid = v['url'].split('v=')[-1].split('&')[0]
    try:
        req = urllib.request.Request(f'https://www.youtube.com/oembed?url=https://www.youtube.com/watch?v={vid}&format=json', headers={'User-Agent': 'Mozilla/5.0'})
        urllib.request.urlopen(req, timeout=5)
    except:
        sys.exit(1)
" 2>/dev/null || { errors=1; echo "    ❌ Dead video in '$f'"; }
done
[ "$errors" = "0" ] && echo '✅' || { echo '❌'; exit 1; }

echo -n '  Images... '
python3 -c "
from PIL import Image, ImageDraw, ImageFont
import json, os, sys

generated = 0
placeholders = []
fonts = []
for p in ['/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf']:
    if os.path.exists(p): fonts.append(p)

for f in sorted(os.listdir('articles/posts')):
    if not f.endswith('.json'): continue
    a = json.load(open(f'articles/posts/{f}'))
    img = a.get('image', {})
    if not isinstance(img, dict): continue
    src = img.get('src', '')
    if not src.startswith('/img/'): continue
    path = f'public{src}'
    webp = path.rsplit('.',1)[0]+'.webp'
    if os.path.exists(path) and os.path.exists(webp): continue
    # Missing — generate placeholder
    slug = a.get('slug', f.replace('.json',''))
    ticker = a.get('ticker', '???')
    title = a.get('title', 'Signal')
    im = Image.new('RGB', (1200, 675), '#0f0f20')
    draw = ImageDraw.Draw(im)
    # Subtle gradient
    for y in range(675):
        r = int(15 + 5*(y/675)); g = int(15 + 5*(y/675)); b = int(32 + 8*(y/675))
        draw.line([(0,y),(1199,y)], fill=(r,g,b))
    # Load fonts
    try:
        font_big = ImageFont.truetype(fonts[0], 42) if fonts else ImageFont.load_default()
        font_sm = ImageFont.truetype(fonts[1], 24) if len(fonts)>1 else font_big
    except:
        font_big = ImageFont.load_default(); font_sm = font_big
    # Ticker badge
    lbl = f'\${ticker}'
    bb = draw.textbbox((0,0), lbl, font=font_big)
    bx, by = 50, 50
    draw.rounded_rectangle([bx-12, by-8, bx+bb[2]-bb[0]+12, by+bb[3]-bb[1]+8], 8, fill='#3b82f6')
    draw.text((bx, by), lbl, fill='white', font=font_big)
    # Title wrapped
    y = 170
    words = title.split()
    line = ''
    for w in words:
        tst = line + ' ' + w if line else w
        bb = draw.textbbox((0,0), tst, font=font_sm)
        if bb[2] - bb[0] > 1100:
            draw.text((50, y), line, fill='#d0d0e0', font=font_sm)
            y += 34; line = w
        else: line = tst
    if line: draw.text((50, y), line, fill='#d0d0e0', font=font_sm)
    draw.text((50, 570), 'THE SIGNAL', fill='#3b82f6', font=font_sm)
    im.save(path, 'JPEG', quality=88)
    im.save(webp, 'WEBP', quality=88)
    print(f'    🖼️ Generated: {src}', flush=True)
    generated += 1
    placeholders.append(slug)
if generated > 0:
    print(f'  ✅ {generated} missing images auto-generated')
else:
    print('✅')
# Write placeholder slugs for Phase 4 image hunt
with open('/tmp/placeholder-articles.txt', 'w') as ph:
    for s in placeholders:
        ph.write(s + '\n')
" && echo '' || { echo '  ❌ Image generation failed'; exit 1; }

# Phase 1.5: Refresh Data
echo ''
echo '📊 Phase 1.5: Refresh Data'
echo -n '  Fetching live prices... '
node scripts/fetch-prices.js && echo '  ✅ Prices refreshed' || echo '  ⚠️  Price fetch failed'
echo -n '  yfinance scorecard refresh... '
python3 scripts/refresh-scorecard.py && echo '  ✅ Scorecard refreshed' || echo '  ⚠️  Scorecard refresh failed (using fallback)'
echo -n '  yfinance highlights refresh... '
python3 scripts/refresh-highlights.py && echo '  ✅ Highlights refreshed' || echo '  ⚠️  Highlights refresh failed (using fallback)'

# Phase 2: Build
echo ''
echo '🔨 Phase 2: Build'
node build.js && echo '  ✅ Build success' || { echo '  ❌ Build failed'; exit 1; }

# Phase 3: Deploy (strip large assets, deploy, restore, alias)
echo ''
echo '🚀 Phase 3: Deploy'
cd /home/chino/thesignal
source scripts/deploy-helper.sh
signal_deploy "readthesignal.net" || { echo '  ❌ Deploy failed'; exit 1; }
echo '  ✅ Deployed to https://readthesignal.net'

# Phase 4: Replace placeholder images with real ones
echo ''
echo '📸 Phase 4: Replace Placeholder Images'
bash scripts/fetch-missing-images.sh || echo '  ⚠️  Image fetch had warnings (non-fatal)'

echo ''
echo '✅ PIPELINE COMPLETE'
