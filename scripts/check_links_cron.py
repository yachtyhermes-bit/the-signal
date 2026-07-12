import json, os, urllib.request, urllib.error, ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

slugs = [
    "lockheed-martin-defense-moat-2026",
    "micron-us-chip-investment-surge-2026",
    "tsmc-ai-chip-monopoly-2026",
    "marvell-ai-switch-asic-rebound-2026",
    "palo-alto-networks-platformization-2026",
    "top-energy-plays-ai-power-2026",
    "oracle-ai-cloud-capex-bet-2026",
    "asml-euv-monopoly-chokepoint-ai-chips",
    "ge-vernova-power-ai-data-centers-2026",
    "credo-ai-connectivity-chips-2026"
]

total_links = 0
bad_links = 0

for slug in slugs:
    fp = f'/home/chino/thesignal/articles/posts/{slug}.json'
    a = json.load(open(fp))
    links = a.get('links', [])
    print(f"\n{slug}:")
    for link in links:
        url = link['url']
        label = link.get('label', 'N/A')[:50]
        total_links += 1
        try:
            req = urllib.request.Request(url, method='HEAD', headers={'User-Agent': 'Mozilla/5.0'})
            resp = urllib.request.urlopen(req, timeout=8, context=ctx)
            code = resp.getcode()
            if code == 200:
                print(f"  OK [{code}] {label}")
            elif code in (301, 302):
                print(f"  OK [{code} redirect] {label}")
            elif code == 403:
                print(f"  OK [403 acceptable] {label}")
            else:
                print(f"  FLAG [{code}] {label}")
                bad_links += 1
        except urllib.error.HTTPError as e:
            code = e.code
            if code in (403, 429):
                print(f"  OK [{code} acceptable] {label}")
            else:
                print(f"  DEAD [{code}] {label}")
                bad_links += 1
        except urllib.error.URLError as e:
            print(f"  DEAD [URLError] {label} - {e.reason}")
            bad_links += 1
        except Exception as e:
            print(f"  DEAD [Error] {label} - {str(e)[:60]}")
            bad_links += 1

print(f"\n\n=== RESULTS: {total_links} total links, {bad_links} bad/dead ===")
