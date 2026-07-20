#!/usr/bin/env python3
"""Fact-check the 5 most recently published articles + spell-check."""
import json, os, subprocess, sys
from datetime import datetime

ARTICLES_DIR = '/home/chino/thesignal/articles/posts'

# Load all articles and sort by date (newest first)
articles = []
for fname in os.listdir(ARTICLES_DIR):
    if not fname.endswith('.json'):
        continue
    path = os.path.join(ARTICLES_DIR, fname)
    with open(path) as f:
        try:
            art = json.load(f)
            date_str = art.get('date', '')
            articles.append((date_str, art, path))
        except:
            print(f"⚠️ Could not parse {fname}")

articles.sort(key=lambda x: x[0], reverse=True)
top5 = articles[:5]

print(f"📋 Top 5 articles (by date):")
for date_str, art, path in top5:
    print(f"  [{date_str}] {art.get('slug','?')} — {art.get('title','?')[:60]}")
print()

# Check 1: Spell check
print("=" * 60)
print("CHECK 1: Spell Check")
print("=" * 60)
spell_result = subprocess.run(
    ['python3', '/home/chino/thesignal/scripts/factcheck_spellcheck.py'],
    capture_output=True, text=True, timeout=120
)
print(spell_result.stdout[-2000:] if len(spell_result.stdout) > 2000 else spell_result.stdout)
if spell_result.stderr:
    print(f"STDERR: {spell_result.stderr[-500:]}")
print()

# Check 2: Per-article fact check
print("=" * 60)
print("CHECK 2: Per-Article Fact Check")
print("=" * 60)

for date_str, art, path in top5:
    slug = art.get('slug', '?')
    ticker = art.get('ticker', '?')
    title = art.get('title', '?')
    subtitle = art.get('subtitle', '')
    summary = art.get('summary', '')
    body = art.get('bodyHtml', '')
    price = art.get('price')
    links = art.get('links', [])
    
    print(f"\n{'─'*50}")
    print(f"📰 {title}")
    print(f"  Slug: {slug} | Ticker: {ticker} | Date: {date_str} | Price: ${price}")
    
    # Check for dollar-sign prefixed tickers
    import re
    dollar_ticker_matches = re.findall(r'\$' + re.escape(ticker), body)
    if dollar_ticker_matches:
        print(f"  ⚠️ Dollar-sign prefixed ticker found ({len(dollar_ticker_matches)}x): ${ticker}")
    
    # Check for price in body
    price_pattern = re.findall(r'\$\d+\.\d{2}', body)
    if price_pattern:
        print(f"  🔴 PRICE IN BODY: {price_pattern[:5]}")
    
    # Check garbled text patterns
    garbled_patterns = [
        (r'\bthe\s+gets\b', 'garbled: "the gets"'),
        (r'\bit\s+gets\s+real\b', 'OK: "it gets real"'),
        (r'[a-z][A-Z][a-z]{2,}', 'possible missing space'),
    ]
    for pat, desc in garbled_patterns:
        matches = re.findall(pat, body)
        if matches and desc != 'OK: "it gets real"':
            print(f"  ⚠️ {desc}: {matches[:3]}")
    
    # Check disclosure
    if 'class="disclosure"' not in body:
        print(f"  🔴 MISSING DISCLOSURE")
    elif ticker not in body.split('class="disclosure"')[-1][:200]:
        print(f"  ⚠️ Ticker {ticker} may not be in disclosure")

    # Check links
    for i, link in enumerate(links):
        url = link.get('url', '')
        label = link.get('label', link.get('text', ''))
        print(f"  🔗 [{label}]({url})")

print(f"\n{'='*60}")
print("DONE — review results above")
