#!/bin/bash
set -e
cd /home/chino/thesignal

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
import json, os, sys
errors=[]
for f in sorted(os.listdir('articles/posts')):
    if not f.endswith('.json'): continue
    a = json.load(open(f'articles/posts/{f}'))
    img = a.get('image', {})
    if isinstance(img, dict):
        src = img.get('src', '')
        if src.startswith('/img/'):
            path = f'public{src}'
            if not os.path.exists(path):
                errors.append(f'Missing: {path}')
            webp = path.rsplit('.',1)[0]+'.webp'
            if not os.path.exists(webp):
                errors.append(f'Missing WebP: {webp}')
if errors:
    for e in errors: print(f'  {e}')
    exit(1)
" && echo '✅' || { echo '❌'; exit 1; }

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

# Phase 3: Deploy
echo ''
echo '🚀 Phase 3: Deploy'
vercel --prod && echo '  ✅ Deployed to https://readthesignal.net' || { echo '  ❌ Deploy failed'; exit 1; }

echo ''
echo '✅ PIPELINE COMPLETE'
