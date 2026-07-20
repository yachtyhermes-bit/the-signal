#!/usr/bin/env python3
"""Fix HOOD article broken link."""
import json

path = 'articles/posts/hood-fintech-turnaround-profitability-expansion-2026.json'
with open(path) as f:
    hood = json.load(f)

links = hood.get('links', [])
for i, link in enumerate(links):
    if 'detail/48/' in link.get('url', ''):
        print(f"Found broken link: {link['url']}")
        # Replace with the main investor relations page which works
        links[i]['url'] = 'https://investors.robinhood.com/'
        links[i]['label'] = 'Robinhood Investor Relations →'
        print(f"Replaced with: {links[i]['url']}")

hood['links'] = links
with open(path, 'w') as f:
    json.dump(hood, f, indent=2)
print("✅ HOOD link fixed")
