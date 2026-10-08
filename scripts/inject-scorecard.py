#!/usr/bin/env python3
"""Inject the Signal Scorecard section into the homepage design file from data/scorecard.json.

Why this exists: refresh-scorecard.py has always written data/scorecard.json, but nothing ever
rendered it into the homepage — the section was hand-baked into _backup_dist/index.html and went
stale. This closes the loop so curated panel changes actually reach the page.

Writes into _backup_dist/index.html (the build source), replacing everything between
<section class="scorecard-section" id="scorecard"> and its closing </section>.
Idempotent: running it twice produces identical output.

Usage:
  python3 scripts/inject-scorecard.py            # rewrite the section
  python3 scripts/inject-scorecard.py --check    # report whether it is already in sync
"""
import argparse, json, pathlib, re, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
DATA = ROOT / 'data' / 'scorecard.json'
TARGET = ROOT / '_backup_dist' / 'index.html'
ARC_LEN = 125.66370614359172          # 2*pi*20 for the 40px-radius gauge arc
OUTER, INNER = '<section class="scorecard-section" id="scorecard">', '</section>'

GAUGE = (
    '<div class="sc-gauge-wrap"><svg width="100" height="48" viewBox="0 0 100 48" class="sc-gauge-svg">'
    '<defs><filter id="glow-{t}"><feGaussianBlur stdDeviation="3" result="coloredBlur"/>'
    '<feMerge><feMergeNode in="coloredBlur"/><feMergeNode in="SourceGraphic"/></feMerge></filter>'
    '<filter id="arcglow-{t}"><feGaussianBlur stdDeviation="2" result="blur"/>'
    '<feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge></filter></defs>'
    '<path d="M 10 46 A 40 40 0 0 1 90 46" fill="none" stroke="#1e293b" stroke-width="8" stroke-linecap="round"/>'
    '<path d="M 10 46 A 40 40 0 0 1 90 46" fill="none" stroke="{c}" stroke-width="8" stroke-linecap="round" '
    'stroke-dasharray="{arc}" stroke-dashoffset="{off}" filter="url(#arcglow-{t})"/>'
    '<polygon points="46,44 54,44 50,8" fill="{c}" stroke="rgba(255,255,255,0.3)" stroke-width="0.5" '
    'transform="rotate({rot}, 50, 46)" filter="url(#glow-{t})"/></svg></div>'
)

LOGO = ('<img class="sc-logo" src="data:image/svg+xml,%3Csvg xmlns=\'http://www.w3.org/2000/svg\' '
        'width=\'40\' height=\'40\'%3E%3Ccircle cx=\'20\' cy=\'20\' r=\'20\' fill=\'%23{c}\'/%3E'
        '%3Ctext x=\'20\' y=\'26\' text-anchor=\'middle\' font-family=\'Arial,sans-serif\' '
        'font-size=\'18\' font-weight=\'bold\' fill=\'white\'%3E{initial}%3C/text%3E%3C/svg%3E" '
        'alt="{t}" onerror="this.style.display=\'none\'" crossorigin="anonymous">')


def card(row, idx):
    t = row['ticker']
    c = (row.get('color') or '#64748b').lstrip('#')
    score = int(row.get('score') or 50)
    off = round(ARC_LEN * (1 - score / 100), 14)
    rot = round((score - 50) * 1.8, 14)
    drivers = ''.join(
        f'<div class="sc-driver"><span class="sc-dot" style="background:#{c}"></span>{d}</div>'
        for d in (row.get('drivers') or [])[:3])
    return (
        f'<a href="/stocks/{t}/" class="sc-card" data-sc-idx="{idx}">'
        f'<div class="sc-card-header">{LOGO.format(t=t, c=c, initial=t[0])}'
        f'<div class="sc-card-info"><div class="sc-card-name">{t}</div>'
        f'<div class="sc-card-sub">{row.get("name", t)}</div></div></div>'
        + GAUGE.format(t=t, c='#' + c, arc=ARC_LEN, off=off, rot=rot) +
        f'<div class="sc-signal-label" style="color:#{c}">'
        f'{(row.get("signal") or "Neutral").upper()} SIGNAL {score}</div>'
        f'<div class="sc-drivers">{drivers}</div></a>'
    )


def table(rows):
    def cell(v):
        v = '-' if v in (None, '', 'N/A') else str(v)
        cls = ' class="positive"' if v.startswith('+') else ''
        return f'<td{cls}>{v}</td>'

    def row_of(label, key):
        cells = []
        for r in rows:
            m = r.get('metrics') or {}
            v = r.get('upside') if key == 'upside' else m.get(key)
            cells.append(cell(v))
        return f'<tr><td class="metric-label">{label}</td>{"".join(cells)}</tr>'

    head = ''.join(f'<th>{r["ticker"]}</th>' for r in rows)
    body = (row_of('Revenue (TTM)', 'revenue') + row_of('Rev Growth (YoY)', 'growth')
            + row_of('Net Income', 'netIncome') + row_of('P/E Ratio', 'pe')
            + row_of('Price/Sales', 'ps') + row_of('Target Upside', 'upside'))
    icon = ('<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
            'stroke-width="2" style="vertical-align:middle;margin-right:6px">'
            '<rect x="3" y="12" width="4" height="8"/><rect x="10" y="6" width="4" height="14"/>'
            '<rect x="17" y="2" width="4" height="18"/></svg>')
    return ('<div class="sc-table-container"><div class="sc-table-header"><h3>' + icon +
            'Key Metrics (TTM)</h3></div><div class="sc-table-scroll"><table class="sc-table">'
            f'<thead><tr><th>Metric</th>{head}</tr></thead><tbody>{body}</tbody></table>'
            '</div></div>')


def build_section(rows):
    cards = ''.join(card(r, i) for i, r in enumerate(rows))
    return (OUTER + '<div class="scorecard-inner"><div class="scorecard-header-top">'
            '<img class="sc-header-logo" src="/img/logo-hex.jpg" alt="The Signal">'
            '<h2 class="scorecard-title">Signal <span>Scorecard</span></h2></div>'
            '<p class="scorecard-subtitle">High-signal intelligence, researched with AI and '
            'reviewed by humans</p>'
            f'<div class="scorecard-grid" id="scorecardGrid">{cards}</div>'
            + table(rows) + '</div></section>')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--check', action='store_true')
    a = ap.parse_args()

    rows = json.loads(DATA.read_text())
    html = TARGET.read_text()
    start = html.find(OUTER)
    if start == -1:
        sys.exit('FAIL: scorecard section anchor not found in _backup_dist/index.html')
    end = html.find(INNER, start)
    if end == -1:
        sys.exit('FAIL: no closing </section> after the scorecard section')
    end += len(INNER)
    new_section = build_section(rows)
    current = html[start:end]
    in_sync = current == new_section

    if a.check:
        print('in sync' if in_sync else 'OUT OF SYNC — run without --check to rewrite')
        return
    if in_sync:
        print('scorecard section already in sync — nothing to do')
        return

    TARGET.with_suffix('.html.sc-backup').write_text(html)
    TARGET.write_text(html[:start] + new_section + html[end:])
    print(f'injected {len(rows)} cards: {", ".join(r["ticker"] for r in rows)}')
    print(f'  section {len(current)} -> {len(new_section)} bytes; backup at {TARGET.name}.sc-backup')


if __name__ == '__main__':
    main()
