import json

articles = [
    'arista-ai-data-center-networking-2026',
    'marvell-ai-custom-chips-data-center-2026',
    'broadcom-ai-networking-vmware-dominance-2026',
    'l3harris-defense-avionics-contracts-2026',
    'nvidia-cuda-ai-moat-2026'
]
for s in articles:
    with open(f'articles/posts/{s}.json') as f:
        a = json.load(f)
    print(f"\n===== {s} =====")
    print(f"TITLE: {a['title']}")
    print(f"SUBTITLE: {a['subtitle']}")
    print(f"SUMMARY: {a['summary']}")
    print(f"PRICE: {a.get('price', 'N/A')}")
    if 'disclosure' in a.get('bodyHtml', '').lower():
        idx = a['bodyHtml'].lower().find('disclosure')
        print(f"DISCLOSURE FOUND at bodyHtml index {idx}")
    else:
        print("NO DISCLOSURE FOUND in bodyHtml")
    print(f"BODY LENGTH: {len(a['bodyHtml'])} chars")
