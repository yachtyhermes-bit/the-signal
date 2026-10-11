#!/usr/bin/env python3
"""Assemble articles/posts/ionq-quantum-interconnect-defense-2026.json from the writer draft.

The prose is the Gemini 3.8 Flash draft, used as written except for two integrity fixes
(accuracy vs the cited sources), matching the precedent of the RKLB publish script:

  1. "success probabilities decay exponentially" -> "quadratically". The cited technical write-up
     (Quantum Computing Report) states the two-photon heralding scheme scales as p^2, i.e.
     quadratically. "Exponentially" overstates the mechanism.
  2. The Bhaskar attribution came back garbled ("need not bottle distributed systems"), which
     misstates the sourced meaning: "a photonic quantum interconnect need not be a bottleneck for
     distributed quantum computing." Re-stated cleanly, no quotation marks.

Everything else is verbatim. The stats card is inserted after the third paragraph (house
convention), and the values are mirrored into meta.keyMetrics per the article schema.
"""
import json, pathlib, re, sys
from datetime import datetime, timezone

ROOT = pathlib.Path('/home/chino/thesignal')
SLUG = 'ionq-quantum-interconnect-defense-2026'
DRAFT = pathlib.Path(f'/tmp/draft-{SLUG}.md')
PRICE = 39.89  # 2026-10-09 close = last completed session before the 2026-10-11 publish date

FIXES = [
    ('which makes success probabilities decay exponentially',
     'which makes success probabilities decay quadratically'),
    ('the technology proves photonic links need not bottle distributed systems',
     'the result shows a photonic quantum interconnect does not have to be a bottleneck for distributed quantum computing'),
]

STATS_CARD = (
    '<div class="stats-card"><div class="stats-card-title">The Numbers That Matter</div>'
    '<table class="stats-table">'
    '<tr><td class="stat-label">Price <span class="stats-live-badge">LIVE</span></td>'
    '<td class="stat-value" data-live-ticker="IONQ" data-live-field="price">$39.89</td></tr>'
    '<tr><td class="stat-label">Market Cap</td><td class="stat-value">$16.16B</td></tr>'
    '<tr><td class="stat-label">Forward P/E</td><td class="stat-value">-30.9</td></tr>'
    '<tr><td class="stat-label">Total Revenue (TTM)</td><td class="stat-value">$246.5M</td></tr>'
    '<tr><td class="stat-label">52-Week Low</td><td class="stat-value">$25.89</td></tr>'
    '<tr><td class="stat-label">52-Week High</td><td class="stat-value">$84.64</td></tr>'
    '<tr><td class="stat-label">Analyst Consensus</td><td class="stat-value">Strong Buy (14 analysts)</td></tr>'
    '<tr><td class="stat-label">Analyst Target Mean</td><td class="stat-value">$66.63</td></tr>'
    '</table><div class="stats-card-note">Price refreshes live \u00b7 All other figures as of October 11, 2026</div></div>'
)

KEY_METRICS = {
    "Price": 39.89,
    "Market Cap": "$16.16B",
    "Forward P/E": "-30.9",
    "Total Revenue (TTM)": "$246.5M",
    "52-Week Low": 25.89,
    "52-Week High": 84.64,
    "Analyst Consensus": "Strong Buy (14 analysts)",
    "Analyst Target Mean": 66.63,
}

LINKS = [
    {"label": "DARPA: Four More Teams Enter the Quantum Benchmarking Initiative's Final Stage, Oct. 7, 2026 \u2192",
     "url": "https://www.darpa.mil/news/2026/four-more-teams-enter-quantum-benchmarking-initiative-final-stage"},
    {"label": "IonQ: Advances to the Final Stage of DARPA's Quantum Benchmarking Initiative \u2014 Stage C agreement with a potential value of up to $300 million, Oct. 7, 2026 \u2192",
     "url": "https://www.ionq.com/news/ionq-advances-to-final-stage-of-darpas-quantum-benchmarking-initiative"},
    {"label": "IonQ: World-First Quantum Memory-Enhanced Interconnect for Distributed Quantum Applications \u2014 more than 1,000 entanglement events per second, Oct. 9, 2026 \u2192",
     "url": "https://www.ionq.com/news/ionq-demonstrates-world-first-quantum-memory-enhanced-interconnect-for-distributed-quantum-applications"},
    {"label": "Quantum Computing Report: DARPA Selects Atom Computing, Diraq, IBM and IonQ for Final Stage C Verification \u2192",
     "url": "https://quantumcomputingreport.com/darpa-selects-atom-computing-diraq-ibm-and-ionq-for-final-stage-c-verification-under-quantum-benchmarking-initiative"},
    {"label": "Quantum Computing Report: IonQ's 1.032 kHz Interconnect Between Trapped Ions and Diamond Colour Centres \u2014 87.9% state fidelity, 969 \u00b5s mean time to success \u2192",
     "url": "https://quantumcomputingreport.com/ionq-demonstrates-1-khz-memory-enhanced-quantum-interconnect-connecting-trapped-ions-and-diamond-color-centers/amp"},
    {"label": "Military & Aerospace Electronics: Department of War announces $350 million in quantum computing initiatives, Oct. 9, 2026 \u2192",
     "url": "https://www.militaryaerospace.com/computers/article/55410692/dod-announces-350-million-in-quantum-computing-initiatives"},
    {"label": "Evertiq: Department of War announces $350M in quantum computing initiatives, Oct. 9, 2026 \u2192",
     "url": "https://evertiq.com/news/2026-10-09-department-of-war-announces-350m-in-quantum-computing-initiatives"},
]

