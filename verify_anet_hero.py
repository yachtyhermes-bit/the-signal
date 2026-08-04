#!/usr/bin/env python3
"""Verify the ANET hero image is live on R2."""
import requests

url = "https://pub-4b6ad449790f433c8b0fde9b167147c9.r2.dev/img/articles/anet-ai-networking-backbone-2026.jpg"
r = requests.get(url, timeout=30)
print("HTTP", r.status_code)
print("Content-Type:", r.headers.get("Content-Type"))
print("Bytes downloaded:", len(r.content))
print("First bytes (JPEG magic):", r.content[:3] == b"\xff\xd8\xff")
