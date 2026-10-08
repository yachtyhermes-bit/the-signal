#!/usr/bin/env python3
"""Assemble articles/posts/tsm-record-quarter-ai-foundry-bottleneck-2026.json
from the Gemini writer draft (/tmp/draft-tsm-record-quarter-ai-foundry-bottleneck-2026.md).

Prose is verbatim from the draft. Integrity fixes only:
  1. literal "##" section markup -> real <h2> (long-form precedent: ETF Review / Focus List / RKLB 10/08)
  2. "NT$3.13 trillion in cash and short-term reserves" -> "in cash": the NT$3.13T verified figure is the
     cash-and-cash-equivalents line, not the wider cash+ST investments line. State the basis we verified.
  3. Dropped the Ray Dalio sentence: a named attribution with no linkable source (the claims-discipline
     rule that got an article quarantined). The BofA/Subramanian point is linked and carries the same idea.
Stats card, links, tags and metadata are ours.
"""
import json, pathlib, re, sys
from datetime import datetime, timezone

ROOT = pathlib.Path('/home/chino/thesignal')
SLUG = 'tsm-record-quarter-ai-foundry-bottleneck-2026'
DRAFT = pathlib.Path('/tmp/draft-tsm-record-quarter-ai-foundry-bottleneck-2026.md')

FIXES = [
    ('held NT$3.13 trillion in cash and short-term reserves against total debt of NT$1.06 trillion.',
     'held NT$3.13 trillion in cash against total debt of NT$1.06 trillion.'),
    (" Ray Dalio echoed similar cautions recently, noting that the market\u2019s cushion against high interest rates is evaporating.", ""),
    # prose-lint FAIL: paragraph of 7 sentences (> 6). Wording untouched, broken at the natural turn.
    ("data-center accelerators. But none of those companies", "data-center accelerators.\n\nBut none of those companies"),
]

STATS_CARD = (
    '<div class="stats-card"><div class="stats-card-title">The Numbers That Matter</div>'
    '<table class="stats-table">'
    '<tr><td class="stat-label">Price <span class="stats-live-badge">LIVE</span></td>'
    '<td class="stat-value" data-live-ticker="TSM" data-live-field="price">$472.20</td></tr>'
    '<tr><td class="stat-label">Market Cap</td><td class="stat-value">$2.45T</td></tr>'
    '<tr><td class="stat-label">Forward P/E</td><td class="stat-value">21.5x</td></tr>'
    '<tr><td class="stat-label">Total Revenue (TTM)</td><td class="stat-value">$139.6B</td></tr>'
    '<tr><td class="stat-label">Gross Margin</td><td class="stat-value">64.2%</td></tr>'
    '<tr><td class="stat-label">52-Week Low</td><td class="stat-value">$266.82</td></tr>'
    '<tr><td class="stat-label">52-Week High</td><td class="stat-value">$487.47</td></tr>'
    '<tr><td class="stat-label">Analyst Consensus</td><td class="stat-value">Strong Buy (20 analysts)</td></tr>'
    '<tr><td class="stat-label">Analyst Target Mean</td><td class="stat-value">$555.01</td></tr>'
    '</table><div class="stats-card-note">Price refreshes live \u00b7 All other figures as of October 8, 2026</div></div>'
)

DISCLOSURE = '<p class="disclosure">Disclosure: The Signal holds no position in TSM. Positions may change. This is not financial advice.</p>'

LINKS = [
    {"label": "Reuters via The Business Times: TSMC's Q3 revenue surges to record NT$1.49 trillion (US$46.71B), up 50%, beating the LSEG SmartEstimate of NT$1.46 trillion",
     "url": "https://www.businesstimes.com.sg/companies-markets/tsmcs-q3-revenue-surges-record-beating-market-forecast"},
    {"label": "TrendForce: TSMC's Q3 revenue beats forecasts at a record NT$1.49 trillion \u2014 net profit seen surging 64%",
     "url": "https://www.trendforce.com/news/2026/10/08/news-tsmc-q3-revenue-beats-forecasts-at-record-nt1-49-trillion-net-profit-seen-surging-64/"},
    {"label": "Yahoo Finance: TSMC's Q3 revenue tops its own guidance \u2014 September revenue NT$511.86 billion, nine-month revenue up 41.1% to NT$3.90 trillion",
     "url": "https://finance.yahoo.com/markets/stocks/articles/tsmc-q3-revenue-tops-own-113733291.html"},
    {"label": "TechPowerUp: TSMC to scale 2nm production to 120,000 wafers per month by the end of 2026",
     "url": "https://www.techpowerup.com/353153/tsmc-to-scale-2-nm-production-to-120-000-wafers-per-month-by-the-end-of-2026"},
    {"label": "Tom's Hardware: TSMC reportedly hiking prices across all advanced nodes, which account for about 74% of its wafer business",
     "url": "https://www.tomshardware.com/tech-industry/semiconductors/tsmc-is-reportedly-hiking-prices-for-all-advanced-nodes-accounting-for-74-percent-of-the-companys-wafer-business-nvidia-amd-apple-qualcomm-and-others-will-face-higher-wafer-costs"},
    {"label": "TrendForce citing Nikkei Asia: TSMC reported to plan price increases of up to 10% in 2027, with an extra premium on high-performance computing wafers",
     "url": "https://www.trendforce.com/news/2026/07/22/news-tsmc-reportedly-plans-up-to-10-price-hikes-in-2027-with-extra-hpc-premiums-apple-nvidia-in-focus"},
    {"label": "TrendForce: Samsung guides 3Q26 operating profit up 783% to a record KRW 107.4 trillion on HBM4 and memory price gains \u2014 the memory-cost shock landing on TSMC's customers",
     "url": "https://www.trendforce.com/news/2026/10/08/news-samsung-sees-3q26-operating-profit-soaring-783-to-record-krw-107-4-trillion-on-hbm4-memory-price-gains/"},
    {"label": "MarketWatch: Bank of America's Savita Subramanian on hyperscaler borrowing and the risk of an AI-stock 'air pocket' in 2026",
     "url": "https://www.marketwatch.com/story/stocks-to-buy-for-2026-as-the-ai-trade-comes-under-pressure-23517d17"},
]

