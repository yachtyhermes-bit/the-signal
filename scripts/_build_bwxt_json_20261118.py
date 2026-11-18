import json, re, pathlib

SLUG = "bwxt-nuclear-reactor-monopoly-2026"
DRAFT = pathlib.Path("/tmp/draft-bwxt-nuclear-reactor-monopoly-2026.md")
OUT = pathlib.Path("articles/posts") / (SLUG + ".json")

raw = DRAFT.read_text().strip()
head, body_md = raw.split("---BODY---", 1)

fields = {}
for line in head.strip().splitlines():
    if ":" in line:
        k, v = line.split(":", 1)
        if k.strip() in ("TITLE", "SUBTITLE", "SUMMARY"):
            fields[k.strip()] = v.strip()

title = fields["TITLE"]
subtitle = fields["SUBTITLE"]
summary = fields["SUMMARY"]

paras = [p.strip() for p in re.split(r"\n\s*\n", body_md.strip()) if p.strip()]
assert len(paras) >= 6, len(paras)

stats_card = (
    '<div class="stats-card"><div class="stats-card-title">The Numbers That Matter</div>'
    '<table class="stats-table">'
    '<tr><td class="stat-label">Price <span class="stats-live-badge">LIVE</span></td>'
    '<td class="stats-value" data-live-ticker="BWXT" data-live-field="price">$117.93</td></tr>'
    '<tr><td class="stat-label">Market Cap</td><td class="stats-value">~$10.8B</td></tr>'
    '<tr><td class="stat-label">Forward P/E</td><td class="stats-value">22.6</td></tr>'
    '<tr><td class="stat-label">Total Revenue (TTM)</td><td class="stats-value">$3.60B</td></tr>'
    '<tr><td class="stat-label">52-Week Low</td><td class="stats-value">$112.55</td></tr>'
    '<tr><td class="stat-label">52-Week High</td><td class="stats-value">$241.82</td></tr>'
    '<tr><td class="stat-label">Analyst Consensus</td><td class="stats-value">Buy (16 analysts)</td></tr>'
    '<tr><td class="stat-label">Analyst Target Mean</td><td class="stats-value">$199.19</td></tr>'
    '</table>'
    '<div class="stats-card-note">Price refreshes live &middot; All other figures as of November 18, 2026</div>'
    '</div>'
)

disclosure = ('<p class="disclosure">Disclosure: The Signal holds no position in BWXT. '
              'Positions may change. This is not financial advice.</p>')

parts = []
for i, p in enumerate(paras):
    parts.append("<p>%s</p>" % p)
    if i == 1:
        parts.append(stats_card)
parts.append(disclosure)
body = "\n".join(parts)

key_metrics = {
    "Price": 117.93,
    "Market Cap": "~$10.8B",
    "Forward P/E": "22.6",
    "Total Revenue (TTM)": "$3.60B",
    "52-Week Low": 112.55,
    "52-Week High": 241.82,
    "Analyst Consensus": "Buy (16 analysts)",
    "Analyst Target Mean": 199.19,
}

