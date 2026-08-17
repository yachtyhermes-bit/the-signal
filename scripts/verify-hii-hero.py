#!/usr/bin/env python3
"""Verify HII hero image is live on R2 CDN."""
import requests

URL = 'https://pub-4b6ad449790f433c8b0fde9b167147c9.r2.dev/img/articles/hii-q2-2026-earnings-nuclear-navy-backlog.jpg'

r = requests.head(URL, timeout=30)
print('HTTP', r.status_code)
print('Content-Type:', r.headers.get('Content-Type'))
print('Content-Length:', r.headers.get('Content-Length'))
print('ETag:', r.headers.get('ETag'))
print('CF-Cache-Status:', r.headers.get('CF-Cache-Status'))
print('Last-Modified:', r.headers.get('Last-Modified'))

# Also fetch a few bytes to confirm body serves
r2 = requests.get(URL, timeout=30, stream=True)
body = next(r2.iter_content(16))
print('Body bytes (first 16):', body[:8].hex(), '...')
print('GET status:', r2.status_code)
