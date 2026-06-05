#!/usr/bin/env python3
"""Test Wikipedia image API for company tickers"""
import json, urllib.request, sys, time

companies = {
    "NVDA": "Nvidia",
    "RKLB": "Rocket Lab",
    "PLTR": "Palantir Technologies",
    "AVGO": "Broadcom Inc.",
    "RDW": "Redwire",
    "LMT": "Lockheed Martin",
    "AMD": "Advanced Micro Devices",
    "BA": "Boeing",
    "GOOGL": "Google",
    "AMZN": "Amazon",
    "META": "Meta Platforms",
    "AAPL": "Apple Inc.",
    "MSFT": "Microsoft",
    "TSLA": "Tesla Inc.",
    "ASTS": "AST SpaceMobile",
    "LUNR": "Intuitive Machines",
    "CRWD": "CrowdStrike",
    "NET": "Cloudflare",
}

for ticker, company in companies.items():
    url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{company.replace(' ', '_')}"
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'TheSignal/1.0'})
        resp = urllib.request.urlopen(req, timeout=10)
        data = json.loads(resp.read())
        img = data.get('originalimage', {}).get('source', 'NO IMAGE')
        desc = data.get('extract', '')[:120].replace('\n', ' ')
        print(f"{ticker:6s} | {company:25s} | {'✅ IMAGE' if img != 'NO IMAGE' else '❌ NO IMAGE'}")
        if img != 'NO IMAGE':
            print(f"       URL: {img}")
    except Exception as e:
        print(f"{ticker:6s} | {company:25s} | ❌ ERROR: {str(e)[:60]}")
    time.sleep(0.5)
