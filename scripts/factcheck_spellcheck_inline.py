import json, re

articles_to_check = [
    'msft-frontier-ai-2026',
    'amat-chip-equipment-selloff-opportunity-2026',
    'northrop-grumman-defense-backlog-moat-2026',
    'axon-ai-policing-moat-2026',
    'salesforce-agentforce-ai-growth-2026'
]

for slug in articles_to_check:
    with open(f'articles/posts/{slug}.json') as f:
        d = json.load(f)
    
    body = d['bodyHtml']
    text = re.sub(r'<[^>]+>', ' ', body)
    text = re.sub(r'&[a-z]+;', ' ', text)
    text = re.sub(r'&#\d+;', ' ', text)
    
    print(f'=== {slug} ===')
    print(f'Title: {d["title"][:80]}')
    print(f'Subtitle: {d.get("subtitle","")[:80]}...')
    
    # Check disclosure
    if 'class="disclosure"' in body:
        print(f'  [OK] Disclosure present')
    else:
        print(f'  [WARN] Missing disclosure!')
    
    # Check ticker in disclosure
    ticker = d['ticker']
    if f'no position in ${ticker}' in body:
        print(f'  [WARN] Dollar-sign prefixed ticker in disclosure!')
    if f'no position in {ticker}' in body:
        print(f'  [OK] Ticker in disclosure')
    
    # Check dollar-sign prefixed tickers elsewhere
    dollar_tickers = re.findall(r'\$[A-Z]{2,5}', body)
    real_tickers = [t for t in dollar_tickers if t[1:] in ['MSFT','AMAT','NOC','AXON','CRM','AVGO','NVDA','PLTR','AAPL','GOOGL','META']]
    if real_tickers:
        print(f'  [OK] Dollar tickers found: {real_tickers[:3]}')
    
    # Check for long/garbled words
    words = re.findall(r'[a-zA-Z]{20,}', text)
    if words:
        print(f'  [WARN] Long words (>20 chars): {words[:5]}')
    
    # Check for common misspellings
    common_errors = ['recieved', 'occured', 'privelege', 'millenia', 'accomodate', 'embeded', 'rerat']
    for err in common_errors:
        if err in text.lower():
            print(f'  [WARN] Possible misspelling: {err}')
    
    # Check for garbled patterns
    if re.search(r'\brerat\b(?!e)', text.lower()):
        matches = re.findall(r'\brerat\b(?!e)', text.lower())
        print(f'  [WARN] "rerat" without trailing e: {matches}')
    
    # Check repeated words
    if re.search(r'\b(\w+)\s+\1\b', text):
        repeats = re.findall(r'\b(\w{3,})\s+\1\b', text)
        if repeats:
            print(f'  [WARN] Repeated words: {repeats[:3]}')
    
    print()
