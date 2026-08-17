#!/usr/bin/env python3
"""Verify CAT hero image is live on R2 CDN."""
import requests

url = 'https://pub-4b6ad449790f433c8b0fde9b167147c9.r2.dev/img/articles/cat-ai-power-record-backlog-2026.jpg'
r = requests.head(url, timeout=30)
print('HTTP status:', r.status_code)
print('Content-Type:', r.headers.get('Content-Type'))
print('Content-Length:', r.headers.get('Content-Length'))
assert r.status_code == 200, f'Expected 200, got {r.status_code}'
print('VERIFY OK')