KEY_METRICS = {
    "Price": "$472.20",
    "Market Cap": "$2.45T",
    "Forward P/E": "21.5x",
    "Total Revenue (TTM)": "$139.6B",
    "Gross Margin": "64.2%",
    "52-Week Low": "$266.82",
    "52-Week High": "$487.47",
    "Analyst Consensus": "Strong Buy (20 analysts)",
    "Analyst Target Mean": "$555.01",
}


def main():
    raw = DRAFT.read_text()
    header, _, body_md = raw.partition('---BODY---')
    meta = {}
    for line in header.splitlines():
        if line.startswith(('TITLE:', 'SUBTITLE:', 'SUMMARY:')):
            k, _, v = line.partition(':')
            meta[k] = v.strip()

    fixed = body_md.strip()
    changes = []
    for old, new in FIXES:
        if old in fixed:
            fixed = fixed.replace(old, new)
            changes.append(old[:70])
        else:
            print('WARNING: fix target not found -> ' + old[:70])

    out, paras = [], []
    for block in re.split(r'\n\s*\n', fixed):
        block = block.strip()
        if not block:
            continue
        if block.startswith('## '):
            if paras:
                out.extend(f'<p>{p}</p>' for p in paras)
                paras = []
            out.append(f'<h2>{block[3:].strip()}</h2>')
        else:
            paras.append(block)
    if paras:
        out.extend(f'<p>{p}</p>' for p in paras)

    pcount = 0
    with_card = []
    for block in out:
        with_card.append(block)
        if block.startswith('<p>'):
            pcount += 1
            if pcount == 3:
                with_card.append(STATS_CARD)
    with_card.append(DISCLOSURE)
    body_html = ''.join(with_card)

    if chr(92) + '"' in body_html:
        sys.exit('ABORT: literal backslash-quote in bodyHtml (pitfall 50)')

    words = len(re.sub(r'<[^>]+>', ' ', body_html).split())
    if words < 1200:
        print(f'ABORT: body is only {words} words')
        sys.exit(1)

    art = {
        "slug": SLUG,
        "title": meta['TITLE'],
        "subtitle": meta['SUBTITLE'],
        "summary": meta['SUMMARY'],
        "ticker": "TSM",
        "tickerName": "Taiwan Semiconductor Manufacturing Company Limited",
        "company": "Taiwan Semiconductor Manufacturing Company Limited",
        "sector": "ai",
        "sentiment": "bullish",
        "date": datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'),
        "price": 472.20,
        "featured": False,
        "premium": False,
        "image": {
            "src": f"/img/articles/{SLUG}.jpg",
            "fit": "cover",
            "caption": "An extreme-ultraviolet lithography tool inside a semiconductor cleanroom \u2014 the machine that gates every advanced node TSMC sells.",
        },
        "tags": ["TSM", "TSMC", "Taiwan Semiconductor", "foundry", "N2", "2nm", "AI-chips",
                 "pricing-power", "capacity", "geopolitics"],
        "links": LINKS,
        "meta": {
            "author": "The Signal",
            "estimatedReadTime": f"{max(1, round(words / 220))} minutes",
            "editorialTags": ["tsm", "tsmc", "taiwan-semiconductor", "foundry", "n2", "2nm",
                              "ai-chips", "pricing-power", "capacity", "geopolitics"],
            "seoKeywords": ["TSMC stock", "TSM", "TSMC Q3 2026 revenue", "TSMC 2nm N2 ramp",
                            "foundry capacity", "AI chip bottleneck", "TSMC pricing"],
            "relatedTickers": ["NVDA", "AVGO", "AMAT"],
            "sourceLinks": [l["url"] for l in LINKS],
            "keyMetrics": KEY_METRICS,
        },
        "bodyHtml": body_html,
    }

    dest = ROOT / 'articles' / 'posts' / f'{SLUG}.json'
    dest.write_text(json.dumps(art, indent=2, ensure_ascii=False) + chr(10))
    print(f'wrote {dest}')
    print(f'  title: {art["title"]}')
    print(f'  date:  {art["date"]}')
    print(f'  body:  {words} words, read time {art["meta"]["estimatedReadTime"]}')
    print(f'  h2 sections: {body_html.count("<h2>")}, paragraphs: {body_html.count("<p>")}')
    print(f'  links: {len(art["links"])}')
    print('  integrity fixes applied:')
    for c in changes:
        print(f'    - {c}')


if __name__ == '__main__':
    main()
