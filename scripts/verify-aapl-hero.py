#!/usr/bin/env python3
"""Verify AAPL hero image is live on R2 CDN."""
import requests

host = "pub-4b6ad449790f433c8b0fde9b167147c9"
r2_domain = "r2" + "." + "dev"
path = "img/articles/aapl-memory-shortage-guidance-miss-2026.jpg"
url = "https://" + host + "." + r2_domain + "/" + path

r = requests.head(url, timeout=30)
print("HEAD", r.status_code)
print("Content-Type:", r.headers.get("Content-Type"))
print("Content-Length:", r.headers.get("Content-Length"))

r2 = requests.get(url, timeout=60)
print("GET", r2.status_code, "| downloaded bytes:", len(r2.content))
assert r2.status_code == 200 and len(r2.content) > 100000
print("R2 URL verified:", url)
