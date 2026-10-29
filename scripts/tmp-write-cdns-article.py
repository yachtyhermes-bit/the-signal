import json, re

SLUG = "cdns-record-backlog-agentic-design-2026"

draft = open(f"/tmp/draft-{SLUG}.md", encoding="utf-8").read()
title = re.search(r"^TITLE:\s*(.+)$", draft, re.M).group(1).strip()
subtitle = re.search(r"^SUBTITLE:\s*(.+)$", draft, re.M).group(1).strip()
summary = re.search(r"^SUMMARY:\s*(.+)$", draft, re.M).group(1).strip()
body_md = draft.split("---BODY---", 1)[1].strip()

paras = [p.strip() for p in body_md.split("\n\n") if p.strip()]

card = """<div class="stats-card">
<div class="stats-card-title">The Numbers That Matter</div>
<table class="stats-table">
<tr><td class="stat-label">Price</td><td class="stats-value" data-live-ticker="CDNS" data-live-field="price">$322.17 <span class="stats-live-badge">LIVE</span></td></tr>
<tr><td class="stat-label">Market Cap</td><td class="stat-value">$95.8B</td></tr>
<tr><td class="stat-label">Forward P/E</td><td class="stat-value">32.9x</td></tr>
<tr><td class="stat-label">Total Revenue (TTM)</td><td class="stat-value">$6.13B</td></tr>
<tr><td class="stat-label">52-Week Low</td><td class="stat-value">$262.75</td></tr>
<tr><td class="stat-label">52-Week High</td><td class="stat-value">$416.69</td></tr>
<tr><td class="stat-label">Analyst Consensus</td><td class="stat-value">Strong Buy (25 analysts)</td></tr>
<tr><td class="stat-label">Analyst Target Mean</td><td class="stat-value">$409.89</td></tr>
</table>
<div class="stats-card-note">Price refreshes live &middot; All other figures as of October 27, 2026</div>
</div>"""

html_parts = []
for i, p in enumerate(paras):
    if p.startswith("Disclosure:"):
        html_parts.append('<p class="disclosure">' + p + "</p>")
    else:
        html_parts.append("<p>" + p + "</p>")
    if i == 1:
        html_parts.append(card)

body_html = "\n\n".join(html_parts)
assert chr(92) + '"' not in body_html, "escaped-quote corruption"
assert "class=\"stats-card\"" in body_html
assert 'class="disclosure"' in body_html

data = {
    "slug": SLUG,
    "title": title,
    "subtitle": subtitle,
    "summary": summary,
    "ticker": "CDNS",
    "tickerName": "Cadence Design Systems",
    "company": "Cadence Design Systems, Inc.",
    "sector": "ai",
    "sentiment": "neutral",
    "date": "2026-10-27T18:30:00Z",
    "price": 322.17,
    "featured": False,
    "premium": False,
    "tags": [
        "cadence", "cdns", "eda", "electronic-design-automation", "agentic-ai",
        "ai-super-agents", "maestro", "chip-design", "backlog", "recurring-revenue",
        "earnings", "synopsys",
    ],
    "links": [
        {"label": "Cadence: Q3 2026 financial results and raised 2026 outlook (Oct. 26, 2026) \u2192",
         "url": "https://www.cadence.com/en_US/home/company/newsroom/press-releases/pr-ir/2026/cadence-reports-third-quarter-2026-financial-results.html"},
        {"label": "Cadence Q3 2026 CFO commentary: guidance, backlog, buyback authorization and margin bridge (SEC exhibit 99.02) \u2192",
         "url": "https://www.sec.gov/Archives/edgar/data/813672/000081367226000116/cfocommentary10262026ex9902.htm"},
        {"label": "Cadence Q3 2026 earnings release: segment growth, geography, GAAP-to-non-GAAP reconciliation (SEC exhibit 99.01) \u2192",
         "url": "https://www.sec.gov/Archives/edgar/data/813672/000081367226000116/cdns10262026ex9901.htm"},
        {"label": "Cadence Q3 2026 earnings call transcript: Hexagon margin drag, customer agent deployments, FY27 timing \u2192",
         "url": "https://www.fool.com/earnings/call-transcripts/2026/10/26/cadence-cdns-q3-2026-earnings-call-transcript/"},
        {"label": "Cadence introduces Maestro, a portfolio of domain-specialized AI models \u2192",
         "url": "https://www.cadence.com/en_US/home/company/newsroom/press-releases/pr/2026/cadence-introduces-maestro-a-domain-specialized-ai-model.html"},
        {"label": "OpenAI and Synopsys announce GPT-Synopsys, a chip-design partnership with revenue sharing (Sept. 30, 2026) \u2192",
         "url": "https://news.synopsys.com/2026-09-30-OpenAI-and-Synopsys-Announce-GPT-Synopsys-Frontier-Intelligence-to-Revolutionize-Chip-Design"},
        {"label": "Synopsys Q3 fiscal 2026 results: revenue scale including Ansys \u2192",
         "url": "https://investor.synopsys.com/news/news-details/2026/Synopsys-Posts-Financial-Results-for-Third-Quarter-Fiscal-Year-2026/default.aspx"},
        {"label": "Investor's Business Daily: Cadence beats, raises guidance and the stock reaction \u2192",
         "url": "https://www.investors.com/news/technology/cdns-stock-cadence-design-systems-q3-2026-earnings/"},
    ],
    "meta": {
        "author": "Charles Osi",
        "estimatedReadTime": "5 min",
        "editorialTags": [
            "cadence", "cdns", "eda", "electronic-design-automation", "agentic-ai",
            "ai-super-agents", "chip-design", "recurring-revenue", "backlog",
            "gaap-margin-compression", "synopsys-openai", "hexagon-integration",
        ],
        "seoKeywords": [
            "CDNS stock",
            "Cadence Q3 2026 earnings",
            "Cadence record backlog $8.2 billion",
            "Cadence Maestro AI models",
            "Cadence AI Super Agents",
            "Cadence recurring revenue growth",
            "Cadence non-GAAP operating margin",
            "Cadence vs Synopsys EDA",
            "GPT-Synopsys OpenAI chip design",
            "Cadence 2026 guidance raise",
        ],
        "relatedTickers": ["CDNS", "ANET", "AVGO"],
        "keyMetrics": {
            "Price": 322.17,
            "Market Cap": "$95.8B",
            "Forward P/E": "32.9x",
            "Total Revenue (TTM)": "$6.13B",
            "52-Week Low": 262.75,
            "52-Week High": 416.69,
            "Analyst Consensus": "Strong Buy (25 analysts)",
            "Analyst Target Mean": 409.89,
        },
    },
    "bodyHtml": body_html,
    "image": {
        "src": f"/img/articles/{SLUG}.jpg",
        "fit": "cover",
        "caption": "A chip designer reviewing a processor floorplan at an EDA workstation. Cadence sells the software that turns a chip idea into a manufacturable layout. Photo: The Signal / AI-generated.",
        "alt": "Semiconductor design engineer at a workstation reviewing a dense chip floorplan on a wide display beside a schematic view",
    },
}

path = f"articles/posts/{SLUG}.json"
with open(path, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

words = len(re.sub(r"<[^>]+>", " ", body_html).split())
print("wrote", path)
print("title:", title)
print("words:", words)
print("paras:", len(paras))
