import json, re

slugs = [
    "snow-ai-data-cloud-consumption-2026",
    "amat-picks-shovels-ai-supercycle-2026", 
    "crm-agentforce-doubt-discount-2026",
    "rbrk-cyber-resilience-secular-growth-2026",
    "avav-counterdrone-switchblade-contracts-2026",
]

def check_price_context(body, article_price, ticker, label):
    """Check if the actual stock price appears in body text."""
    # Only flag prices that match or are close to the article price
    if article_price is None:
        return []
    
    # Try matching $XXX.XX or $XXX patterns that could be stock prices
    # Stock prices are usually $100+, smaller numbers are EPS/metrics
    flags = []
    
    # The article's stated price
    price_str = f"${article_price:.2f}"
    price_rounded = f"${round(article_price)}"
    price_compact = f"${article_price}"  # e.g. $267.8
    
    for field_name, text in [('subtitle', label)]:
        if price_str in text or price_rounded in text:
            flags.append(f"Article stock price ${article_price} in {field_name}")
        # Also check for the compact form
        if price_compact in text and article_price >= 100:
            # Check it's the actual price, not a substring of a different number
            idx = text.find(price_compact)
            if idx >= 0:
                before = text[idx-1] if idx > 0 else ' '
                after = text[idx+len(price_compact)] if idx+len(price_compact) < len(text) else ' '
                if not after.isdigit() and before != '.':
                    flags.append(f"Article stock price ${article_price} in {field_name}")
    
    return flags

for slug in slugs:
    print(f"\n=== {slug} ===")
    with open(f'articles/posts/{slug}.json') as f:
        a = json.load(f)
    
    body = a.get('bodyHtml', '')
    subtitle = a.get('subtitle', '')
    summary = a.get('summary', '')
    price = a.get('price')
    ticker = a.get('ticker', '')
    
    # Strip HTML
    clean_body = re.sub(r'<[^>]+>', ' ', body)
    clean_body = re.sub(r'&[a-z]+;', ' ', clean_body)
    
    # Find ALL $XX.XX and $X,XXX patterns
    all_dollar_amounts = re.findall(r'\$\d{1,3}(?:,\d{3})*(?:\.\d{2})?', clean_body)
    
    # Group by context
    for amt in set(all_dollar_amounts):
        # Skip if it's clearly not the stock price
        numeric = float(amt.replace('$', '').replace(',', ''))
        if price and abs(numeric - price) < 1.0 and numeric >= 10:
            print(f"  ⚠️ STOCK PRICE MATCH in body: {amt} (article price: ${price})")
        elif numeric < 5:
            print(f"  (small value, likely EPS/metric): {amt}")
        elif numeric >= 5 and numeric < 10:
            print(f"  (medium value): {amt}")
        elif numeric >= 10 and numeric < 50:
            print(f"  (medium value): {amt}")
    
    # Check subtitle and summary for the actual stock price
    for field_name, text in [('subtitle', subtitle), ('summary', summary)]:
        if price:
            # Check various formats
            for fmt in [f"${price:.2f}", f"${price}", f"${int(price)}"]:
                if fmt in text:
                    # Verify it's not part of a longer number
                    idx = text.find(fmt)
                    after = text[idx+len(fmt):idx+len(fmt)+1] if idx+len(fmt) < len(text) else ' '
                    if not after.isdigit():
                        print(f"  ⚠️ STOCK PRICE ${price} in {field_name}: '{fmt}'")
    
    print(f"  Summary: {summary[:120]}...")
