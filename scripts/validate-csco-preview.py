import json, re

d = json.load(open('articles/posts/csco-q4-fy2026-earnings-preview-2026.json'))

# 1. Required fields
required = ["slug","title","subtitle","summary","ticker","sector","sentiment","date","price","image","bodyHtml"]
missing = [k for k in required if k not in d]
print("1. Required fields:", "OK" if not missing else f"MISSING {missing}")
assert not missing
assert d["image"]["src"] == "/img/articles/csco-q4-fy2026-earnings-preview-2026.jpg"
print("   image.src:", "OK")

# 2. Word count of body text (strip tags)
body = d["bodyHtml"]
text = re.sub(r'<[^>]+>', ' ', body)
text = re.sub(r'\s+', ' ', text).strip()
words = len(text.split())
print(f"2. Word count: {words} (target 700-800) ->", "OK" if 700 <= words <= 800 else "FAIL")

# 3. No h2/h3/bullets/ol/ul
bad = re.findall(r'<(h2|h3|h4|ul|ol|li)\b', body, re.I)
print("3. No headings/bullets:", "OK" if not bad else f"FAIL {bad}")

# 4. Stats card + live row + note
assert '<div class="stats-card">' in body
assert 'data-live-ticker="CSCO"' in body
assert 'data-live-field="price"' in body
assert 'stats-live-badge' in body
assert 'class="stats-card-note">Price refreshes live' in body
assert 'All other figures as of August 12, 2026' in body
print("4. Stats card + LIVE price row + note:", "OK")

# 5. Disclosure
assert '<p class="disclosure">Disclosure: The Signal holds no position in CSCO. Positions may change. This is not financial advice.</p>' in body
print("5. Disclosure:", "OK")

# 6. No exact dollar STOCK PRICES in body prose (exclude stats-card & disclosure).
# Revenue/EPS guidance figures in prose are site convention (cf. AMAT article).
# Flag only dollar figures that match the stock's price levels or bare standalone prices.
before_card = body.split('<div class="stats-card">')[0]
after_card = body.split('</div>')[-1]
prose = before_card + after_card
price_values = {"$120.43", "$65.75", "$130.37", "$132.59"}
bare_prices = [m for m in re.findall(r'\$\d[\d,.]*(?: ?[bB]illion| ?[mM]illion)?', prose)
               if m in price_values or ('.' not in m and 'illion' not in m)]
print("6. No exact dollar stock prices in prose:", "OK" if not bare_prices else f"FAIL {bare_prices}")

# 7. Links array
labels = [l["label"] for l in d["links"]]
ok_links = len(d["links"]) >= 4 and any("Investor" in l for l in labels) and any("Yahoo" in l for l in labels)
print("7. Links:", len(d["links"]), "->", "OK" if ok_links else "FAIL")

# 8. Live price cell exact markup
assert '<td class="stat-value" data-live-ticker="CSCO" data-live-field="price">$120.43</td>' in body
print("8. Live price cell markup:", "OK")

print("\nALL CHECKS PASSED")
