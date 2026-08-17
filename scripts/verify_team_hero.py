#!/usr/bin/env python3
"""Verify the R2 hero image upload for the TEAM article via HEAD request."""

import requests

cdn = "https://pub-4b6ad449790f433c8b0fde9b167147c9.r2" + ".dev"
url = cdn + "/img/articles/team-atlassian-ai-enterprise-collaboration-2026.jpg"

r = requests.head(url, timeout=30, allow_redirects=True)
print("HTTP", r.status_code)
for h in ["content-type", "content-length", "etag", "last-modified"]:
    print(f"{h}: {r.headers.get(h)}")
print("OK" if r.status_code == 200 else "FAILED")
