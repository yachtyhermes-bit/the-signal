#!/usr/bin/env python3
"""Fix remaining TSM article issues."""
import json, re

path = 'articles/posts/tsm-ai-chip-monopoly-2026.json'
with open(path) as f:
    tsm = json.load(f)

body = tsm['bodyHtml']

# 1. Fix "TSM at $398 with 60% operating margins" — stock price in body
if 'TSM at $398 with 60% operating margins' in body:
    body = body.replace('TSM at $398 with 60% operating margins', 'TSM with 60% operating margins')
    print("✅ Fixed: 'TSM at $398 with 60%' → 'TSM with 60%'")

# 2. Fix "spending over $120 billion" variant
for variant in ['spending over $120 billion a year on capital expenditures',
                 'is spending over $120 billion a year on capital expenditures',
                 'spending over $120 billion']:
    if variant in body:
        body = body.replace(variant, variant.replace('$120 billion', '$35 billion'))
        print(f"✅ Fixed capex variant: '{variant[:50]}...'")

# 3. Double check no remaining '$120 billion' in capex context
import re
if re.search(r'\$120\s*billion', body):
    for m in re.finditer(r'\$120\s*billion', body):
        ctx = body[max(0, m.start()-20):m.end()+30]
        print(f"⚠️ Still has '$120 billion' at {m.start()}: ...{ctx}...")
else:
    print("✅ No remaining '$120 billion' references")

# 4. Check for remaining '$398' references
if re.search(r'\$398(?!\.)', body):
    for m in re.finditer(r'\$398(?!\.)', body):
        ctx = body[max(0, m.start()-15):m.end()+25]
        print(f"⚠️ Still has '$398' at {m.start()}: ...{ctx}...")
else:
    print("✅ No remaining '$398' references")

tsm['bodyHtml'] = body
with open(path, 'w') as f:
    json.dump(tsm, f, indent=2)
print("✅ TSM article saved")
