import json, re, os

slugs = [
    "lockheed-martin-defense-moat-2026",
    "micron-us-chip-investment-surge-2026",
    "tsmc-ai-chip-monopoly-2026",
    "marvell-ai-switch-asic-rebound-2026",
    "palo-alto-networks-platformization-2026",
    "top-energy-plays-ai-power-2026",
    "oracle-ai-cloud-capex-bet-2026",
    "asml-euv-monopoly-chokepoint-ai-chips",
    "ge-vernova-power-ai-data-centers-2026",
    "credo-ai-connectivity-chips-2026"
]

for slug in slugs:
    fp = f'/home/chino/thesignal/articles/posts/{slug}.json'
    a = json.load(open(fp))
    body = a.get('bodyHtml', '')
    text = re.sub(r'<[^>]+>', '', body)
    text = text.replace('&amp;', '&').replace('&lt;', '<').replace('&gt;', '>')
    text = text.replace('\\n', ' ').replace('\\"', '"').replace('\\/', '/')
    
    issues = []
    
    # 1. Check for garbled text patterns
    # Repeated words with space (e.g. "the the")
    if re.search(r'\b(\w+)\s+\1\b', text, re.IGNORECASE):
        issues.append("Repeated words found")
    
    # 2. Check for dollar-sign prefixed tickers
    ticker = a.get('ticker', '')
    if ticker and re.search(r'\$' + ticker, body):
        issues.append(f"Dollar-sign prefixed ticker ${ticker}")
    
    # 3. Check for missing punctuation at sentence boundaries
    # Look for periods without space
    if re.search(r'\.(?!\s|$)', text):
        issues.append("Period without trailing space")
    
    # 4. Check for garbled AI text patterns (the gets-real happens type)
    garbled_patterns = [
        r'\bthe\s+gets\b',
        r'\bgets-real\b',
        r'\bit\s+the\s+that\b',
    ]
    for pat in garbled_patterns:
        if re.search(pat, text, re.IGNORECASE):
            issues.append(f"Garbled syntax match: {pat}")
    
    # 5. Check for disclosure presence and format
    discl_found = 'class="disclosure"' in body or 'class=\\"disclosure\\"' in body
    
    # 6. Check the disclosure ends the article
    if discl_found:
        last_1000 = body[-1000:]
        if 'disclosure' not in last_1000.lower():
            issues.append("Disclosure not at end of article")
    
    # 7. Check title + subtitle for garbled text
    title = a.get('title', '')
    subtitle = a.get('subtitle', '')
    if re.search(r'\b(?:[A-Z]{,2})\s+(?:[A-Z]{,2})\s+(?:[A-Z]{,2})\b', title):
        issues.append("Title may have garbled spacing")
    
    if issues:
        print(f"\n{slug}: {len(issues)} issue(s)")
        for iss in issues:
            print(f"  - {iss}")
    else:
        print(f"\n{slug}: All text quality checks passed")

# Also check for the specific pattern mentioned in the skill
# "the gets-real happens" type garbled text
print("\n\n=== GARBLED TEXT SCAN (specific patterns) ===")
for slug in slugs:
    fp = f'/home/chino/thesignal/articles/posts/{slug}.json'
    a = json.load(open(fp))
    body = a.get('bodyHtml', '')
    text = re.sub(r'<[^>]+>', '', body)
    text = text.replace('\\n', ' ').replace('\\"', '"')
    
    # Check for repeated short words
    for m in re.finditer(r'\b(\w{2,4})\s+\1\b', text, re.IGNORECASE):
        w = m.group(1)
        if w.lower() not in ['that', 'has', 'had', 'and', 'for', 'the', 'not', 'are', 'was', 'but', 'its', 'all', 'can', 'been', 'were', 'than']:
            print(f"  {slug}: repeated '{w}'")
    
    # Check for garbled adjective+noun patterns  
    for m in re.finditer(r'\b(the|a|an)\s+\w{2,5}\s+-\s+\w{2,5}\s+\w{2,5}\b', text[:5000]):
        print(f"  {slug}: possible hyphen-garbled: '{m.group()[:60]}'")
PYEOF