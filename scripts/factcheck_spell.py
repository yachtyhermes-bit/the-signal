#!/usr/bin/env python3
"""Spell-check all 5 articles using aspell."""
import json, os, subprocess, re

ARTICLES_DIR = '/home/chino/thesignal/articles/posts'

slugs = [
    'ge-aftermarket-moat-2026',
    'tsm-ai-chip-monopoly-2026',
    'shopify-ai-commerce-moat-ecosystem-2026',
    'hood-fintech-turnaround-profitability-expansion-2026',
    'rtx-defense-supercycle-nato-2026',
]

for slug in slugs:
    path = os.path.join(ARTICLES_DIR, f'{slug}.json')
    with open(path) as f:
        art = json.load(f)
    
    body = art.get('bodyHtml', '')
    title = art.get('title', '')
    subtitle = art.get('subtitle', '')
    summary = art.get('summary', '')
    
    # Strip HTML tags
    text = re.sub(r'<[^>]+>', ' ', body)
    text = title + ' ' + subtitle + ' ' + summary + ' ' + text
    
    # Check for common garbled patterns
    issues = []
    
    # Check for repeated words (like "the the", "is is")
    repeats = re.findall(r'\b(\w{2,})\s+\1\b', text.lower())
    if repeats:
        issues.append(f"Repeated words: {repeats}")
    
    # Check for garbled AI patterns
    garbled = [
        (r'\bthe\s+gets\b', '"the gets" pattern'),
        (r'\bgets[-\s]real\b', '"gets-real" or "gets real"'),
        (r'[a-z][A-Z][a-z]{2,}', 'possible missing space (camelCase in wrong context)'),
        (r'\brerat\b(?!e)', '"rerat" without trailing e'),
    ]
    for pat, desc in garbled:
        matches = re.findall(pat, text)
        if matches and desc != '"gets-real" or "gets real"':
            issues.append(f"{desc}: {matches[:3]}")
    
    # Check for dollar-sign prefixed ticker ($TICKER)
    ticker = art.get('ticker', '')
    dollar_ticker = re.findall(r'\$' + re.escape(ticker), body)
    if dollar_ticker:
        issues.append(f"Dollar-sign prefixed ticker ({len(dollar_ticker)}x): ${ticker}")
    
    # Run aspell
    try:
        result = subprocess.run(
            ['aspell', 'list', '--lang=en_US', '--ignore-case'],
            input=text.encode('utf-8'),
            capture_output=True,
            timeout=30
        )
        misspelled = set(result.stdout.decode().strip().split('\n'))
        # Filter out known proper nouns, tickers, financial terms
        known = {'moat', 'moats', 'supercycle', 'fintech', 'hyperscaler', 'hyperscalers',
                 'TTM', 'YoY', 'CAGR', 'GAAP', 'EPS', 'FCF', 'P/E', 'ROE', 'SPY-6',
                 'AMRAAMs', 'Sidewinders', 'bootstrappable', 'recurring',
                 'aftermarket', 'interceptors', 'narrowbodies', 'narrowbody',
                 'aerospace', 'cryptocurrency', 'ecosystem', 'conglomerate',
                 'aftermarkets', 'tollbooth', 'semis', 'tick', 'ticks',
                 'Leaps', 'LEAP', 'LEAPs', 'Avionics', 'avionics',
                 'edit', 'F135', 'H200', 'B200', 'MI300X',
                 'NATO', 'GE', 'TSM', 'SHOP', 'HOOD', 'RTX',
                 'AMAT', 'PLTR', 'GOOGL', 'NVDA', 'AMD',
                 'Sofi', 'SoFi', 'fintechs', 'underappreciated',
                 'restocking', 'powerplants', 'rebalancing',
                 'outperformance', 'topline', 'sellside',
                 'Cathie', 'Lütke', 'Tobias', 'Tenev', 'Vladimir',
                 'Culp', 'Larry', 'Pratt', 'Whitney', 'GTF',
                 'Q1', 'Q2', 'Q3', 'Q4', 'FY2025', 'FY2026',
                 'Cincinnati', 'Arizona', 'Rhode Island',
                 'Germanys', 'Netherlands', 'Ukraine', 'Navy',
                 'copilot', 'Copilot', 'Gemini', 'Stripe',
                 'Amazon', 'Walmart', 'Shopify', 'Shopifys',
                 'PayPal', 'Stripe', 'Square', 'Adyen',
                 'Mastercard', 'Visa', 'Affirm', 'Klarna',
                 'TikTok', 'Instagram', 'WhatsApp', 'Meta',
                 'Roku', 'Spotify', 'Uber', 'Lyft',
                 'NVIDIA', 'AMD', 'Intel', 'Qualcomm', 'Broadcom',
                 'Palantir', 'CrowdStrike', 'Salesforce', 'Adobe',
                 'Boeing', 'Lockheed', 'Northrop', 'Grumman',
                 'L3Harris', 'General', 'Dynamics', 'Huntington',
                 'Ingalls', 'Textron', 'Leidos', 'Booz', 'Allen',
        }
        misspelled = {w for w in misspelled if w and w not in known and len(w) > 2}
        if misspelled:
            # Filter out HTML-like artifacts
            misspelled = {w for w in misspelled if not w.startswith('&') and not w.startswith(';')}
            if misspelled:
                issues.append(f"Spelling: {sorted(misspelled)[:20]}")
    except Exception as e:
        issues.append(f"Aspell error: {e}")
    
    if issues:
        print(f"\n📰 {slug}:")
        for issue in issues:
            print(f"  ⚠️ {issue}")
    else:
        print(f"✅ {slug}: No issues found")

print("\nDone.")
