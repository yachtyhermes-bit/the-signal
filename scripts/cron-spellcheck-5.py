#!/usr/bin/env python3
"""Spell-check the 5 most recent articles using aspell."""
import json, re, subprocess, glob

articles = []
for f in glob.glob('articles/posts/*.json'):
    with open(f) as fh:
        try:
            a = json.load(fh)
            if a.get('date'):
                articles.append((a['date'], a['slug'], f, a.get('ticker',''), a.get('title','')))
        except:
            pass

articles.sort(key=lambda x: x[0], reverse=True)
recent = articles[:5]

for date, slug, path, ticker, title in recent:
    with open(path) as fh:
        a = json.load(fh)
    body = a.get('bodyHtml', '')
    text = re.sub(r'<[^>]+>', ' ', body)
    text = re.sub(r'&[a-z]+;', ' ', text)
    text = re.sub(r'https?://\S+', '', text)
    text = re.sub(r'\$\d+(?:[,.\d]*)?[BMK]?', '', text)
    text = re.sub(r'[^\w\s\'-]', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    
    p = subprocess.run(['aspell', 'list', '--lang=en_US'], input=text.encode('utf-8'), capture_output=True, timeout=30)
    misspelled = set(w for w in p.stdout.decode('utf-8', errors='replace').strip().split('\n') if len(w.strip()) > 1)
    
    print(f'--- {slug} ({ticker}) ---')
    if misspelled:
        print(f'  Misspellings ({len(misspelled)}): {", ".join(sorted(misspelled)[:20])}')
    else:
        print(f'  ✅ Clean')
    print()
