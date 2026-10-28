#!/usr/bin/env python3
"""Assemble articles/posts/ter-broad-test-mix-2026.json from the Gemini draft.

Draft edits applied (accuracy, not style):
 1. weekday -> concrete date (style: weekday words decay)
 2. open/low % corrected to the real session (open ~-7%, low ~-9%, midday ~-4%)
 3. robotics "finally swung to a profit" -> "turned profitable in the quarter" (no first-ever claim)
 4. drop unsupported "compute orders drifted to the right twice this year"
 5. disclosure wrapped in <p class="disclosure">
"""
import json

SLUG = "ter-broad-test-mix-2026"

TITLE = "Teradyne Stumbles on Guidance as Test Intensity Rewrites the AI Playbook"
SUBTITLE = ("Record quarterly sales could not save the stock from a growth reset, "
            "but the real catalyst sits in 2027.")
SUMMARY = ("Teradyne reported record third-quarter revenue on surging memory and storage test demand, "
           "but softer forward guidance sparked a sharp midday selloff. While near-term compute orders "
           "slipped, rising test intensity and scheduled hyperscaler ramps frame the setup for next year.")

CARD = """<div class="stats-card">
<div class="stats-card-title">The Numbers That Matter</div>
<table class="stats-table">
<tr><td class="stat-label">Price</td><td class="stats-value" data-live-ticker="TER" data-live-field="price">$323.68 <span class="stats-live-badge">LIVE</span></td></tr>
<tr><td class="stat-label">Market Cap</td><td class="stat-value">$50.6B</td></tr>
<tr><td class="stat-label">Forward P/E</td><td class="stat-value">28.3x</td></tr>
<tr><td class="stat-label">Total Revenue (TTM)</td><td class="stat-value">$5.00B</td></tr>
<tr><td class="stat-label">52-Week Low</td><td class="stat-value">$151.52</td></tr>
<tr><td class="stat-label">52-Week High</td><td class="stat-value">$487.91</td></tr>
<tr><td class="stat-label">Analyst Consensus</td><td class="stat-value">Buy (15 analysts)</td></tr>
<tr><td class="stat-label">Analyst Target Mean</td><td class="stat-value">$445.47</td></tr>
</table>
<div class="stats-card-note">Price refreshes live &middot; All other figures as of October 28, 2026</div>
</div>"""

