import json, re, subprocess

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
    
    print(f"\n{'='*70}")
    print(f"SPELL CHECK: {slug}")
    print(f"Title: {a['title'][:80]}")
    
    # Run aspell
    r = subprocess.run(
        ['aspell', 'list'],
        input=text,
        capture_output=True,
        text=True,
        timeout=10
    )
    misspelled = [w for w in r.stdout.strip().split('\n') if w.strip() and len(w.strip()) > 1]
    
    known = {'nvidia', 'asml', 'gevernova', 'crdo', 'orcl', 'oracle',
             'hyperscaler', 'hyperscalers', 'backlog',
             'strazik', 'brennan', 'ellison',
             'zettascale', 'stargate', 'stifel', 'evercore', 'isi',
             'multicloud',
             'aeroderivative',
             'darlington', 'osge', 'bwrx',
             'capex', 'rpo', 'iaas', 'peg',
             'dustphotonics',
             'retimers', 'dsps', 'serdes', 'pics',
            }
    
    real_errors = [w for w in misspelled if w.lower() not in known and not w.startswith(("'", '-')) and not w.isupper() and not w.isdigit()]
    
    if real_errors:
        print(f"  Potential spelling issues:")
        for w in sorted(set(real_errors))[:30]:
            # Show context
            idx = text.lower().find(w.lower())
            ctx = text[max(0,idx-20):idx+len(w)+20]
            print(f"    - '{w}' in context: ...{ctx}...")
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
    
    # Check dollar-sign prefixed ticker
    if re.search(r'\$' + ticker, body):
        print(f"  Dollar-sign prefixed ticker found: ${ticker}")
    
    # Check for specific known issues
    if re.search(r'\brerat\b(?!e)', text):
        print(f"  'rerat' found (possible typo for 'rerate')")
    
    print(f"  Body length: {len(body)} chars")
