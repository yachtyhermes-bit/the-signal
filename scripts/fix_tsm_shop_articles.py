#!/usr/bin/env python3
"""Fix TSM and SHOP articles: remove stock price from body, fix TSM capex figure."""
import json

# ============ FIX 1: TSM - remove price from body, fix capex ============
tsm_path = 'articles/posts/tsm-ai-chip-monopoly-2026.json'
with open(tsm_path) as f:
    tsm = json.load(f)

old_body = tsm['bodyHtml']
new_body = old_body

# Fix 1a: Remove stock price from body
if 'TSM at $398.37' in new_body:
    new_body = new_body.replace('TSM at $398.37', 'TSM')
    print("TSM: Removed stock price $398.37 from body")

# Fix 1b: Fix capex claim - $120B is wrong, actual is ~$35-40B
if 'spends over $120 billion a year on capital expenditures' in new_body:
    new_body = new_body.replace(
        'spends over $120 billion a year on capital expenditures',
        'spends over $35 billion a year on capital expenditures'
    )
    print("TSM: Fixed capex from $120B to $35B")
elif 'spends over $120 billion' in new_body:
    new_body = new_body.replace(
        'spends over $120 billion',
        'spends over $35 billion'
    )
    print("TSM: Fixed capex from $120B to $35B")

tsm['bodyHtml'] = new_body
with open(tsm_path, 'w') as f:
    json.dump(tsm, f, indent=2)
print("TSM: Saved")

# ============ FIX 2: SHOP - remove price from body ============
shop_path = 'articles/posts/shopify-ai-commerce-moat-ecosystem-2026.json'
with open(shop_path) as f:
    shop = json.load(f)

old_body2 = shop['bodyHtml']
new_body2 = old_body2

if 'Shopify at $123.56' in new_body2:
    new_body2 = new_body2.replace('Shopify at $123.56,', 'Shopify,')
    print("SHOP: Removed stock price $123.56 from body")

shop['bodyHtml'] = new_body2
with open(shop_path, 'w') as f:
    json.dump(shop, f, indent=2)
print("SHOP: Saved")

# ============ VERIFICATION ============
for path, label in [(tsm_path, 'TSM'), (shop_path, 'SHOP')]:
    with open(path) as f:
        art = json.load(f)
    body = art['bodyHtml']
    price = art.get('price')
    import re
    price_str = f'${price:.2f}' if price else str(price)
    if price_str in body:
        print(f"⚠️ {label}: Price ${price} STILL in body!")
    else:
        print(f"✅ {label}: Price ${price} removed from body")
    
    # Verify capex fix in TSM
    if label == 'TSM':
        if '$35 billion' in body:
            print(f"✅ TSM: Capex fixed to $35 billion")
        elif '$120' in body:
            idx = body.find('$120')
            ctx = body[max(0,idx-30):idx+50]
            print(f"⚠️ TSM: '$120' still present near: ...{ctx}...")
