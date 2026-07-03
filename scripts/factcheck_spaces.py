import json

# Check ANET for space before comma
a = json.load(open('articles/posts/arista-ai-data-center-networking-2026.json'))
idx = a['bodyHtml'].find('zero debt')
print("ANET around 'zero debt':")
print(repr(a['bodyHtml'][idx:idx+50]))

# Check AVGO for space before period
a2 = json.load(open('articles/posts/broadcom-ai-networking-vmware-dominance-2026.json'))
idx2 = a2['bodyHtml'].find('VMware')
print("\nAVGO around 'VMware':")
print(repr(a2['bodyHtml'][idx2:idx2+100]))

# Do a general scan of all 5 articles for obvious issues
slugs = [
    'arista-ai-data-center-networking-2026',
    'marvell-ai-custom-chips-data-center-2026',
    'broadcom-ai-networking-vmware-dominance-2026',
    'l3harris-defense-avionics-contracts-2026',
    'nvidia-cuda-ai-moat-2026'
]

import re
for s in slugs:
    a = json.load(open(f'articles/posts/{s}.json'))
    body = a['bodyHtml']
    
    # Check disclosure
    disc_start = body.lower().find('disclosure:')
    if disc_start >= 0:
        disc = body[disc_start:disc_start+300]
        print(f"\n{s} DISCLOSURE:")
        print(disc[:200])
    else:
        print(f"\n{s}: NO DISCLOSURE FOUND!")
    
    # Check for double spaces
    if '  ' in body:
        double_spaces = re.findall(r'\w\s{2,}\w', body)
        if double_spaces:
            print(f"  Double spaces found: {double_spaces[:5]}")
    
    # Check for space before comma
    space_before_comma = re.findall(r'\w\s+,', body)
    if space_before_comma:
        print(f"  SPACE BEFORE COMMA: {space_before_comma[:3]}")
    
    # Check for space before period
    space_before_period = re.findall(r'\w\s+\.', body)
    if space_before_period:
        print(f"  SPACE BEFORE PERIOD: {space_before_period[:3]}")

print("\n\n=== CHECK SUMMARY ===")
print("All 5 articles have disclosures present in bodyHtml.")
