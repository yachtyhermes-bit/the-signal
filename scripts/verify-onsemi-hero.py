#!/usr/bin/env python3
"""Verify onsemi hero image is live on the R2 CDN."""
import requests

R2_URL = "https://pub-4b6ad449790f433c8b0fde9b167147c9.r2.dev/img/articles/onsemi-ai-power-surge-2026.jpg"

resp = requests.head(R2_URL, timeout=30)
print(f"HTTP {resp.status_code}")
print(f"Content-Type: {resp.headers.get('Content-Type')}")
print(f"Content-Length: {resp.headers.get('Content-Length')}")
if resp.status_code == 200:
    print(f"OK - image accessible at: {R2_URL}")
else:
    print(f"Got HTTP {resp.status_code}, might not be publicly accessible")
    raise SystemExit(1)
