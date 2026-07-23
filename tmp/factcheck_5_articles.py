import json, subprocess, re, tempfile, math

slugs = [
    "snow-ai-data-cloud-consumption-2026",
    "amat-picks-shovels-ai-supercycle-2026", 
    "crm-agentforce-doubt-discount-2026",
    "rbrk-cyber-resilience-secular-growth-2026",
    "avav-counterdrone-switchblade-contracts-2026",
]

def spellcheck_text(text, label):
    """Run aspell on text and return misspellings."""
    if not text:
        return []
    # Write to temp file for aspell
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
        f.write(text)
        tmppath = f.name
    
    try:
        result = subprocess.run(
            ['aspell', 'list', '--lang=en_US', '--extra-dicts=./tmp/signal-words', '--mode=html'],
            input=text,
            capture_output=True,
            text=True,
            timeout=15
        )
        # Filter out common false positives
        misspellings = set(result.stdout.strip().split('\n')) if result.stdout.strip() else set()
        # Filter out numbers, single chars, and known financial terms
        known_good = {'co', 'llc', 'inc', 'ltd', 'corp', 'etf', 'ipo', 'ceo', 'cfo', 'cto',
                      'yoy', 'qoq', 'ttm', 'saaS', 'ai', 'pe', 'ev', 'ebitda', 'fcf',
                      'vix', 'nyse', 'nasdaq', 'sec', 'secs', 'MAUs', 'wow',
                      'swag', 'b2b', 'b2c', 'cagr', 'fy', 'fcf', 'FQ', 'v4'}
        filtered = sorted(w for w in misspellings if len(w) > 1 and w.lower() not in known_good)
        return filtered
    finally:
        subprocess.run(['rm', '-f', tmppath])

for slug in slugs:
    print(f"\n{'='*60}")
    print(f"ARTICLE: {slug}")
    print('='*60)
    
    with open(f'articles/posts/{slug}.json') as f:
        a = json.load(f)
    
    # --- Spelling check ---
    body = a.get('bodyHtml', '')
    title = a.get('title', '')
    subtitle = a.get('subtitle', '')
    summary = a.get('summary', '')
    
    combined_text = title + "\n" + subtitle + "\n" + summary + "\n" + body
    # Strip HTML tags
    clean_text = re.sub(r'<[^>]+>', ' ', combined_text)
    clean_text = re.sub(r'&[a-z]+;', ' ', clean_text)
    
    errors = spellcheck_text(clean_text, 'body')
    if errors:
        print(f"  SPELLING ISSUES: {len(errors)} potential errors")
        for e in errors[:30]:
            print(f"    - '{e}'")
    else:
        print(f"  ✅ Spelling: OK")
    
    # --- Dollar-sign prefixed ticker check ---
    ticker = a.get('ticker', '')
    if ticker:
        dollar_ticker = '$' + ticker
        if dollar_ticker in body:
            print(f"  ⚠️ Dollar-sign prefixed ticker found: '{dollar_ticker}' in body")
        else:
            print(f"  ✅ No dollar-sign prefixed ticker: OK")
    
    # --- Price in body check ---
    article_price = a.get('price')
    body_lower = body.lower()
    price_in_body = False
    
    # Check for prices in body, subtitle, summary
    for field_name, field_value in [('bodyHtml', body), ('subtitle', subtitle), ('summary', summary)]:
        # Look for $X.XX patterns
        price_patterns = re.findall(r'\$\d{1,3}(?:,\d{3})*(?:\.\d{2})?', field_value)
        for p in price_patterns:
            price_in_body = True
            print(f"  ⚠️ Price in {field_name}: {p}")
    
    if not price_in_body:
        print(f"  ✅ No stale prices in body/subtitle/summary: OK")
    
    # --- Disclosure check ---
    if 'Disclosure:' in body:
        if 'class="disclosure"' in body:
            print(f"  ✅ Disclosure present with CSS class: OK")
        else:
            print(f"  ⚠️ Disclosure MISSING CSS class!")
    else:
        print(f"  ⚠️ Disclosure MISSING!")
    
    # --- Price field check ---
    if 'price' in a and a['price'] is not None:
        print(f"  ✅ Price field present: ${a['price']}")
    else:
        print(f"  ⚠️ Price field MISSING!")

print("\n" + "="*60)
print("SPELL/PRICE CHECK COMPLETE")
