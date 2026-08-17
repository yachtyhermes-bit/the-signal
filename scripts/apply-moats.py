#!/usr/bin/env python3
"""Apply strict re-rated moats to data/moat-*.json with human corrections."""
import json, glob, os

DATA = '/home/chino/thesignal/data'
ai = json.load(open('/tmp/moat-rerate.json'))

# Human corrections after review (Morningstar-aligned / identity fixes)
OVERRIDES = {
    'CRWV': {  # identity fix: CoreWeave, NOT CrowdStrike
        'rating': 'Narrow', 'stars': 2, 'confidence': 'Low',
        'industry': 'Cloud Computing - AI Infrastructure',
        'rationale': 'CoreWeave is a capital-intensive GPU cloud provider with little proprietary technology; take-or-pay contracts and cluster integration create modest switching costs, but customers (Microsoft, Meta) hold the pricing power and margins are thin.',
        'factors': {
            'Switching Costs': {'score': 3, 'rationale': 'custom GPU clusters are deeply integrated into customer stacks, but contracts are finite and infrastructure is portable in theory'},
            'Intangible Assets': {'score': 1, 'rationale': 'no proprietary silicon or software; competes on capacity and price'},
            'Network Effect': {'score': 1, 'rationale': 'no network effects; utilization is scale-driven, not user-driven'},
            'Cost Advantage': {'score': 2, 'rationale': 'flexible NVIDIA allocation helps, but hyperscalers enjoy better unit economics'},
            'Efficient Scale': {'score': 2, 'rationale': 'huge capital barriers deter entrants, but the market is contested by hyperscalers and rivals'},
        },
    },
    'SPCX': {  # identity fix: SpaceX (Space Exploration Technologies), NOT Momentus
        'rating': 'Wide', 'stars': 4, 'confidence': 'High',
        'industry': 'Space Launch & Satellite',
        'rationale': 'SpaceX owns the only reusable launch architecture at scale and Starlink creates a self-funding network-effect moat with no credible near-term rival.',
        'factors': {
            'Switching Costs': {'score': 4, 'rationale': 'launch customers and Starlink subscribers face high re-platforming costs'},
            'Intangible Assets': {'score': 5, 'rationale': 'reusable rocket IP and manufacturing flywheel are unmatched'},
            'Network Effect': {'score': 5, 'rationale': 'Starlink scale lowers cost per user and improves service, compounding advantage'},
            'Cost Advantage': {'score': 5, 'rationale': 'reusability collapses marginal launch cost versus all competitors'},
            'Efficient Scale': {'score': 4, 'rationale': 'launch cadence and vertical integration create scale others cannot match'},
        },
    },
    'META': {  # Morningstar: Narrow (advertising duopoly, but platform risk + AI spend)
        'rating': 'Narrow', 'stars': 3, 'confidence': 'Medium',
        'rationale': 'Meta has genuine network effects but faces platform dependence (iOS), regulatory pressure, and massive AI capex; Morningstar rates it Narrow.',
        'factors': {
            'Switching Costs': {'score': 2, 'rationale': 'users and advertisers can shift spend; no data lock-in'},
            'Intangible Assets': {'score': 4, 'rationale': 'brands (Facebook, Instagram, WhatsApp) and proprietary AI ranking'},
            'Network Effect': {'score': 5, 'rationale': '3B+ users create classic two-sided network effects'},
            'Cost Advantage': {'score': 2, 'rationale': 'AI infrastructure spending is enormous and rising'},
            'Efficient Scale': {'score': 3, 'rationale': 'advertising scale is efficient, but competition from TikTok/YouTube persists'},
        },
    },
    'AMZN': {  # Morningstar: Wide (AWS + logistics flywheel)
        'rating': 'Wide', 'stars': 4, 'confidence': 'High',
        'rationale': 'AWS is the scale leader in cloud with deep switching costs and Amazon retail logistics create a wide, self-reinforcing moat.',
    },
    'AVGO': {  # Morningstar: Wide (custom silicon + software switching costs)
        'rating': 'Wide', 'stars': 4, 'confidence': 'High',
        'rationale': 'Broadcom\'s custom ASIC designs, networking silicon, and mission-critical software create high switching costs; Morningstar rates it Wide.',
    },
    'ANET': {  # Morningstar: Wide (Ethernet switching dominance)
        'rating': 'Wide', 'stars': 4, 'confidence': 'High',
        'rationale': 'Arista\'s dominant position in high-speed data-center Ethernet switching with high margins and deep customer integration; Morningstar rates it Wide.',
    },
    'MU': {  # Morningstar: Narrow (HBM qualification + memory oligopoly)
        'rating': 'Narrow', 'stars': 3, 'confidence': 'Medium',
        'rationale': 'Memory is cyclical and capital-intensive, but HBM qualification with AI customers and a 3-player DRAM oligopoly create a narrow moat.',
    },
    'SPACEX': {  # duplicate entry for the phantom ticker (not in financials)
        'rating': 'Wide', 'stars': 4, 'confidence': 'High',
        'industry': 'Space Launch & Satellite',
        'rationale': 'Same as SPCX — SpaceX. This ticker is not in financials.json; SPCX is the live one.',
    },
}

def build_entry(ticker, data, ov):
    if ticker in OVERRIDES:
        ov = OVERRIDES[ticker]
        rating, stars, conf = ov['rating'], ov['stars'], ov['confidence']
        rationale = ov['rationale']
        industry = ov.get('industry', data.get('industry', 'n/a'))
        factors = ov.get('factors')
        if factors is None and data.get('factors'):
            factors = data['factors']
    else:
        rating, stars, conf = data['rating'], data['stars'], data['confidence']
        rationale = data['rationale']
        industry = data.get('industry', 'n/a')
        factors = data.get('factors')
    sources = []
    if factors:
        for name, f in factors.items():
            sources.append({'name': name, 'score': f['score'], 'rationale': f['rationale']})
    return {'symbol': ticker, 'industry': industry, 'rating': rating,
            'stars': stars, 'confidence': conf, 'rationale': rationale,
            'sources': sources}

count = 0
for f in sorted(glob.glob(os.path.join(DATA, 'moat-*.json'))):
    ticker = os.path.basename(f)[5:-5]
    if ticker not in ai:
        continue
    entry = build_entry(ticker, ai[ticker], OVERRIDES.get(ticker))
    json.dump(entry, open(f, 'w'), indent=2)
    count += 1
    print(f"{ticker:6} {entry['rating']:7} {entry['stars']}★ {entry['confidence']:6} — {entry['rationale'][:60]}")

print(f"\n{count} moat files rewritten")
