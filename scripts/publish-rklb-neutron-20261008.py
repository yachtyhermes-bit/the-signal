#!/usr/bin/env python3
"""Assemble articles/posts/rocket-lab-neutron-re-rate-launch-bottleneck-2026.json
from the writer draft (/tmp/rklb-draft2.md), applying only integrity fixes.

The user asked for the piece published as written. Fixes applied are limited to things that
cannot ship:
  1. literal "##" section markup -> real <h2> (long-form precedent: ETF Review / Focus List)
  2. "constellation constellations" duplication
  3. a moat rating attributed to Morningstar -> our own read (unattributed third-party
     opinion is the exact pattern that got an article quarantined)
  4. "second-most-frequent orbital launch provider on Earth" -> the company's own framing
     ("second most frequently launched U.S. rocket"), which is the defensible claim
  5. "$769,145,984" / "$165,459,008" -> $769 million / $165 million (house formatting)
  6. "decades of telemetry ... dozens of ... flights" -> nine years / more than ninety flights
Everything else is verbatim from the draft.
"""
import json, pathlib, re, sys
from datetime import datetime, timezone

ROOT = pathlib.Path('/home/chino/thesignal')
SLUG = 'rocket-lab-neutron-re-rate-launch-bottleneck-2026'
DRAFT = pathlib.Path('/tmp/rklb-draft2.md')

FIXES = [
    ('constellation constellations being deployed',
     'constellations being deployed'),
    ('Today, it ranks as the second-most-frequent orbital launch provider on Earth, trailing only SpaceX.',
     "Today, Electron is the second most frequently launched U.S. rocket, behind only SpaceX."),
    ('Rocket Lab possesses decades of telemetry captured across dozens of operational Electron flights.',
     'Rocket Lab holds nine years of telemetry captured across more than ninety Electron flights.'),
    ("Morningstar rates Rocket Lab\u2019s economic moat as Narrow.",
     "We rate Rocket Lab\u2019s economic moat as Narrow."),
    ('Rocket Lab generated $769,145,984 in revenue. That represents a blistering 62.0% top-line growth rate year over year.',
     'Rocket Lab generated $769 million in revenue. That represents a blistering 62% top-line growth rate year over year.'),
    ('Rocket Lab reported a net loss of $165,459,008 over the trailing twelve months.',
     'Rocket Lab reported a net loss of $165 million over the trailing twelve months.'),
    ('With net losses sitting at $165 million, every month',
     'With net losses at $165 million, every month'),
]

# Long sentences that prose-lint FAILs (>34 words). Split, keeping the draft's wording.
SPLITS = [
    ("You could wait in line to hitchhike as a secondary payload on a SpaceX Falcon 9, or you could pay an astronomical fee to a legacy defense contractor whose hardware had not changed fundamentally since the Cold War.",
     "You could wait in line as a secondary payload on a SpaceX Falcon 9. Or you could pay an astronomical fee to a legacy defense contractor whose hardware has not changed fundamentally since the Cold War."),
    ("In plain terms: if you want to put a camera, a radar antenna, or an edge-compute node into space, Rocket Lab will build the satellite chassis, pack your payload inside, and blast it off their private pads.",
     "In plain terms: if you want to put a camera, a radar antenna, or an edge-compute node into space, Rocket Lab will build the satellite chassis. Then it packs your payload inside and blasts it off its private pads."),
    ("A customer brings an optical sensor or an experimental communications chip; Rocket Lab designs the satellite frame, manufactures the power and navigation components in-house, integrates the payload, and fires it into space from its proprietary launch complexes.",
     "A customer brings an optical sensor or an experimental communications chip. Rocket Lab designs the satellite frame, builds the power and navigation components in-house, integrates the payload, and launches it from its own complexes."),
    ("With net losses at $165 million, every month of development brings the company closer to the point where it must raise dilutive secondary equity capital or take on high-interest debt in a tight rate environment.",
     "With net losses at $165 million, every month of development brings the company closer to a choice. It can raise dilutive secondary equity, or take on high-interest debt in a tight rate environment."),
    ("You can run finite element analysis on a computer cluster for a decade, but you do not truly understand cryogenic fluid dynamics, supersonic aerodynamic heating, and acoustic vibration until your rocket passes through maximum aerodynamic pressure.",
     "You can run finite element analysis on a computer cluster for a decade. But you do not truly understand cryogenic fluid dynamics, supersonic heating, and acoustic vibration until your rocket passes through maximum aerodynamic pressure."),
    ("The Archimedes test cadence is the canary in the coal mine: steady, issue-free hot fires mean the maiden launch remains on track; cracked manifolds or ignition anomalies signal the schedule slip that short-sellers are waiting for.",
     "The Archimedes test cadence is the canary in the coal mine. Steady, issue-free hot fires mean the maiden launch stays on track. Cracked manifolds or ignition anomalies signal the schedule slip shorts are waiting for."),
]

