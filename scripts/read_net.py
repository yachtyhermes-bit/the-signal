#!/usr/bin/env python3
"""Read full article bodies for NET and check problematic claims."""
import json, re

with open('/home/chino/thesignal/articles/posts/net-cloudflare-precursor-agentic-internet-2026.json') as f:
    a = json.load(f)

body = a['bodyHtml']
body_clean = re.sub(r'<[^>]+>', ' ', body)
print("=== NET FULL BODY (cleaned) ===")
print(body_clean)
