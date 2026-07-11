import json, re, html

slugs = [
    "asml-euv-monopoly-chokepoint-ai-chips",
    "oracle-ai-cloud-capex-bet-2026",
    "credo-ai-connectivity-chips-2026",
    "smci-ai-server-accounting-comeback-2026",
    "vertiv-ai-data-center-infrastructure-q1-2026"
]

for slug in slugs:
    with open(f"articles/posts/{slug}.json") as f:
        a = json.load(f)
    
    body = a.get("bodyHtml", "")
    text = re.sub(r'<[^>]+>', ' ', body)
    text = html.unescape(text)
    text = re.sub(r'\s+', ' ', text).strip()
    
    print(f"\n=== {slug} ===")
    print(f"Title: {a['title'][:80]}")
    print(f"Text length: {len(text)} chars")
    
    # Check for garbled text patterns
    garbled_patterns = [
        (r'\bthe gets\b', 'the gets'),
        (r'\w{25,}', 'very long word'),
    ]
    for pat, desc in garbled_patterns:
        matches = re.findall(pat, text)
        if matches:
            print(f"  WARNING [{desc}]: {matches[:5]}")
    
    # Check for repeated words
    rep_pattern = r'\b(\w{3,})\s+\1\b'
    matches = re.findall(rep_pattern, text)
    if matches:
        print(f"  WARNING Repeated words: {matches[:5]}")
    
    # Check disclosure exists
    has_disclosure = 'class="disclosure"' in body or 'class=\"disclosure\"' in body
    if has_disclosure:
        ticker = a.get('ticker', '')
        disc_match = re.search(r'<p[^>]*class="disclosure"[^>]*>.*?</p>', body)
        if not disc_match:
            disc_match = re.search(r'<p[^>]*class=\\\\"disclosure\\\\"[^>]*>.*?</p>', body)
        if disc_match:
            disc = disc_match.group(0)
            if f'no position in {ticker}' in disc:
                print(f"  OK: Disclosure present for {ticker}")
            elif f'no position in ${ticker}' in disc:
                print(f"  WARNING: Dollar-sign prefixed ticker in disclosure!")
            else:
                print(f"  WARNING: Disclosure ticker mismatch. Checking: {disc[:150]}")
        else:
            print(f"  WARNING: Could not find disclosure HTML element")
    else:
        print(f"  WARNING: No disclosure found in body!")
    
    # Check body for rerate vs rerat
    if re.search(r'\brerat\b', text):
        if re.search(r'\brerat\b(?!e)', text):
            # Check if any "rerat" not followed by "e"
            for m in re.finditer(r'\brerat\b', text):
                end = m.end()
                if end >= len(text) or text[end] != 'e':
                    ctx = text[max(0,m.start()-10):min(len(text),m.end()+10)]
                    print(f"  WARNING: 'rerat' (not rerate) near: ...{ctx}...")
    
    # Print a sample of the body for visual inspection
    print(f"  First 100 chars: {text[:100]}...")
    print(f"  Last 100 chars: ...{text[-100:]}")
