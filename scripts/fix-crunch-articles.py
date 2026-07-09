#!/usr/bin/env python3
"""Fix CRWV and SMCI article issues found during fact-check."""
import json

# === CRWV Fixes ===
with open('articles/posts/coreweave-ai-cloud-sale-2026.json') as f:
    crwv = json.load(f)

# Fix 1: Update video schema (was using embed/description instead of proper fields)
crwv['videos'] = [{
    "id": "53dOth6_1qM",
    "title": "CoreWeave: The Essential Cloud for AI",
    "source": "CoreWeave",
    "url": "https://www.youtube.com/watch?v=53dOth6_1qM",
    "position": "after_3rd_paragraph"
}]

# Fix 2: Add missing subtitle
crwv['subtitle'] = "CoreWeave is down 45% from its highs despite $99B in contracted revenue and 111% growth. Here's why the market might be missing the forest for the trees."

# Fix 3: Replace thefly.com dead link (404) with Yahoo Finance
crwv['links'] = [
    {"label": "CoreWeave Investor Relations", "url": "https://investors.coreweave.com/"},
    {"label": "Yahoo Finance CRWV", "url": "https://finance.yahoo.com/quote/CRWV/"}
]

with open('articles/posts/coreweave-ai-cloud-sale-2026.json', 'w') as f:
    json.dump(crwv, f, indent=2)
print("✓ CRWV article fixed (video schema, subtitle, dead link)")

# === SMCI Fix ===
with open('articles/posts/smci-ai-server-accounting-comeback-2026.json') as f:
    smci = json.load(f)

# Fix: Replace dead supermicro IR link (404) with SEC filings link
smci['links'] = [
    {"label": "Yahoo Finance SMCI", "url": "https://finance.yahoo.com/quote/SMCI"},
    {"label": "SMCI SEC Filings", "url": "https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=SMCI&owner=exclude&count=40"}
]

with open('articles/posts/smci-ai-server-accounting-comeback-2026.json', 'w') as f:
    json.dump(smci, f, indent=2)
print("✓ SMCI article fixed (dead IR link)")

# Verify both parse
for slug in ['coreweave-ai-cloud-sale-2026', 'smci-ai-server-accounting-comeback-2026']:
    with open(f'articles/posts/{slug}.json') as f:
        a = json.load(f)
    print(f"✓ {slug}: {len(a.get('links', []))} links, {'subtitle' in a} subtitle, {len(a.get('videos', []))} videos")