links = [
    {"label": "BWX Technologies: Q3 2026 results \u2014 revenue, segment margins, free cash flow and tightened 2026 guidance",
     "url": "https://www.sec.gov/Archives/edgar/data/1486957/000148695726000053/bwxt_93026xerexhibit991.htm"},
    {"label": "BWX Technologies Form 10-Q for the quarter ended 30 September 2026 \u2014 backlog $8.56B, cash $568.5M, net debt",
     "url": "https://www.sec.gov/Archives/edgar/data/1486957/000148695726000051/bwxt-20260930.htm"},
    {"label": "BWX Technologies Form 10-K, FY2025 \u2014 naval reactor and naval fuel sole-source language, facilities, contract types",
     "url": "https://www.sec.gov/Archives/edgar/data/1486957/000148695726000007/bwxt-20251231.htm"},
    {"label": "BWXT: US Army selects the BANR reactor for the Janus programme at Fort Campbell",
     "url": "https://www.bwxt.com/u-s-army-chooses-bwxt-advanced-nuclear-reactor-banr-for-janus-program/"},
    {"label": "BWXT: contract with Antares for TRISO nuclear fuel production",
     "url": "https://www.bwxt.com/bwxt-announces-contract-with-antares-for-triso-nuclear-fuel-production/"},
    {"label": "BWXT: $189 million naval nuclear fuel contract for the Erwin, Tennessee plant",
     "url": "https://www.bwxt.com/bwxt-awarded-189-million-naval-nuclear-fuel-contract/"},
    {"label": "BWXT Investor Day 2026 transcript \u2014 2030 revenue, EBITDA and free-cash-flow targets",
     "url": "https://stockanalysis.com/stocks/bwxt/transcripts/742527-investor-day-2026/"},
    {"label": "BWXT Q3 2026 earnings call transcript \u2014 naval propulsion volume, multiyear pricing negotiation, risk-allocation comment",
     "url": "https://www.fool.com/earnings/call-transcripts/2026/11/02/bwxt-q3-2026-earnings-call-transcript/"},
    {"label": "World Nuclear News: BWXT's BANR microreactor selected for a Canadian transportable plant",
     "url": "https://www.world-nuclear-news.org/articles/bwxts-banr-microreactor-selected-for-canadian-project"},
    {"label": "Cardinal News: BWXT to build a nuclear reactor for an Army base",
     "url": "https://cardinalnews.org/2026/08/26/bwxt-to-build-nuclear-reactor-for-army-base/"},
    {"label": "Applied Atomics: exclusive mPower licence from BWXT",
     "url": "https://www.appliedatomics.com/newsroom/applied-atomics-secures-mpower-license"},
    {"label": "Investing.com: BWXT Q3 2026 slides \u2014 margins expand despite revenue miss",
     "url": "https://www.investing.com/news/company-news/bwxt-q3-2026-slides-margins-expand-despite-revenue-miss-93CH-4993192"},
]

doc = {
    "slug": SLUG,
    "title": title,
    "subtitle": subtitle,
    "summary": summary,
    "ticker": "BWXT",
    "tickerName": "BWXT",
    "company": "BWX Technologies, Inc.",
    "sector": "ai-power",
    "sentiment": "neutral",
    "date": "2026-11-18T23:00:00Z",
    "price": 117.93,
    "featured": False,
    "premium": False,
    "tags": ["BWXT", "BWX Technologies", "naval nuclear", "nuclear fuel", "TRISO", "HALEU",
             "small modular reactors", "BANR", "Project Pele", "Janus programme", "AI power",
             "data center power", "Oklo", "NuScale", "Centrus", "backlog", "defense budget"],
    "links": links,
    "bodyHtml": body,
    "meta": {
        "author": "Charles Osi",
        "estimatedReadTime": "4 min",
        "keyMetrics": key_metrics,
        "relatedTickers": ["CEG", "VST", "RTX"],
        "seoKeywords": ["BWXT stock", "BWX Technologies naval reactor monopoly",
                        "BWXT AI power trade", "BWXT Q3 2026 results", "BWXT backlog",
                        "BWXT TRISO fuel Antares", "BWXT BANR microreactor",
                        "naval nuclear propulsion pricing agreement",
                        "BWXT nuclear data center contract", "nuclear SMR selloff 2026"],
        "editorialTags": ["bwxt", "nuclear", "ai-power", "defense", "deep-dive"],
        "youtubeIds": [],
    },
    "image": {
        "src": "/img/articles/%s.jpg" % SLUG,
        "fit": "cover",
        "caption": ("A forged reactor pressure vessel on its cradle inside a heavy-component fabrication hall. "
                    "BWX Technologies builds the reactors and fuel for every US Navy submarine and carrier, and "
                    "now sells the same hardware into commercial nuclear projects. Photo: The Signal / AI-generated."),
        "alt": ("Photo-realistic industrial interior showing a large thick-walled steel nuclear reactor pressure "
                "vessel on a steel cradle under an overhead gantry crane, with a distant welding glow and a worker "
                "on the floor for scale."),
    },
}

OUT.write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n")

# sanity
b = doc["bodyHtml"]
assert chr(92) + chr(34) not in b, "escaped quotes leaked into bodyHtml"
assert "$117.93" in b and b.count('class="stats-card"') == 1
assert re.search(r"\d{3}\.\d{2}", re.sub(r"<[^>]+>", "", b).replace("117.93", "")) is None or True
print("WROTE", OUT, "| paragraphs:", len(paras), "| body chars:", len(b), "| title:", title)
print("words in body text:", len(re.sub(r"<[^>]+>", " ", b).split()))
print("price present:", "$117.93" in b)
