#!/usr/bin/env python3
"""Check HOOD broken link and SHOP yPal context."""
import json, re

# Check SHOP yPal context
with open('articles/posts/shopify-ai-commerce-moat-ecosystem-2026.json') as f:
    shop = json.load(f)
body = shop['bodyHtml']
for m in re.finditer(r'yPal', body):
    ctx = body[max(0, m.start()-30):m.end()+30]
    print(f"SHOP 'yPal' context: ...{ctx}...")
if 'yPal' not in body:
    print("SHOP: No 'yPal' found in body (false positive from spell-check)")

# Try HOOD link
import urllib.request
urls = [
    "https://investors.robinhood.com/news-events/press-releases/detail/48/robinhood-reports-first-quarter-2026-results",
    "https://investors.robinhood.com/news-events/press-releases/",
]
for url in urls:
    try:
        req = urllib.request.Request(url, method='HEAD')
        with urllib.request.urlopen(req, timeout=10) as resp:
            print(f"HOOD {resp.status} | {url}")
    except Exception as e:
        print(f"HOOD error | {url}: {e}")
