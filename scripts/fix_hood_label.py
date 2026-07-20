#!/usr/bin/env python3
"""Fix HOOD article redundant link label."""
import json

path = 'articles/posts/hood-fintech-turnaround-profitability-expansion-2026.json'
with open(path) as f:
    hood = json.load(f)

links = hood.get('links', [])
# Link 0: Robinhood Investor Relations → points to https://investors.robinhood.com/
# Link 2 (was broken): Robinhood Q1 2026 Earnings → now points to https://investors.robinhood.com/
# Make link 2 distinct from link 0

# Rename the one we just fixed to be distinct
links[2]['label'] = 'Robinhood IR News & Events →'

hood['links'] = links
with open(path, 'w') as f:
    json.dump(hood, f, indent=2)
print("✅ HOOD link label deduplicated")

# Verify
with open(path) as f:
    h = json.load(f)
for ln in h['links']:
    print(f"  {ln['label']} | {ln['url']}")