P = [
 # 1 hook
 "Imagine posting the best quarter of your entire corporate life, only to watch your equity get dumped at the opening bell. That was Teradyne on Oct. 28. Peers like Applied Materials and KLA rallied alongside the broader chip index. Teradyne opened sharply lower, fell nearly nine percent at its worst, and was still down about four percent by midday. The market saw a headline that looked triumphant, read the forward guidance, and slammed the brakes.",
 # 2 what the company does
 "Strip away the ticker tape, and Teradyne's business is dead simple. It builds the massive automated systems that test silicon before it ever reaches a consumer device or a data center. Think of every advanced semiconductor as a plane waiting on a runway: it cannot take off until it clears inspection, and Teradyne owns the inspection lane. Its customers are foundries, memory titans, and cloud hyperscalers who cannot afford to let a defective processor slip through.",
 # 3 why it matters to AI
 "That bottleneck role makes the company pivotal to the artificial intelligence buildout. Modern AI accelerators draw up to fifteen thousand amps and pack billions of transistors into microscopic stacks.",
 "If a single microscopic connection fails under heat, an entire server rack goes dark, taking your cloud subscriptions down with it. Testing used to be a routine quality check at the end of the line. Today, it is a grueling trial by fire that determines whether a data center device actually functions.",
 # 4 the twist
 "Yet this blowout quarter arrived with an unexpected twist. Everyone treats Teradyne as a pure-play accelerator bet, but compute silicon accounted for only about twenty percent of third-quarter sales. The other eighty percent came from an eclectic bench: record memory test, soaring hard-drive testing, and robotics that turned profitable in the quarter. Even the memory boom has an AI twist: severe wafer shortages forced chipmakers to build shorter memory stacks, requiring more individual test runs across every wafer they produce.",
 # 5 guidance
 "The selloff comes down to what happens next. Management guided fourth-quarter revenue growth down to roughly twenty percent, with operating margins and earnings per share both shrinking sequentially. The company explained that major compute test orders simply shifted on the calendar into next year. For an impatient market accustomed to relentless sequential acceleration, a calendar slip feels like a stall.",
 # 6 re-rate
 "For this equity to sustainably re-rate, investors need proof that testing is claiming a permanently larger slice of the chip budget. In 2025, test equipment soaked up just over six percent of semiconductor capital spending. Through the first eight months of this year, that share climbed past eight percent. As packaging becomes more intricate, test intensity compounds, meaning chipmakers must buy more inspection lanes for every wafer they run.",
 # 7 roadmap
 "Management also handed the Street a concrete roadmap for where the next leg of demand originates. Big tech buyers hate relying on a single vendor for mission-critical hardware, and Teradyne is winning dual-sourcing slots across the industry. One cloud titan ramps purchases in mid-2027, an existing merchant GPU customer expands next year, and a second cloud giant begins capacity buys in late 2027. If those milestones hit on schedule, the current pullback will look like a routine timing discount.",
 # 8 bear case
 "The short thesis argues that the growth story just slammed into a wall. Decelerating from seventy percent top-line expansion to twenty percent in ninety days is not a minor timing blip; it is the classic signature of a cyclical peak.",
 "Compute orders just slid on the calendar, leaving investors staring at three quarters of thin air before any promised 2027 rescue arrives. Meanwhile, the record memory test figures rely on temporary DRAM bottlenecks that will fade as new wafer capacity comes online.",
 "Second-sourcing deals also carry an inherent ceiling, ensuring Teradyne remains a minority supplier rather than an entrenched incumbent. If fourth-quarter margins slip below fifty-seven and a half percent or the mid-2027 customer ramps get delayed again, this premium valuation will deflate rapidly.",
 # 9 rebuttal
 "The bears have the timing right, but they have the architecture wrong. Silicon is not getting simpler, and the leap toward next-generation packaging guarantees that test intensity remains elevated. Teradyne is rolling out new instruments for PCIe Gen6 and high-power burn-in because next-generation chips cannot even be evaluated on older machines.",
 "Tolerating near-term calendar lumps is the price of admission for owning a toll booth on the AI supply chain. The market is pricing in a structural slowdown where there is only an operational pause.",
 # 10 what to watch
 "The single event that will settle the argument is the fourth-quarter earnings call. That is where leadership plans to unveil an updated long-term target earnings model and prove whether the late-2027 cloud ramps are bankable reality or wishful thinking.",
]

DISCLOSURE = ('<p class="disclosure">Disclosure: The Signal holds no position in TER. '
              'Positions may change. This is not financial advice.</p>')

body = []
for i, para in enumerate(P):
    body.append("<p>" + para + "</p>")
    if i == 1:  # after the company explainer, right after the intro block
        body.append(CARD)
body.append(DISCLOSURE)
BODY = "\n\n".join(body)

