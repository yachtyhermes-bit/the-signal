#!/usr/bin/env python3
"""Fact-check + spell-check for the 10 most recent articles."""

import json, os, re, html as html_mod

base = '/home/chino/thesignal/articles/posts'

slugs = [
    'credo-ai-connectivity-chips-2026',
    'smci-ai-server-accounting-comeback-2026',
    'vertiv-ai-data-center-infrastructure-q1-2026',
    'coinbase-european-crypto-moat-2026',
    'coreweave-ai-cloud-sale-2026',
    'kratos-defense-unmanned-systems-hypersonics-2026',
    'vertiv-data-center-infrastructure-2026',
    'axon-ai-policing-monopoly-2026',
    'applied-materials-ai-chip-equipment-monopoly-2026',
    'servicenow-ai-workflow-automation-2026'
]

articles = []
for s in slugs:
    with open(f'{base}/{s}.json') as f:
        a = json.load(f)
        articles.append(a)

# ===== DISCLOSURE CHECK =====
print("=" * 80)
print("DISCLOSURE CHECK")
print("=" * 80)
for a in articles:
    body = a.get('bodyHtml', '')
    ticker = a.get('ticker', '')
    slug = a.get('slug', '')
    
    has_disclosure = '<p class="disclosure">' in body
    has_dollar_ticker = '$' + ticker in body if ticker else False
    
    print(f"\n{slug} ({ticker}):")
    print(f"  Has disclosure element: {has_disclosure}")
    
    if has_disclosure:
        match = re.search(r'<p class="disclosure"><em>(.*?)</em></p>', body)
        if match:
            disc_text = match.group(1)
            print(f"  Disclosure text: {disc_text}")
            if ticker in disc_text:
                print(f"  ✓ Ticker {ticker} found in disclosure")
            else:
                print(f"  ✗ Ticker {ticker} NOT found in disclosure!")
            if 'holds no position' in disc_text and 'financial advice' in disc_text:
                print(f"  ✓ Standard disclosure language present")
            else:
                print(f"  ✗ Non-standard disclosure language")
        else:
            print(f"  ✗ Could not parse disclosure text (regex mismatch)")
    else:
        print(f"  ✗ MISSING DISCLOSURE!")
    
    if has_dollar_ticker:
        print(f"  ⚠️ Dollar-sign prefixed ticker found: ${ticker}")

# ===== WORD COUNT & GARBLED TEXT CHECK =====
print("\n" + "=" * 80)
print("WORD COUNT & TEXT CHECK")
print("=" * 80)
for a in articles:
    body = html_mod.unescape(a.get('bodyHtml', ''))
    slug = a.get('slug', '')
    
    body_text = re.sub(r'<[^>]+>', ' ', body)
    body_text = re.sub(r'\s+', ' ', body_text).strip()
    word_count = len(body_text.split())
    print(f"\n{slug}: {word_count} words")

    # Check for 'rerat' pattern (no trailing e)
    if re.search(r'(?<![a-z])rerat\b', body_text.lower()):
        print(f"  ⚠️ 'rerat' found (should be 'rerate')")
        for m in re.finditer(r'(?<![a-z])rerat\b', body_text, re.I):
            ctx = body_text[max(0,m.start()-30):m.end()+30]
            print(f"    ...{ctx}...")

    # Check for garbled text patterns
    garbled_patterns = [
        r'\bgets-real\b',
        r'\bthe\s+[a-z]{2,5}\s+is\s+[a-z]{2,5}s\b',
    ]

# ===== LINK CHECK =====
print("\n" + "=" * 80)
print("LINK CHECK (will be done via curl)")
print("=" * 80)
for a in articles:
    links = a.get('links', [])
    print(f"\n{a['slug']}: {len(links)} links")
    for link in links:
        print(f"  {link.get('label','?'):50s} -> {link.get('url','?')}")

# ===== EXTRACT FULL BODIES =====
print("\n" + "=" * 80)
print("FULL BODIES FOR SPELL CHECK")
print("=" * 80)
for a in articles:
    body = a.get('bodyHtml', '')
    body_text = re.sub(r'<[^>]+>', ' ', body)
    body_text = html_mod.unescape(body_text)
    body_text = re.sub(r'\s+', ' ', body_text).strip()
    
    title = a.get('title', '')
    subtitle = a.get('subtitle', '')
    summary = a.get('summary', '')
    slug = a.get('slug', '')
    
    print(f"\n{'='*60}")
    print(f"ARTICLE: {slug}")
    print(f"{'='*60}")
    print(f"TITLE: {title}")
    print(f"SUBTITLE: {subtitle}")
    print(f"SUMMARY: {summary}")
    print(f"\nBODY TEXT:\n{body_text}")
