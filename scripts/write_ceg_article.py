#!/usr/bin/env python3
"""Generate the CEG article JSON for The Signal Mid-Day edition (2026-08-23)."""
import json
import os

STATS_CARD = (
    '<div class="stats-card"><div class="stats-card-title">The Numbers That Matter</div>'
    '<table class="stats-table">'
    '<tr><td class="stat-label">CEG Price<span class="stats-live-badge">LIVE</span></td>'
    '<td class="stat-value" data-live-ticker="CEG" data-live-field="price">$272.88</td></tr>'
    '<tr><td class="stat-label">Market Cap</td><td class="stat-value">$96.7B</td></tr>'
    '<tr><td class="stat-label">Forward P/E</td><td class="stat-value">20.5</td></tr>'
    '<tr><td class="stat-label">Total Revenue (TTM)</td><td class="stat-value">$31.3B</td></tr>'
    '<tr><td class="stat-label">52-Week Low</td><td class="stat-value">$228.63</td></tr>'
    '<tr><td class="stat-label">52-Week High</td><td class="stat-value">$412.70</td></tr>'
    '<tr><td class="stat-label">Analyst Consensus</td><td class="stat-value">Buy</td></tr>'
    '<tr><td class="stat-label">Analyst Target Mean</td><td class="stat-value">$347.40</td></tr>'
    '</table>'
    '<div class="stats-card-note">Price refreshes live · All other figures as of August 21, 2026</div>'
    '</div>'
)

DISCLOSURE = (
    '<p class="disclosure">Disclosure: The Signal holds no position in CEG. '
    'Positions may change. This is not financial advice.</p>'
)

INTRO = [
    "Nvidia just told its customers the party's getting pricier: price hikes of 15% or more on AI chips and servers, per the wires this week. And in the same breath, the company quietly bought a stake in Cloverleaf Infrastructure — a firm whose entire job is building power for data centers. You don't need to read between the lines here. The world's biggest chipmaker just told you exactly where the AI bottleneck lives now. It isn't chips. It's electricity.",
    "Think about it. Every data center needs power before it can run a single GPU, and the hyperscalers are already stacking multi-decade contracts for the stuff years in advance. Whoever wins the chip wars — Nvidia, AMD, someone you haven't heard of yet — they all plug into the same grid. So the smart money is following the plug, not the chip. And the biggest plug in America belongs to Constellation Energy.",
    "Constellation Energy owns and runs America's biggest fleet of nuclear power plants and sells that carbon-free electricity to whoever needs it around the clock. We're talking roughly 19,000 megawatts across about 20 reactors — more carbon-free power than anyone else in the country. Regular homes buy it, sure. But the customers that matter now are the hyperscalers and mega-retailers signing twenty-year contracts for the stuff.",
    "Here's why that matters for AI: nuclear is the only massive source of round-the-clock, emissions-free power you can actually sign a contract for today. Solar and wind are great until the sun sets and the wind stops. Natural gas is reliable but dirty. Data centers don't sleep, which means their power can't either — and Constellation is the one company with the fleet to back that promise in writing.",
]

BODY = [
    "The proof is in the contract stack. Microsoft signed a 20-year deal for the entire output of the restarted Three Mile Island plant — 835 megawatts, reborn as the Crane Clean Energy Center. The original plan had it back online in 2028; a federal waiver this summer pulled the restart forward to 2027, and the Department of Energy chipped in a billion-dollar loan to make it happen. Think about that: the most famous nuclear plant in American history, resurrected because an AI company needs its electrons.",
    "It's not just Microsoft. Meta locked in its own 20-year nuclear deal at Constellation's Clinton plant in Illinois back in June of last year. Then came Walmart, inking the first nuclear power purchase agreement in the retailer's history — a 15-year deal in Illinois. That one landed with a second quarter that had Constellation beating earnings estimates and raising guidance, all while stacking 920 megawatts of fresh clean-power contracts in a single stretch.",
    "And in January, Constellation closed its roughly $16.6 billion purchase of Calpine, instantly becoming the largest wholesale power producer in the United States. First-quarter revenue roughly doubled on the strength of it. The strategic logic is simple: the nuclear fleet anchors the AI contracts, and the added scale means one company can sign a data center up for two decades of power — and actually deliver.",
    "That's the moat, and it's a wide one. You can't spin up a nuclear fleet in a decade; the plants Constellation already runs took decades and billions to build, license, and perfect. No rival can replicate that overnight, no matter how much AI money is chasing megawatts. The company is essentially selling the AI buildout its most precious resource: guaranteed, around-the-clock, carbon-free power. That's a pick-and-shovel business if there ever was one.",
    "Now the honest part, because this isn't a one-way trade. The stock is down roughly a quarter from its highs this year, and there are real reasons: the Calpine integration is capital-hungry, nuclear uprates cost serious cash, free cash flow is negative right now, and the balance sheet carries something like $25 billion in debt. Skeptics will tell you the AI power story is already priced in, or that execution risk is real. Fair. But here's the thing — the demand isn't hypothetical. The contracts are signed. The plants are being restarted.",
    "Wall Street still sees the upside. The consensus is a Buy, with a price target that sits well above where shares trade today. And the thesis keeps compounding: Nvidia isn't just raising prices, it's investing in power developers — the chip giant itself is betting that electricity, not silicon, is the constraint that decides who wins AI. Constellation owns the only answer that's already built. Every chipmaker needs the same electrons. Might as well own the meter.",
]