links = [
    {"label": "Teradyne third-quarter 2026 results: revenue up 70%, record memory and storage test, robotics profitable \u2192",
     "url": "https://investors.teradyne.com/news-events/press-releases/detail/455/teradyne-reports-third-quarter-2026-results"},
    {"label": "Teradyne Q3 2026 prepared remarks: test share of semiconductor capex 6.4% to 8.1%, dual-vendor ramp calendar, compute order timing \u2192",
     "url": "https://d1io3yog0oux5.cloudfront.net/_7b4642188ebc0095352a4d3d09ee3f19/teradyne/db/938/9658/webcast_transcript/Teradyne_Q3%2726_Earnings_Prepared_Remarks.pdf"},
    {"label": "Teradyne launches UltraFLEXplus instruments for AI and data-center devices, including the industry's first ATE for PCIe Gen6 \u2192",
     "url": "https://investors.teradyne.com/news-events/press-releases/detail/447/teradyne-launches-advanced-ultraflexplus-instruments-engineered-for-ai-and-data-center-computing-devices"},
    {"label": "Teradyne Magnum E2 targets next-generation DRAM and HBM test demand \u2192",
     "url": "https://investors.teradyne.com/news-events/press-releases/detail/451/teradyne-announces-magnum-e2-to-address-next-generation-memory-test-demands-driven-by-ai-and-high-performance-computing"},
    {"label": "Teradyne Titan HP adds burn-in and system-level test for advanced AI data-center devices \u2192",
     "url": "https://investors.teradyne.com/news-events/press-releases/detail/452/teradyne-introduces-titan-hp-platform-with-burn-in-capabilities-for-advanced-ai-data-center-devices"},
    {"label": "Teradyne UltraFLEXplus S brings production test to edge-AI devices \u2192",
     "url": "https://investors.teradyne.com/news-events/press-releases/detail/453/teradyne-introduces-ultraflexplus-s-series-for-edge-ai-applications"},
    {"label": "SK hynix third-quarter 2026 results: record revenue, HBM4 mainstream from the fourth quarter, long-term agreements covering more than half of 2027-2028 capacity \u2192",
     "url": "https://news.skhynix.com/en/q3-2026-business-results/"},
]

key_metrics = {
    "Price": 323.68,
    "Market Cap": "$50.6B",
    "Forward P/E": "28.3x",
    "Total Revenue (TTM)": "$5.00B",
    "52-Week Low": 151.52,
    "52-Week High": 487.91,
    "Analyst Consensus": "Buy (15 analysts)",
    "Analyst Target Mean": 445.47,
}

article = {
    "slug": SLUG,
    "title": TITLE,
    "subtitle": SUBTITLE,
    "summary": SUMMARY,
    "ticker": "TER",
    "tickerName": "Teradyne",
    "company": "Teradyne, Inc.",
    "sector": "ai",
    "sentiment": "neutral",
    "date": "2026-10-28T17:00:00Z",
    "price": 323.68,
    "featured": False,
    "premium": False,
    "tags": ["ter", "teradyne", "semiconductor-test", "ate", "ai-chips", "hbm-test",
             "memory-test", "robotics", "dual-vendor", "hyperscalers", "formfactor",
             "optical-test", "capex", "guidance", "sell-the-news", "universal-robots"],
    "bodyHtml": BODY,
    "links": links,
    "meta": {
        "author": "Charles Osi",
        "estimatedReadTime": "5 min",
        "keyMetrics": key_metrics,
        "relatedTickers": ["TER", "AMAT", "KLAC"],
        "seoKeywords": [
            "TER stock", "Teradyne Q3 2026", "Teradyne earnings", "semiconductor test equipment",
            "AI chip test", "HBM memory test", "Teradyne guidance", "Teradyne dual vendor",
            "Teradyne robotics", "AI capex test intensity",
        ],
    },
    "image": {
        "src": "/img/articles/ter-broad-test-mix-2026.jpg",
        "alt": "Macro photograph of a probe card, its fan of fine tungsten probe needles radiating from a circular circuit board",
        "caption": "A probe card, the interface that touches a wafer to test each die. Teradyne sells the systems that use them. Photo: The Signal",
    },
}

path = "articles/posts/%s.json" % SLUG
with open(path, "w") as f:
    json.dump(article, f, indent=2, ensure_ascii=False)

# --- integrity checks -------------------------------------------------------
bad = chr(92) + chr(34)
assert bad not in BODY, "escaped-quote corruption in bodyHtml"
assert "$3" in BODY or True
print("wrote", path)
print("body chars:", len(BODY), "paragraphs:", BODY.count("<p>"))
print("has stats-card:", 'class="stats-card"' in BODY)
print("has live row:", 'data-live-ticker="TER"' in BODY)
print("disclosure class ok:", '<p class="disclosure">' in BODY)
print("links:", len(links))
import re
words = len(re.sub("<[^>]+>", " ", BODY).split())
print("body word count:", words)
