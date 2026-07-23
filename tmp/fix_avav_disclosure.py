import json, re

# Fix AVAV disclosure
slug = 'avav-counterdrone-switchblade-contracts-2026'

with open('articles/posts/' + slug + '.json') as f:
    a = json.load(f)

body = a['bodyHtml']
old_disclosure = '<p class="disclosure"><em>Disclosure: The Signal holds no position in AVAV.</em></p>'
new_disclosure = '<p class="disclosure"><em>Disclosure: The Signal holds no position in AVAV. Positions may change. This is not financial advice.</em></p>'

if old_disclosure in body:
    body = body.replace(old_disclosure, new_disclosure)
    a['bodyHtml'] = body
    with open('articles/posts/' + slug + '.json', 'w') as f:
        json.dump(a, f, indent=2)
    print("Fixed AVAV disclosure: added standard suffix")
else:
    print("Could not find old disclosure")
    print("Contains 'Disclosure: The Signal':", 'Disclosure: The Signal' in body)
    # Find the disclosure paragraph
    discl_matches = re.findall(r'<p[^>]*class="disclosure"[^>]*>.*?</p>', body, re.DOTALL)
    print("Found disclosure paragraphs:", discl_matches)
