#!/usr/bin/env python3
"""Verify R2 CDN accessibility of the Zscaler hero image."""
import requests

url = "https://pub-4b6ad449790f433c8b0fde9b167147c9.r2.dev/img/articles/zs-cloud-native-zero-trust-moat-2026.jpg"
r = requests.get(url, timeout=30)
print("HTTP", r.status_code)
print("Content-Type:", r.headers.get("Content-Type"))
print("Bytes:", len(r.content))
print("First bytes:", r.content[:3])
assert r.status_code == 200, "CDN verification FAILED"
assert r.content[:3] == b"\xff\xd8\xff", "Not a JPEG"
print("VERIFIED: public JPEG served from R2 CDN")
