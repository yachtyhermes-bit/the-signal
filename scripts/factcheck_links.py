import json, subprocess, sys

tickers = ['ANET', 'MRVL', 'AVGO', 'LHX', 'NVDA']

# check links
slugs = [
    'arista-ai-data-center-networking-2026',
    'marvell-ai-custom-chips-data-center-2026',
    'broadcom-ai-networking-vmware-dominance-2026',
    'l3harris-defense-avionics-contracts-2026',
    'nvidia-cuda-ai-moat-2026'
]

for s in slugs:
    with open(f'articles/posts/{s}.json') as f:
        a = json.load(f)
    print(f"\n--- Links for {s} ---")
    for link in a.get('links', []):
        url = link['url']
        try:
            r = subprocess.run(['curl', '-sIo', '/dev/null', '-w', '%{http_code}', '--max-time', '5', url], capture_output=True, text=True, timeout=10)
            code = r.stdout.strip()
            print(f"  {code} | {link['label']}: {url}")
        except Exception as e:
            print(f"  FAIL | {link['label']}: {url} - {e}")
