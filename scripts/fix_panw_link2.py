#!/usr/bin/env python3
"""Use Benzinga instead of GuruFocus for the PANW link."""
import json

with open('/home/chino/thesignal/articles/posts/panw-ai-security-cash-flow-machine-2026.json') as f:
    a = json.load(f)

for i, link in enumerate(a['links']):
    if 'thefly.com' in link['url']:
        link['url'] = 'https://www.benzinga.com/quote/PANW/analyst-ratings'
        link['label'] = "Benzinga — PANW Analyst Ratings"
        print(f"  ✅ Replaced with Benzinga: {link['url']}")

with open('/home/chino/thesignal/articles/posts/panw-ai-security-cash-flow-machine-2026.json', 'w') as f:
    json.dump(a, f, indent=2)

# Verify JSON is valid
import json
with open('/home/chino/thesignal/articles/posts/panw-ai-security-cash-flow-machine-2026.json') as f:
    json.load(f)
print("  ✅ JSON valid")
