#!/usr/bin/env python3
"""Check if NET audio exists on R2."""
import urllib.request

url = 'https://pub-4b6ad449790f433c8b0fde9b167147c9.r2.dev/v2/net-cloudflare-precursor-agentic-internet-2026.mp3'
req = urllib.request.Request(url, method='HEAD')
try:
    resp = urllib.request.urlopen(req, timeout=10)
    print(f'R2 status: {resp.status}')
    print(f'Content-Type: {resp.headers.get("Content-Type")}')
    print(f'Content-Length: {resp.headers.get("Content-Length")}')
except Exception as e:
    print(f'Error: {e}')
