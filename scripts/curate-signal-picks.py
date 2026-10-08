#!/usr/bin/env python3
"""Bi-weekly curator for the Signal Scorecard + Signal Highlights panels.

Scores the curated moat universe against the selection profile (data/signal-picks-profile.json)
using cached fundamentals (data/financials.json) and curated moat ratings (data/moat-*.json),
then proposes the next 16 names.

Selection is INCUMBENT-ANCHORED but a rolling rotation:
  1. forced removals first — names excluded by policy, or incumbents that fell below the score floor
  2. discretionary rotation — up to `target_swaps` per cycle, weakest incumbents out, strongest
     eligible challengers in, so long as the challenger outscores by at least `min_uplift`
  3. top up to panel size, respecting cluster targets

Incumbents missing cached data are KEPT and flagged unscored — never dropped for missing data,
which would read as a deliberate rotation. "No change" is still valid when nothing clears the bar.

Default is a dry run writing data/signal-picks-proposal.json plus a digest for review. Nothing on
the homepage changes until --apply is used AND the panels are rebuilt.
"""
import argparse, datetime, glob, json, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
DATA = ROOT / 'data'
PROFILE = json.loads((DATA / 'signal-picks-profile.json').read_text())
FIN = json.loads((DATA / 'financials.json').read_text())
CHURN = PROFILE['churn_rule']
EXCLUDED = {e['ticker'].upper(): e.get('reason', 'excluded by policy') for e in PROFILE.get('exclusions', [])}
MOAT_POINTS = {'wide': 25, 'narrow': 16, 'none': 6}
NULL_SCORE = -1.0


def raw(node, *path):
    """Numeric value at path, unwrapping the {'raw':…,'fmt':…} shape."""
    cur = node
    for p in path:
        if not isinstance(cur, dict):
            return None
        cur = cur.get(p)
    if isinstance(cur, dict):
        v = cur.get('raw')
        return v if isinstance(v, (int, float)) else None
    return cur if isinstance(cur, (int, float)) else None


def text(node, *path):
    cur = node
    for p in path:
        if not isinstance(cur, dict):
            return None
        cur = cur.get(p)
    if isinstance(cur, dict):
        v = cur.get('fmt') or cur.get('raw')
        return str(v) if v is not None else None
    return cur if isinstance(cur, str) else None


MOATS = {}
for _f in glob.glob(str(DATA / 'moat-*.json')):
    _m = json.loads(pathlib.Path(_f).read_text())
    if _m.get('symbol'):
        MOATS[_m['symbol'].upper()] = _m

CLUSTER_OF, CLUSTER_BY_NAME = {}, {}
for c in PROFILE['clusters']:
    CLUSTER_BY_NAME[c['name']] = c
    for t in c['tickers']:
        CLUSTER_OF.setdefault(t.upper(), c['name'])


def read_tickers(name, fallback):
    for cand, key in ((name, None), (fallback, 'ticker')):
        p = DATA / cand
        if not p.exists():
            continue
        try:
            v = json.loads(p.read_text())
        except Exception:
            continue
        if isinstance(v, list) and v:
            if key is None and isinstance(v[0], str):
                return [x.upper() for x in v]
            if key and isinstance(v[0], dict):
                return [x[key].upper() for x in v if x.get(key)]
    return []


CURRENT = {
    'scorecard': read_tickers('scorecard-tickers.json', 'scorecard.json'),
    'highlights': read_tickers('signal-highlights-tickers.json', 'signal-highlights.json'),
}
INCUMBENTS = set(CURRENT['scorecard']) | set(CURRENT['highlights'])


def placeholder(ticker):
    return {'ticker': ticker, 'cluster': CLUSTER_OF.get(ticker), 'name': ticker, 'moat': '—',
            'score': None, 'parts': {}, 'growth_pct': None, 'pe': None, 'buys': 0,
            'upside': None, 'blocked': ['no cached fundamentals'], 'no_data': True}


