import json, re, subprocess, os

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

known_words = {
    'nvidia', 'asml', 'gevernova', 'crdo', 'orcl', 'oracle',
    'hyperscaler', 'hyperscalers', 'backlog',
    'strazik', 'brennan', 'ellison',
    'zettascale', 'stargate', 'stifel', 'evercore', 'isi',
    'multicloud', 'aeroderivative',
    'darlington', 'osge', 'bwrx',
    'capex', 'rpo', 'iaas', 'peg',
    'dustphotonics', 'retimers', 'dsps', 'serdes', 'pics',
    'thaad', 'platformization', 'cortx',
    'aramco', 'calpine', 'trainium', 'axion', 'tpu',
    'cmos', 'chokepoint', 'reshoring',
    'nongaap', 'euv', 'toolmaker', 'xsi', 'sase',
    'stellantis', 'pensana', 'quimby',
    'paloaltonetworks', 'nimesh', 'soc', 'ngs', 'arr',
    'mse', 'interceptors', 'idira',
    'amd', 'msft',
    'interceptors',
}

for slug in slugs:
    fp = f'/home/chino/thesignal/articles/posts/{slug}.json'
    if not os.path.exists(fp):
        print(f"\n=== {slug} === FILE NOT FOUND!")
        continue
    
    a = json.load(open(fp))
    body = a.get('bodyHtml', '')
    text = re.sub(r'<[^>]+>', '', body)
    text = text.replace('&amp;', '&').replace('&lt;', '<').replace('&gt;', '>')
    text = text.replace('\\n', ' ').replace('\\"', '"').replace('\\/', '/')
    text = re.sub(r'\s+', ' ', text).strip()
    
    print(f"\n{'='*70}")
    print(f"SPELL CHECK: {slug}")
    print(f"Title: {a.get('title','N/A')[:80]}")
    
    # Run aspell
    try:
        r = subprocess.run(
            ['aspell', 'list'],
            input=text,
            capture_output=True,
            text=True,
            timeout=10
        )
        misspelled = [w for w in r.stdout.strip().split('\n') if w.strip() and len(w.strip()) > 1]
    except:
        misspelled = []
        print("  [aspell not available]")
    
    real_errors = [w for w in misspelled if w.lower() not in known_words and not w.startswith(("'", '-')) and not w.isupper() and not w.isdigit() and len(w) > 2]
    
    if real_errors:
        print(f"  Potential spelling issues ({len(real_errors)} total, showing up to 15):")
        for w in sorted(set(real_errors))[:15]:
            idx = text.lower().find(w.lower())
            ctx = text[max(0,idx-25):idx+len(w)+25]
            print(f"    - '{w}': ...{ctx.strip()}...")
    else:
        print(f"  No spelling issues found")
    
    # Check disclosure
    body_lower = body.lower()
    ticker = a.get('ticker', '')
    has_disclosure = 'disclosure: the signal holds no position' in body_lower
    if has_disclosure:
        print(f"  Has disclosure for {ticker}")
    else:
        print(f"  MISSING DISCLOSURE!")
    
    # Check for $TICKER pattern
    if re.search(r'\$' + ticker, body):
        print(f"  Dollar-sign prefixed ticker found: ${ticker}")
    
    # Check for 'rerat' typo
    if re.search(r'\brerat\b(?!e)', text, re.IGNORECASE):
        print(f"  rerat found (possible typo for rerate)")
    
    print(f"  Body length: {len(body)} chars")
