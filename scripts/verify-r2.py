#!/usr/bin/env python3
"""Verify R2 upload by checking the URL."""
import requests

url = ('https://pub-4b6ad449790f433c8b0fde9b167147c9'
       '.r2.dev/img/articles/salesforce-agentforce-ai-growth-2026.jpg')

r = requests.head(url, timeout=10)
print(f'Status: {r.status_code}')
print(f'Content-Type: {r.headers.get("Content-Type")}')
print(f'Content-Length: {r.headers.get("Content-Length")} bytes')

if r.status_code == 200:
    print('R2 verification PASSED')
else:
    print('R2 verification FAILED')
    exit(1)
