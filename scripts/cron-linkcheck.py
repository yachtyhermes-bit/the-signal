#!/usr/bin/env python3
"""Check all links from 5 articles."""
import json, subprocess, sys

articles = [
    'ge-aftermarket-moat-2026',
    'coreweave-ai-factory-moat-2026',
    'panw-ai-security-cash-flow-machine-2026',
    'net-cloudflare-precursor-agentic-internet-2026',
    'arm-agi-cpu-custom-silicon-bet-2026',
]

for slug in articles:
    print(f'=== {slug} ===')
    with open(f'articles/posts/{slug}.json') as f:
        a = json.load(f)
    for link in a.get('links', []):
        url = link['url']
        label = link.get('label', '')
        try:
            r = subprocess.run(['curl', '-sI', '-o', '/dev/null', '-w', '%{http_code}', '--max-time', '10', url],
                             capture_output=True, timeout=15)
            code = r.stdout.decode().strip()
            if code in ('200', '301', '302', '308'):
                print(f'  ✅ [{code}] {label[:40]}')
            elif code in ('403', '429', '401'):
                print(f'  ⚠️  [{code}] {label[:40]} (paywall/bot block — acceptable)')
            else:
                print(f'  ❌ [{code}] {label[:40]} — {url}')
        except subprocess.TimeoutExpired:
            print(f'  ⏱️  TIMEOUT {label[:40]} — {url}')
        except Exception as e:
            print(f'  ❌ ERROR {label[:40]}: {e}')
    print()
