#!/usr/bin/env python3
"""Search PANW article for margin and FCF margin claims."""
import json, re

with open('/home/chino/thesignal/articles/posts/panw-ai-security-cash-flow-machine-2026.json') as f:
    a = json.load(f)

body = a['bodyHtml']

# Find all sentences with "margin" or "FCF margin" 
for s in body.split('.'):
    if 'margin' in s.lower() or 'fcf' in s.lower():
        # Strip tags
        clean = re.sub(r'<[^>]+>', ' ', s).strip()
        if clean:
            print(f"  {clean}\n")