IMAGE = {
    "src": f"/img/articles/{SLUG}.jpg",
    "fit": "cover",
    "caption": "An optical bench inside a quantum photonics laboratory, where light carried through fibre links separate quantum devices. IonQ's October interconnect result entangled a trapped barium ion with a diamond-based quantum memory over a photonic link. Photo: The Signal / AI-generated.",
    "alt": "Photo-realistic photograph of a photonics laboratory optical bench with mirrors, lenses and a fibre patch cable running into a small mounted chip clamped in a brass holder, with a vacuum chamber blurred in the background.",
}


def main():
    dest = ROOT / 'articles' / 'posts' / f'{SLUG}.json'
    if dest.exists():
        sys.exit(f'ABORT: {dest} already exists — slug collision guard')

    raw = DRAFT.read_text()
    header, _, body_md = raw.partition('---BODY---')
    meta = {}
    for line in header.splitlines():
        if line.startswith(('TITLE:', 'SUBTITLE:', 'SUMMARY:')):
            k, _, v = line.partition(':')
            meta[k] = v.strip()
    for k in ('TITLE', 'SUBTITLE', 'SUMMARY'):
        if not meta.get(k):
            sys.exit(f'ABORT: draft missing {k}')

    fixed = body_md.strip()
    changes = []
    for old, new in FIXES:
        if old in fixed:
            fixed = fixed.replace(old, new)
            changes.append('FIX: ' + old[:60])
        else:
            print(f'WARNING: fix target not found -> {old[:70]}')

    # markdown -> html (no headings expected; handled in case the writer emits any)
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
            paras.append(re.sub(r'\s+', ' ', block))
    if paras:
        out.extend(f'<p>{p}</p>' for p in paras)

    # disclosure must render as <p class="disclosure">
    disc_idx = [i for i, b in enumerate(out) if b.startswith('<p>') and 'Disclosure: The Signal holds no position in IONQ' in b]
    if not disc_idx:
        sys.exit('ABORT: no disclosure paragraph in draft')
    i = disc_idx[-1]
    out[i] = ('<p class="disclosure">' + out[i][3:-4].strip() + '</p>')

    # stats card after the third paragraph (house convention)
    # exact-price guard runs on the PROSE only (the stats card legitimately carries the price row)
    prose_html = ''.join(out)
    old_price_hits = len(re.findall(r'\$\d{1,4}\.\d{2}', prose_html))
    if old_price_hits:
        sys.exit(f'ABORT: {old_price_hits} exact dollar-price pattern(s) in prose')

    with_card, pcount = [], 0
    for block in out:
        with_card.append(block)
        if block.startswith('<p>'):
            pcount += 1
            if pcount == 3:
                with_card.append(STATS_CARD)
    body_html = ''.join(with_card)

    if chr(92) + chr(34) in body_html:
        sys.exit('ABORT: literal backslash-quote in body (pitfall 50 escaping corruption)')

    words = len(re.sub(r'<[^>]+>', ' ', body_html).split())

    art = {
        "slug": SLUG,
        "title": meta['TITLE'],
        "subtitle": meta['SUBTITLE'],
        "summary": meta['SUMMARY'],
        "ticker": "IONQ",
        "tickerName": "IonQ",
        "company": "IonQ, Inc.",
        "sector": "quantum",
        "sentiment": "neutral",
        "date": "2026-10-11T14:00:00Z",
        "price": PRICE,
        "featured": True,
        "premium": False,
        "image": IMAGE,
        "tags": ["IONQ", "IonQ", "quantum-computing", "trapped-ion", "quantum-networking",
                 "DARPA", "quantum-benchmarking-initiative", "skywater", "photonics", "defense-technology"],
        "links": LINKS,
        "meta": {
            "author": "The Signal Editorial",
            "estimatedReadTime": f"{max(1, round(words / 220))} min",
            "editorialTags": ["ionq", "quantum-computing", "trapped-ion", "quantum-interconnect",
                              "darpa-qbi", "skywater", "photonic-interconnect", "defense-tech"],
            "seoKeywords": ["IonQ stock", "IONQ stock", "DARPA quantum benchmarking initiative",
                            "quantum interconnect 1 kHz", "IonQ trapped ion quantum computer",
                            "SkyWater acquisition", "quantum computing defense funding",
                            "PsiQuantum loan", "quantum networking"],
            "relatedTickers": ["IONQ", "QBTS", "RGTI"],
            "keyMetrics": KEY_METRICS,
            "sourceLinks": [l["url"] for l in LINKS],
        },
        "bodyHtml": body_html,
    }

    dest.write_text(json.dumps(art, indent=2) + '\n')
    print(f'wrote {dest}')
    print(f'  title: {art["title"]}')
    print(f'  subtitle: {art["subtitle"]}')
    print(f'  body: {words} words, read time {art["meta"]["estimatedReadTime"]}')
    disc_tag = 'class="disclosure"'
    print(f'  h2 sections: {body_html.count("<h2>")}, paragraphs: {body_html.count("<p>")}')
    print(f'  stats card present: {"stats-card" in body_html}, disclosure: {disc_tag in body_html}')
    print(f'  links: {len(art["links"])}')
    print(f'  date: {art["date"]}  price: {art["price"]}  featured: {art["featured"]} sector: {art["sector"]}')
    for c in changes:
        print('  ' + c)


if __name__ == '__main__':
    main()