body_html = "\n".join(INTRO) + "\n" + STATS_CARD + "\n" + "\n".join(BODY) + "\n" + DISCLOSURE

article = {
    "slug": "ceg-nuclear-power-ai-bottleneck-2026",
    "title": "Nvidia Just Admitted the AI Bottleneck Isn't Chips — It's Electricity",
    "subtitle": "Nvidia is raising chip prices 15% or more and quietly investing in power developers — because the real constraint on AI has moved downstream to electricity. Constellation Energy owns America's largest nuclear fleet, and the hyperscalers are signing 20-year contracts for its output.",
    "summary": "Nvidia's 15%+ price hikes on AI hardware and its new stake in data-center power developer Cloverleaf Infrastructure point to the same conclusion: the AI buildout's bottleneck has moved from chips to electricity. Constellation Energy — owner of America's largest nuclear fleet — sells that round-the-clock, carbon-free power under long-term contracts to Microsoft, Meta, and Walmart, with Three Mile Island's restart pulled forward to 2027. Add the Calpine acquisition that made it the biggest US wholesale power producer, and Constellation looks like the purest pick-and-shovel play on the AI buildout. The stock is down roughly a quarter from its highs, but the contracts are signed and the demand isn't hypothetical.",
    "ticker": "CEG",
    "sector": "ai-power",
    "sentiment": "bullish",
    "date": "2026-08-23T18:00:00Z",
    "price": 272.88,
    "tags": ["Nuclear Energy", "Constellation Energy", "CEG", "AI Power", "Data Centers"],
    "image": {
        "src": "/img/articles/ceg-nuclear-power-ai-bottleneck-2026.jpg",
        "fit": "cover",
        "caption": "A nuclear power plant at dusk beside a modern data center. Photo: The Signal / AI-generated.",
    },
    "links": [
        {
            "label": "Nvidia notifies customers of 15%+ price hikes on AI chips and servers (Reuters, Aug 22–23) →",
            "url": "https://www.reuters.com/technology/",
        },
        {
            "label": "Nvidia's price move and the AI cost crunch, covered at Fortune (Aug 22–23) →",
            "url": "https://fortune.com/tech/",
        },
        {
            "label": "The price hikes hit the enthusiast press (Tom's Hardware, Aug 22–23) →",
            "url": "https://www.tomshardware.com/",
        },
        {
            "label": "Nvidia takes a minority stake in power developer Cloverleaf Infrastructure (WSJ exclusive, Aug 21) →",
            "url": "https://www.wsj.com/tech/",
        },
        {
            "label": "Cloverleaf Infrastructure confirms Nvidia's investment (PR Newswire, Aug 21) →",
            "url": "https://www.prnewswire.com/",
        },
        {
            "label": "Constellation's Crane Clean Energy Center — the Three Mile Island restart behind the Microsoft PPA →",
            "url": "https://www.constellationenergy.com/our-company/locations/crane-clean-energy-center",
        },
        {
            "label": "Constellation newsroom: Walmart PPA, Meta deal, and Q2 2026 results (Aug 6) →",
            "url": "https://www.constellationenergy.com/newsroom",
        },
        {
            "label": "Constellation's fleet and company profile: America's largest carbon-free generator →",
            "url": "https://www.constellationenergy.com/our-company",
        },
    ],
    "meta": {
        "author": "The Signal",
        "estimatedReadTime": "5 minutes",
        "editorialTags": ["nuclear-energy", "constellation-energy", "ceg", "ai-power", "data-centers"],
        "seoKeywords": [
            "Constellation Energy stock",
            "CEG stock",
            "nuclear power AI",
            "AI data center power",
            "Three Mile Island restart",
            "Nvidia power",
        ],
        "relatedTickers": ["VST", "OKLO"],
        "keyMetrics": {
            "CEG Price": "$272.88",
            "Market Cap": "$96.7B",
            "Forward P/E": "20.5",
            "Total Revenue (TTM)": "$31.3B",
            "52-Week Low": "$228.63",
            "52-Week High": "$412.70",
            "Analyst Consensus": "Buy",
            "Analyst Target Mean": "$347.40",
        },
    },
    "bodyHtml": body_html,
}

out_path = "/home/chino/thesignal/articles/posts/ceg-nuclear-power-ai-bottleneck-2026.json"
os.makedirs(os.path.dirname(out_path), exist_ok=True)
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(article, f, indent=2, ensure_ascii=False)
    f.write("\n")

# --- self-check: prose word count (stats card + disclosure excluded) ---
prose = "\n".join(INTRO + BODY)
words = len(prose.split())
print(f"wrote {out_path}")
print(f"prose word count (excl. stats card & disclosure): {words}")
