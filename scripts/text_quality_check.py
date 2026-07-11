import json, re

slugs = [
    "ge-vernova-ai-power-infrastructure-2026",
    "asml-euv-monopoly-chokepoint-ai-chips",
    "ge-vernova-power-ai-data-centers-2026",
    "oracle-ai-cloud-capex-bet-2026",
    "credo-ai-connectivity-chips-2026"
]

for slug in slugs:
    a = json.load(open(f'articles/posts/{slug}.json'))
    body = a['bodyHtml']
    
    text = re.sub(r'<[^>]+>', '', body)
    text = text.replace('&amp;', '&').replace('&lt;', '<').replace('&gt;', '>')
    text = text.replace('\\n', ' ').replace('\\"', '"').replace('\\/', '/')
    text = re.sub(r'\s+', ' ', text).strip()
    
    print(f"\n{'='*60}")
    print(f"TEXT QUALITY: {slug}")
    
    issues = []
    
    # Double spaces
    if '  ' in text:
        issues.append(f"Double spaces found in text")
    
    # Garbled compound
    for pat in [r'\bthe\s+\w+s-\w+\b', r'\b\w+-\w+\s+\w+ens\b']:
        m = re.findall(pat, text, re.IGNORECASE)
        for phrase in m[:3]:
            idx = text.lower().find(phrase.lower())
            ctx = text[max(0,idx-10):idx+len(phrase)+30]
            issues.append(f"Garbled pattern: '{phrase}' in: ...{ctx}...")
    
    # Repeated words
    for word in ['a', 'an', 'the', 'in', 'on', 'of', 'to', 'is', 'it', 'that', 'and', 'or', 'but']:
        repeats = re.findall(r'\b' + word + r' \b' + word + r'\b', text, re.IGNORECASE)
        if repeats:
            issues.append(f"Repeated '{word}': {repeats}")
    
    # Check for " $S" pattern (dollar-sign ticker pitfall)
    ticker = a.get('ticker', '')
    dollar_ticker = re.findall(r'\$' + ticker + r'\b', text)
    if dollar_ticker:
        issues.append(f"Dollar-sign ticker: {dollar_ticker}")
    
    if not issues:
        print(f"  No issues found")
    else:
        for iss in issues:
            print(f"  {iss}")
