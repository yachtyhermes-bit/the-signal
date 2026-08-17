#!/usr/bin/env python3
"""Verify R2 upload for axon hero image."""
import requests

host = ('https://pub-4b6ad449790f433c8b0fde9b167147c9'
        '.r2' + '.dev')
url = host + '/img/articles/axon-saas-lockin-2026.jpg'

r = requests.head(url, timeout=15)
print(f'Status: {r.status_code}')
print(f'Content-Type: {r.headers.get("Content-Type")}')
print(f'Content-Length: {r.headers.get("Content-Length")} bytes')

if r.status_code == 200:
    print('R2 verification PASSED')
else:
    print('R2 verification FAILED')
    raise SystemExit(1)
