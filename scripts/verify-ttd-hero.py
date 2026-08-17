#!/usr/bin/env python3
"""Verify TTD R2 hero image is publicly reachable (HTTP 200)."""
import requests

url = "https://pub-4b6ad449790f433c8b0fde9b167147c9.r2.dev/img/articles/ttd-adtech-earnings-preview-2026.jpg"
r = requests.get(url, timeout=30)
print(f"HTTP {r.status_code} | {len(r.content)} bytes | {r.headers.get('content-type')} | ETag {r.headers.get('etag')}")
assert r.status_code == 200, f"Expected 200, got {r.status_code}"
assert len(r.content) > 10000, "Response suspiciously small"
print("VERIFY OK")