def score(ticker):
    f = FIN.get(ticker)
    if not f:
        return placeholder(ticker)
    growth = raw(f, 'stats', 'revenueGrowth')
    growth_pct = growth * 100 if growth is not None else None
    net_income = raw(f, 'stats', 'netIncome')
    revenue = raw(f, 'stats', 'totalRevenue')
    pe = raw(f, 'stats', 'trailingPE')
    cons = f.get('consensus') or {}
    buys = (cons.get('strongBuy') or 0) + (cons.get('buy') or 0)
    cluster = CLUSTER_OF.get(ticker)
    moat = MOATS.get(ticker, {}).get('rating', '').lower()

    parts = {
        'moat': MOAT_POINTS.get(moat, 10 if ticker in INCUMBENTS else 0),
        'theme_fit': 20 if cluster else 0,
        'growth': min(growth_pct * 0.5, 20) if growth_pct and growth_pct > 0 else 0,
        'profitability': 15 if (net_income and net_income > 0) else (6 if (revenue and revenue > 1e9) else 0),
        'valuation': (10 if pe and pe < 25 else 6 if pe and pe < 40 else 3 if pe and pe < 80 else 0),
        'coverage': min(buys * 0.5, 10),
    }

    blocked = []
    if ticker in EXCLUDED:
        blocked.append('excluded by policy')
    elif ticker not in INCUMBENTS:
        if ticker not in MOATS:
            blocked.append('no curated moat file')
        if revenue is not None and revenue < 3e8:
            blocked.append('revenue under $300M')
        if buys < 4:
            blocked.append('thin analyst coverage')

    target_mean, current = raw(f, 'analyst', 'targetMeanPrice'), raw(f, 'analyst', 'currentPrice')
    return {
        'ticker': ticker, 'cluster': cluster, 'name': text(f, 'company', 'name') or ticker,
        'moat': MOATS.get(ticker, {}).get('rating', '—'), 'blocked': blocked,
        'score': round(sum(parts.values()), 1), 'parts': parts,
        'growth_pct': round(growth_pct, 1) if growth_pct is not None else None,
        'pe': round(pe, 1) if pe else None, 'buys': buys,
        'upside': round((target_mean / current - 1) * 100, 1) if target_mean and current else None,
    }


