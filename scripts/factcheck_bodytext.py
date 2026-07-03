import json, subprocess, re

slugs = [
    'arista-ai-data-center-networking-2026',
    'marvell-ai-custom-chips-data-center-2026',
    'broadcom-ai-networking-vmware-dominance-2026',
    'l3harris-defense-avionics-contracts-2026',
    'nvidia-cuda-ai-moat-2026'
]

# Extract all text from each article for manual review
for s in slugs:
    with open(f'articles/posts/{s}.json') as f:
        a = json.load(f)
    
    print(f"\n{'='*60}")
    print(f"ARTICLE: {s}")
    print(f"{'='*60}")
    print(f"TITLE: {a['title']}")
    print(f"SUBTITLE: {a['subtitle']}")
    print(f"SUMMARY: {a['summary']}")
    
    # Extract body text
    body = a['bodyHtml']
    # Remove HTML tags
    text = re.sub(r'<[^>]+>', ' ', body)
    text = re.sub(r'&[a-z]+;', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    
    print(f"\nBODY TEXT ({len(text)} chars):")
    print(text[:3000])
    print("...")
    print(text[-500:])
