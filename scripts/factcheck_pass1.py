#!/usr/bin/env python3
"""Pass 1: Identify the 10 most recent articles, validate schemas, run spell-check, check disclosures."""
import json, glob, os, re, html, subprocess

os.chdir('/home/chino/thesignal')

files = sorted(glob.glob('articles/posts/*.json'))
arts = [(json.load(open(f)), f) for f in files]
arts.sort(key=lambda x: x[0]['date'], reverse=True)

REQUIRED = ['slug','ticker','sector','sentiment','date','title','subtitle','summary','price','bodyHtml','tags','links']

print("=" * 80)
print("PASS 1: 10 MOST RECENT ARTICLES")
print("=" * 80)

for a, f in arts[:10]:
    slug = a.get('slug', '?')
    ticker = a.get('ticker', '?')
    title = a.get('title', '?')[:60]
    date = a.get('date', '?')[:19]
    price = a.get('price', 'MISSING')
    
    print(f"\n{'─'*60}")
    print(f"📄 {date} | {ticker:6s} | ${price if price != 'MISSING' else '???'}")
    print(f"   Slug: {slug}")
    print(f"   Title: {title}")
    
    # Schema validation
    missing = [k for k in REQUIRED if k not in a or a[k] is None]
    if missing:
        print(f"   ❌ MISSING FIELDS: {missing}")
    else:
        print(f"   ✅ Schema complete")
    
    # Links check
    links = a.get('links', [])
    if not links:
        print(f"   ⚠️  No links")
    else:
        has_label = all('label' in l for l in links)
        has_text = any('text' in l for l in links)
        if has_text and not has_label:
            print(f"   ❌ Links use 'text' instead of 'label': {[l.get('text','?') for l in links]}")
        else:
            print(f"   ✅ {len(links)} links with labels")
    
    # Videos check
    videos = a.get('videos', [])
    for v in videos:
        vid_id = v.get('id', v.get('embed', ''))
        if 'dQw4w9WgXcQ' in str(vid_id):
            print(f"   ❌ RICKROLL PLACEHOLDER video!")
        missing_vf = [k for k in ['id','title','source','url','position'] if k not in v]
        if missing_vf:
            print(f"   ⚠️  Video missing fields: {missing_vf}")
        if 'embed' in v and 'id' not in v:
            print(f"   ⚠️  Video uses 'embed' format instead of 'id'")
    
    # Disclosure check
    body = a.get('bodyHtml', '')
    has_pmc = 'Positions may change.' in body
    has_advice = 'not financial advice' in body
    ticker_in_disc = f'in {ticker}' in body[-300:] or f'in ${ticker}' in body[-300:]
    
    if has_pmc and has_advice:
        print(f"   ✅ Disclosure complete")
    else:
        if not has_pmc:
            print(f"   ❌ Missing 'Positions may change.'")
        if not has_advice:
            print(f"   ❌ Missing 'not financial advice'")
    
    # Check $TICKER prefix in disclosure
    if re.search(r'\$' + re.escape(ticker), body):
        print(f"   ⚠️  Dollar-sign prefixed ticker found: ${ticker}")
    
    # Image check
    img = a.get('image', {})
    if isinstance(img, dict) and img.get('src'):
        local_path = f"public{img['src']}"
        if os.path.exists(local_path):
            size_kb = os.path.getsize(local_path) / 1024
            print(f"   ✅ Image exists: {img['src']} ({size_kb:.0f}KB)")
        else:
            # Check R2
            r2_path = f"https://pub-4b6ad449790f433c8b0fde9b167147c9.r2.dev{img['src']}"
            print(f"   ⚠️  Local image missing: {img['src']} (expect R2)")
    elif isinstance(img, str):
        print(f"   ❌ Image is a string, not object: {img}")
    else:
        print(f"   ❌ Image src missing")
    
    # Date collision check
    print(f"   ℹ️  Date: {date}")

# Date collision check
print(f"\n{'═'*80}")
print("DATE COLLISION CHECK (top 10)")
print(f"{'═'*80}")
dates = {}
for a, f in arts[:10]:
    d = a['date'][:19]
    dates.setdefault(d, []).append(a['slug'])
for d, slugs in sorted(dates.items()):
    if len(slugs) > 1:
        print(f"  ❌ COLLISION: {d} — {len(slugs)} articles: {slugs}")

# Aspell check
print(f"\n{'═'*80}")
print("SPELL CHECK (aspell)")
print(f"{'═'*80}")

try:
    subprocess.run(['aspell', '--version'], capture_output=True, timeout=5)
    aspell_ok = True
except:
    print("aspell not available — installing...")
    subprocess.run(['sudo', 'apt-get', 'install', '-y', 'aspell', 'aspell-en'], capture_output=True, timeout=60)
    aspell_ok = True

for a, f in arts[:10]:
    slug = a.get('slug', '?')
    body = a.get('bodyHtml', '')
    
    # Strip HTML
    text = re.sub(r'<[^>]+>', ' ', body)
    text = html.unescape(text)
    text = re.sub(r'\s+', ' ', text).strip()
    
    try:
        result = subprocess.run(
            ['aspell', 'list', '--lang=en_US', '--encoding=utf-8'],
            input=text, capture_output=True, text=True, timeout=30
        )
        errors = set()
        for w in result.stdout.strip().split('\n'):
            w = w.strip().strip(".,!?;:'\"()[]{}")
            if not w or len(w) < 3: continue
            if w.isupper() and len(w) <= 6: continue  # tickers
            if w[0].isupper() and len(w) > 1: continue  # proper nouns
            if any(x in w.lower() for x in ('scale', 'compute', 'backlog', 'moat', 'hyperscal', 'attrit', 'lithography')):
                continue
            errors.add(w)
        
        if errors:
            print(f"\n  ❌ {slug}: {len(errors)} possible errors: {', '.join(sorted(errors))}")
        else:
            print(f"  ✅ {slug}: Clean")
    except Exception as e:
        print(f"  ⚠️  {slug}: spell check error: {e}")

# Check for "rerat" specifically
print(f"\n{'═'*80}")
print("GARBLED TEXT CHECKS")
print(f"{'═'*80}")
for a, f in arts[:10]:
    slug = a.get('slug', '?')
    body = a.get('bodyHtml', '')
    ticker = a.get('ticker', '?')
    
    issues = []
    
    # "rerat" without trailing e
    if re.search(r'\brerat\b', body):
        issues.append('"rerat" (should be "rerate")')
    
    # Dollar-sign tickers
    dollar_hits = re.findall(r'\$[A-Z]{1,5}', body)
    legit_dollar = {f'${ticker}', '$TICKER'}
    suspicious = [d for d in dollar_hits if d not in legit_dollar]
    if suspicious:
        issues.append(f'Suspicious $TICKER: {suspicious}')
    
    if issues:
        print(f"  ⚠️  {slug}: {'; '.join(issues)}")
    else:
        print(f"  ✅ {slug}: Clean")

print(f"\n{'═'*80}")
print("DONE — Proceed to Pass 2")