ROWS = [score(t) for t in sorted(set(FIN) | INCUMBENTS | set(EXCLUDED))]
BY_TICKER = {r['ticker']: r for r in ROWS}
POOL = [r for r in ROWS if not r['blocked']]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--apply', action='store_true')
    ap.add_argument('--swaps', type=int, default=CHURN.get('target_swaps', 3))
    a = ap.parse_args()

    budget = {'left': min(a.swaps, CHURN.get('max_swaps_per_cycle', 3))}
    used = set(INCUMBENTS)

    panels = {
        'scorecard': {'chosen': [BY_TICKER[t] if t in BY_TICKER else placeholder(t) for t in CURRENT['scorecard']],
                      'rank': lambda r: r['score'] or NULL_SCORE, 'swaps': []},
        'highlights': {'chosen': [BY_TICKER[t] if t in BY_TICKER else placeholder(t) for t in CURRENT['highlights']],
                       'rank': lambda r: (r['score'] or NULL_SCORE) + (r['upside'] or 0) * 0.15 + (r['buys'] or 0) * 0.4,
                       'swaps': []},
    }
    for p in panels.values():
        p['rank_fn'] = p['rank']

    def next_challenger():
        """Best eligible candidate not already on a panel, strongest first."""
        cands = [r for r in POOL if r['ticker'] not in used]
        cands.sort(key=lambda r: r['score'], reverse=True)
        return cands[0] if cands else None

    # pass 1 — forced removals: policy exclusions and incumbents below the floor
    for name, p in panels.items():
        for idx, inc in enumerate(list(p['chosen'])):
            if budget['left'] <= 0:
                break
            if inc.get('no_data'):
                continue
            excluded = inc['ticker'] in EXCLUDED
            decayed = inc['score'] < CHURN['floor']
            if not (excluded or decayed):
                continue
            c = next_challenger()
            if not c:
                break
            if excluded or (c['score'] - inc['score'] >= CHURN['margin']):
                p['chosen'][idx] = c
                used.add(c['ticker'])
                budget['left'] -= 1
                p['swaps'].append({
                    'panel': name, 'in': c['ticker'], 'out': inc['ticker'],
                    'why': (f"excluded by policy ({EXCLUDED[inc['ticker']]})" if excluded
                            else f"{c['score']} vs {inc['score']} — incumbent under floor {CHURN['floor']}")})

    # pass 2 — discretionary rotation toward the per-cycle target
    for name, p in panels.items():
        while budget['left'] > 0:
            eligible = [r for r in p['chosen'] if not r.get('no_data') and r['ticker'] not in EXCLUDED]
            if not eligible:
                break
            weakest = min(eligible, key=lambda r: r['score'])
            c = next_challenger()
            if not c or c['score'] - weakest['score'] < CHURN.get('min_uplift', 3):
                break
            p['chosen'][p['chosen'].index(weakest)] = c
            used.add(c['ticker'])
            budget['left'] -= 1
            p['swaps'].append({
                'panel': name, 'in': c['ticker'], 'out': weakest['ticker'],
                'why': f"cycle rotation: {c['score']} vs {weakest['score']}"})

    # pass 3 — top up to size, respecting cluster targets (+1 tolerance), then relaxing
    for name, p in panels.items():
        size = PROFILE['panels'][name]['slots']
        for relax in (False, True):
            if len(p['chosen']) >= size:
                break
            for r in sorted(POOL, key=p['rank_fn'], reverse=True):
                if len(p['chosen']) >= size:
                    break
                if r['ticker'] in {x['ticker'] for x in p['chosen']}:
                    continue
                if not relax and r['cluster']:
                    have = sum(1 for x in p['chosen'] if x['cluster'] == r['cluster'])
                    if have >= CLUSTER_BY_NAME[r['cluster']]['target'] + 1:
                        continue
                p['chosen'].append(r)
        p['chosen'] = sorted(p['chosen'], key=p['rank_fn'], reverse=True)[:size]

    scorecard = [r['ticker'] for r in panels['scorecard']['chosen']]
    highlights = [r['ticker'] for r in panels['highlights']['chosen']]
    swaps = panels['scorecard']['swaps'] + panels['highlights']['swaps']
    new_set = set(scorecard) | set(highlights)
    entering = sorted(new_set - INCUMBENTS)
    leaving = sorted(INCUMBENTS - new_set)
    unscored = sorted(t for t in INCUMBENTS if t in BY_TICKER and BY_TICKER[t].get('no_data'))

    proposal = {
        'generated': datetime.date.today().isoformat(),
        'profile_version': PROFILE['version'],
        'target_swaps': budget['left'] + len(swaps),
        'incumbents': CURRENT,
        'scorecard': scorecard, 'highlights': highlights,
        'swaps': swaps, 'entering': entering, 'leaving': leaving, 'unscored': unscored,
        'scores': {r['ticker']: {k: r[k] for k in ('score', 'parts', 'moat', 'cluster', 'growth_pct', 'pe', 'upside', 'buys', 'blocked')}
                   for r in ROWS},
    }
    (DATA / 'signal-picks-proposal.json').write_text(json.dumps(proposal, indent=2))

    lines = ['**Signal panels — bi-weekly proposal**', '']
    if not entering and not leaving:
        lines.append('**No change.** Nothing cleared the rotation bar this cycle — a valid result.')
    else:
        lines.append('**Entering:** ' + (', '.join(entering) or '—'))
        lines.append('**Leaving:** ' + (', '.join(leaving) or '—'))
    lines += ['', f"**Scorecard:** {', '.join(scorecard)}",
              f"**Highlights:** {', '.join(highlights)}", '']
    for s in swaps:
        lines.append(f"- {s['panel']}: {s['out']} to {s['in']} — {s['why']}")
    if unscored:
        lines.append(f"\n_Held without a score (no cached fundamentals): {', '.join(unscored)}_")
    lines += ['', '_Nothing goes live without your approval._']
    print('\n'.join(lines))

    if a.apply:
        (DATA / 'scorecard-tickers.json').write_text(json.dumps(scorecard, indent=2) + '\n')
        (DATA / 'signal-highlights-tickers.json').write_text(json.dumps(highlights, indent=2) + '\n')
        print('\nWrote data/scorecard-tickers.json + data/signal-highlights-tickers.json')
        print('Next: python3 scripts/refresh-scorecard.py && python3 scripts/refresh-signal-highlights.py && node build.js')


if __name__ == '__main__':
    main()
