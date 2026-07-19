#!/usr/bin/env python3
"""Fix the dead link in PANW article - replace thefly.com with GuruFocus."""
import json

with open('/home/chino/thesignal/articles/posts/panw-ai-security-cash-flow-machine-2026.json') as f:
    a = json.load(f)

# Find and replace the dead link
for i, link in enumerate(a['links']):
    if 'thefly.com' in link['url']:
        print(f"  Replacing: {link['url']}")
        link['url'] = 'https://www.gurufocus.com/news/8962602/palo-alto-networks-panw-receives-upgrade-and-price-target-increase-from-capital-one-securities'
        link['label'] = "GuruFocus — Capital One Upgrades PANW, PT $421"
        print(f"  With: {link['url']}")

with open('/home/chino/thesignal/articles/posts/panw-ai-security-cash-flow-machine-2026.json', 'w') as f:
    json.dump(a, f, indent=2)

print("  ✅ PANW article link fixed")
