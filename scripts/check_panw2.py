#!/usr/bin/env python3
"""Find all numeric claims in PANW article about FCF margin."""
import json, re

with open('/home/chino/thesignal/articles/posts/panw-ai-security-cash-flow-machine-2026.json') as f:
    a = json.load(f)

body = a['bodyHtml']
clean = re.sub(r'<[^>]+>', ' ', body)

# Search for the actual FCF margin number
for match in re.finditer(r'.{0,40}FCF.{0,40}', clean):
    print(f"  FCF mention: {match.group().strip()}")

print("\n--- All numeric claims in PANW article ---")
for match in re.finditer(r'.{0,30}\d{1,3}[\.\d]*%.{0,30}', clean):
    print(f"  {match.group().strip()}")

# Check if 30.5 exists
if '30.5' in body:
    print("\n✅ '30.5' found in body")
else:
    print("\n❌ '30.5' NOT found in body")
    
# Check what margin numbers exist
for match in re.finditer(r'\d+\.?\d*%', clean):
    ctx_start = max(0, match.start() - 30)
    ctx = clean[ctx_start:match.end() + 30]
    print(f"  % claim: {ctx.strip()}")
