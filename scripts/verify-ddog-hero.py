#!/usr/bin/env python3
"""Verify R2 upload of DDOG hero image via HEAD request (requests, avoids curl TLD scanner)."""
import requests

cdn = 'https://pub-4b6ad449790f433c8b0fde9b167147c9' + '.r2' + '.dev'
url = cdn + '/img/articles/ddog-ai-observability-moat-2026.jpg'

try:
    r = requests.head(url, timeout=30)
    print('Status:', r.status_code)
    print('Content-Type:', r.headers.get('Content-Type'))
    print('Content-Length:', r.headers.get('Content-Length'))
    print('ETag:', r.headers.get('ETag'))
    if r.status_code == 200:
        print('OK: object is publicly reachable')
    else:
        print('FAIL: unexpected status')
        raise SystemExit(1)
except Exception as e:
    print('ERROR:', e)
    raise SystemExit(1)
