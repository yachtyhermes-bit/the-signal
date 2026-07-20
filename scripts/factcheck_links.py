#!/usr/bin/env python3
"""Check all links in the 5 articles."""
import json, os, subprocess

ARTICLES_DIR = '/home/chino/thesignal/articles/posts'

slugs = [
    'ge-aftermarket-moat-2026',
    'tsm-ai-chip-monopoly-2026',
    'shopify-ai-commerce-moat-ecosystem-2026',
    'hood-fintech-turnaround-profitability-expansion-2026',
    'rtx-defense-supercycle-nato-2026',
]

for slug in slugs:
    path = os.path.join(ARTICLES_DIR, f'{slug}.json')
    with open(path) as f:
        art = json.load(f)
    
    links = art.get('links', [])
    print(f"\n📰 {slug}:")
    
    for link in links:
        url = link.get('url', '')
        label = link.get('label', link.get('text', '?'))
        
        try:
            result = subprocess.run(
                ['curl', '-sI', '-o', '/dev/null', '-w', '%{http_code}', '--connect-timeout', '5', '-m', '10', url],
                capture_output=True, text=True, timeout=15
            )
            status = result.stdout.strip()
            if status in ['200', '301', '302', '308']:
                print(f"  ✅ {status} | {label}")
            elif status in ['403', '429']:
                print(f"  ⚠️ {status} (acceptable) | {label}")
            elif status in ['404', '000']:
                print(f"  🔴 {status} | {label} — FAIL")
            else:
                print(f"  ❓ {status} | {label}")
        except Exception as e:
            print(f"  ❌ error | {label}: {e}")

print("\nDone.")