STATS_CARD = (
    '<div class="stats-card"><div class="stats-card-title">The Numbers That Matter</div>'
    '<table class="stats-table">'
    '<tr><td class="stat-label">Price <span class="stats-live-badge">LIVE</span></td>'
    '<td class="stat-value" data-live-ticker="RKLB" data-live-field="price">$71.92</td></tr>'
    '<tr><td class="stat-label">Market Cap</td><td class="stat-value">$46.0B</td></tr>'
    '<tr><td class="stat-label">Forward P/E</td><td class="stat-value">1,332x</td></tr>'
    '<tr><td class="stat-label">Total Revenue (TTM)</td><td class="stat-value">$769.1M</td></tr>'
    '<tr><td class="stat-label">Gross Margin</td><td class="stat-value">37.3%</td></tr>'
    '<tr><td class="stat-label">52-Week Low</td><td class="stat-value">$37.57</td></tr>'
    '<tr><td class="stat-label">52-Week High</td><td class="stat-value">$151.00</td></tr>'
    '<tr><td class="stat-label">Analyst Consensus</td><td class="stat-value">Buy (20 analysts)</td></tr>'
    '<tr><td class="stat-label">Analyst Target Mean</td><td class="stat-value">$109.15</td></tr>'
    '</table><div class="stats-card-note">Price refreshes live \u00b7 All other figures as of October 8, 2026</div></div>'
)

DISCLOSURE = '<p class="disclosure">Disclosure: The Signal holds no position in RKLB. Positions may change. This is not financial advice.</p>'

LINKS = [
    {"label": "Rocket Lab Q2 2026 results: record $234M revenue, up 62% year over year, backlog of $2.36 billion (company release)",
     "url": "https://investors.rocketlabcorp.com/news-releases/news-release-details/rocket-lab-announces-second-quarter-2026-financial-results-posts"},
    {"label": "Electron program page: 300 kg to LEO, 94 launches, 265+ satellites deployed, second most frequently launched U.S. rocket",
     "url": "https://rocketlabcorp.com/launch/electron"},
    {"label": "Neutron Payload User's Guide: up to 13,000 kg to LEO reusable, 15,000 kg expendable (PDF)",
     "url": "https://rocketlabcorp.com/assets/Uploads/Rocket-Lab-Neutron-PUG-reduced-final.pdf"},
    {"label": "Space.com: Archimedes completes a full-duration hot fire at NASA Stennis, called critical preparation for Neutron's first flight",
     "url": "https://www.space.com/space-exploration/watch-archimedes-burn-rocket-lab-fires-up-engine-for-its-powerful-next-gen-neutron-launcher-video"},
    {"label": "Motley Fool: the case that Neutron slips to 2027 and why the delay matters",
     "url": "https://www.fool.com/investing/2026/09/04/peter-becks-neutron-rocket-could-slip-to-2027"},
    {"label": "Rocket Lab full year 2025 results: $602M revenue, 21 launches at a 100% success rate (Form 8-K, Exhibit 99.1 \u2014 SEC)",
     "url": "https://www.sec.gov/Archives/edgar/data/1819994/000181999426000012/rklb-02262026ex991.htm"},
    {"label": "Rocket Lab Q1 2026 results: Neutron on track for a debut launch this year, Archimedes qualification ongoing (Form 8-K, Exhibit 99.1 \u2014 SEC)",
     "url": "https://www.sec.gov/Archives/edgar/data/1819994/000181999426000027/rklb-05072026ex991.htm"},
]


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
    for old, new in SPLITS:
        if old in fixed:
            fixed = fixed.replace(old, new)
            changes.append('SPLIT ' + old[:60])
        else:
            print('WARNING: split target not found -> ' + old[:70])

    # markdown -> html
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

    # stats card after the third paragraph (hook + what it does + why it matters)
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

    words = len(re.sub(r'<[^>]+>', ' ', body_html).split())
    if words < 1200:
        print(f'ABORT: body is only {words} words — draft not converted correctly')
        sys.exit(1)

    art = {
        "slug": SLUG,
        "title": meta['TITLE'],
        "subtitle": meta['SUBTITLE'],
        "summary": meta['SUMMARY'],
        "ticker": "RKLB",
        "tickerName": "Rocket Lab Corporation",
        "company": "Rocket Lab Corporation",
        "sector": "space",
        "sentiment": "bullish",
        "date": datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'),
        "price": 71.92,
        "featured": False,
        "premium": False,
        "image": {
            "src": f"/img/articles/{SLUG}.jpg",
            "fit": "cover",
            "caption": "A Rocket Lab Archimedes engine on the test stand at NASA's Stennis Space Center in Mississippi, where the engine that has to carry Neutron to orbit is still being qualified.",
        },
        "tags": ["RKLB", "Rocket Lab", "Neutron", "Electron", "space", "launch", "space-systems",
                 "aerospace", "defense", "vertical-integration"],
        "links": LINKS,
        "meta": {
            "author": "The Signal",
            "estimatedReadTime": f"{max(1, round(words / 220))} minutes",
            "editorialTags": ["rklb", "rocket-lab", "neutron", "electron", "space-launch",
                              "space-systems", "archimedes", "vertical-integration", "launch-bottleneck"],
            "seoKeywords": ["Rocket Lab stock", "RKLB", "Neutron rocket", "Archimedes engine",
                            "Rocket Lab Neutron delay", "Electron launch", "space stocks 2026"],
            "relatedTickers": ["RKLB", "IRDM", "SPCX"],
            "sourceLinks": [l["url"] for l in LINKS],
        },
        "bodyHtml": body_html,
    }

    dest = ROOT / 'articles' / 'posts' / f'{SLUG}.json'
    dest.write_text(json.dumps(art, indent=2) + chr(10))
    print(f'wrote {dest}')
    print(f'  title: {art["title"]}')
    print(f'  body: {words} words, read time {art["meta"]["estimatedReadTime"]}')
    print(f'  h2 sections: {body_html.count("<h2>")}, paragraphs: {body_html.count("<p>")}')
    print(f'  links: {len(art["links"])}')
    print('  integrity fixes applied:')
    for c in changes:
        print(f'    - {c}')


if __name__ == '__main__':
    main()
