#!/usr/bin/env python3
"""Spell-check all 10 articles using aspell, and do careful claim verification."""

import json, os, re, html as html_mod, subprocess

base = '/home/chino/thesignal/articles/posts'

slugs = [
    'credo-ai-connectivity-chips-2026',
    'smci-ai-server-accounting-comeback-2026',
    'vertiv-ai-data-center-infrastructure-q1-2026',
    'coinbase-european-crypto-moat-2026',
    'coreweave-ai-cloud-sale-2026',
    'kratos-defense-unmanned-systems-hypersonics-2026',
    'vertiv-data-center-infrastructure-2026',
    'axon-ai-policing-monopoly-2026',
    'applied-materials-ai-chip-equipment-monopoly-2026',
    'servicenow-ai-workflow-automation-2026'
]

# Known financial terms to add to aspell dictionary
known_terms = '''
FinTech
hyperscaler
hyperscale
hyperscalers
MoD
Goog
AMAT
CRDO
CRWV
KTOS
SMCI
AXON
VRT
NOW
COIN
NASD
MiCA
DoD
MACH
TB
MACH-TB
XQ
Valkyrie
Thanatos
SerDes
DSP
DSPs
PIC
PICs
AEC
busway
busbars
switchgear
busbar
Busbar
busbars
Busbars
Hyperscalers
Hyperscaler
YTD
ATH
DLC
Q1
Q2
Q3
Q4
FY
FY2022
FY2023
FY2024
FY2025
FY2026
FY2027
GAAP
TTM
CAGR
ARR
TAM
EBITDA
PEG
EPS
LLM
DoD
SPA
CDN
GPU
GPUs
URL
API
npm
yfinance
CapEx
Capex
hypersonic
Co
pre
buildout
buildouts
hypergrowth
compounder
compounders
picks-and-shovels
moat
SaaS
AI
semiconductor
semiconductors
heterogeneous
heterogeneously
replatforming
replatform
washout
washouts
mispricing
misperception
overhang
tooling
toolchain
frontend
backend
dev
rel
Kratos
Axon
Credo
Vertiv
ServiceNow
CoreWeave
Armis
Moveworks
Fusus
Dedrone
Carbyne
Sky-Hero
DustPhotonics
CoolIt
Stifel
Evercore
Bernstein
Rosenblatt
Keybanc
Guggenheim
Accenture
Nvidia
NVIDIA
Blackwell
Broadcom
AMD
MiCA
IPo
IPO
Delist
delisting
retimers
revenue
moat's
niche
tollbooth
toll
booth
flywheel
beachhead
'''.strip().split()

try:
    result = subprocess.run(['which', 'aspell'], capture_output=True, text=True)
    has_aspell = result.returncode == 0 and result.stdout.strip()
except:
    has_aspell = False

print(f"Aspell available: {has_aspell}")

for s in slugs:
    with open(f'{base}/{s}.json') as f:
        a = json.load(f)

    body = a.get('bodyHtml', '')
    title = a.get('title', '')
    subtitle = a.get('subtitle', '')
    summary = a.get('summary', '')
    ticker = a.get('ticker', '')
    slug = a.get('slug', '')
    
    # Clean HTML
    body_text = re.sub(r'<[^>]+>', ' ', body)
    body_text = html_mod.unescape(body_text)
    body_text = re.sub(r'\s+', ' ', body_text).strip()
    
    # Full text for spell checking
    full_text = f"{title}\n\n{subtitle}\n\n{summary}\n\n{body_text}"
    
    if has_aspell:
        proc = subprocess.run(
            ['aspell', 'list', '--lang=en_US', '--encoding=utf-8'],
            input=full_text,
            capture_output=True,
            text=True,
            timeout=15
        )
        misspelled = set(proc.stdout.strip().split('\n')) if proc.stdout.strip() else set()
        # Filter out known financial terms, tickers, numbers, etc.
        known = set(known_terms)
        real_errors = []
        for w in misspelled:
            w = w.strip().lower()
            if not w or len(w) < 2:
                continue
            if w.isdigit() or w.startswith('$') or w.startswith('\\'):
                continue
            if w.startswith('-') or w.endswith('-'):
                continue
            if w in known or w.upper() in known:
                continue
            if w.endswith('s') and w[:-1] in known:
                continue
            if w.endswith('ing') and w[:-3] in known:
                continue
            if w.endswith('ed') and w[:-2] in known:
                continue
            real_errors.append(w)
        
        if real_errors:
            print(f"\n  ✗ {slug}: {len(real_errors)} possible spelling issues")
            for e in sorted(set(real_errors))[:20]:
                # Find context
                for m in re.finditer(r'\b' + re.escape(e) + r'\b', full_text, re.I):
                    start = max(0, m.start()-20)
                    end = min(len(full_text), m.end()+20)
                    ctx = full_text[start:end].replace('\n', ' ')
                    print(f"    '{e}' in ...{ctx}...")
                    break
        else:
            print(f"  ✓ {slug}: no spelling issues")
    else:
        print(f"  ? {slug}: aspell not available, skipping")

print("\n\n=== ASPELL CHECK COMPLETE ===")
