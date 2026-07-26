#!/usr/bin/env python3
import json, re

with open('/tmp/signal_homepage.html') as f:
    html = f.read()

match = re.search(r'<script id="articles-data" type="application/json">(.*?)</script>', html, re.DOTALL)
if match:
    data = json.loads(match.group(1))
    for a in data:
        print(f'{a["slug"]}: {a["title"]}')
