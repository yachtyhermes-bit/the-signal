import json

slug = 'rbrk-cyber-resilience-secular-growth-2026'

with open(f'articles/posts/{slug}.json') as f:
    a = json.load(f)

body = a['bodyHtml']
old = "Cash flow flipped from negative to four hundred and forty million in positive free cash flow."
new = "Cash flow flipped from negative to nearly three hundred million in positive free cash flow."

if old in body:
    body = body.replace(old, new)
    a['bodyHtml'] = body
    with open(f'articles/posts/{slug}.json', 'w') as f:
        json.dump(a, f, indent=2)
    print(f"✅ Fixed RBRK FCF claim: '$440M' → 'nearly $300M'")
else:
    print("❌ Could not find the old string to replace")
    # Try fuzzy match
    if 'four hundred and forty' in body:
        print("Found 'four hundred and forty' — attempting partial replacement")
        body = body.replace('four hundred and forty', 'nearly three hundred')
        a['bodyHtml'] = body
        with open(f'articles/posts/{slug}.json', 'w') as f:
            json.dump(a, f, indent=2)
        print("✅ Fixed via partial replacement")
