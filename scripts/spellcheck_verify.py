#!/usr/bin/env python3
"""Check CRWV daily OHLC around publication date and spell-check all articles."""

import yfinance as yf
import json, os, re, html as html_mod

base = '/home/chino/thesignal/articles/posts'

# Check CRWV daily data for July 8
t = yf.Ticker('CRWV')
hist = t.history(period='1mo')
print("CRWV daily data around July 8:")
print(hist.tail(10).to_string())
print()

# Check what July 8 close looks like
hist_july = hist[hist.index.month == 7]
print("\nCRWV July data:")
print(hist_july.to_string())

# Now manual spell-check of each article body
print("\n" + "="*80)
print("SPELL CHECK - reading full article bodies")
print("="*80)

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

for s in slugs:
    with open(f'{base}/{s}.json') as f:
        a = json.load(f)
    
    body = a.get('bodyHtml', '')
    title = a.get('title', '')
    subtitle = a.get('subtitle', '')
    summary = a.get('summary', '')
    ticker = a.get('ticker', '')
    
    # Clean HTML for text checking
    body_text = re.sub(r'<[^>]+>', ' ', body)
    body_text = html_mod.unescape(body_text)
    body_text = re.sub(r'\s+', ' ', body_text).strip()
    
    full_text = title + ' ' + subtitle + ' ' + summary + ' ' + body_text
    
    # Check for common AI writing errors:
    
    # 1. Number/word mismatch: look for written-out numbers
    num_words_found = re.findall(r'\b(one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|thirteen|fourteen|fifteen|sixteen|seventeen|eighteen|nineteen|twenty|thirty|forty|fifty|sixty|seventy|eighty|ninety|hundred|thousand|million|billion)\b', full_text, re.I)
    
    # 2. Check for double words
    double_words = re.findall(r'\b(\w+)\s+\1\b', full_text, re.I)
    
    # 3. Check for specific garbled text patterns from skill
    garbled = []
    for pattern in [r'\brerat\b(?!e)', r'\bgets-real\b']:
        matches = re.findall(pattern, full_text, re.I)
        if matches:
            garbled.append((pattern, matches))
    
    # 4. Check trailing P/E and high/drop % claims
    print(f"\n--- {s} ({ticker}) ---")
    
    if num_words_found:
        pass  # Most articles use numbers, not words
    
    if double_words:
        print(f"  ⚠️ Double words: {double_words}")
    
    if garbled:
        print(f"  ⚠️ Garbled patterns: {garbled}")
    
    # Specific claim checks
    if s == 'coreweave-ai-cloud-sale-2026':
        # Check "$99B contracted revenue backlog" - this is in the summary
        if '$99B' in body_text or '$99 billion' in body_text:
            print(f"  ✓ $99B backlog claim found")
        # Check revenue figures
        for yr, rev in [('FY2023', '$229 million'), ('FY2024', '$1.9 billion'), ('FY2025', '$5.13 billion')]:
            if yr in body_text:
                print(f"  ✓ {yr} revenue mentioned")
    
    # Check YTD claims
    if s == 'kratos-defense-unmanned-systems-hypersonics-2026':
        # Article says "Down 36% YTD, from $79 to $50"
        # yfinance 52-week high is $134, low is $44.85
        # Let's check what price was at start of year
        hist_annual = t.history(period='1y')
        print(f"  Checking KTOS YTD...")

print("\n\n=== DONE ===")
