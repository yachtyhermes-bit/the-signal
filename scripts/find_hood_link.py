#!/usr/bin/env python3
"""Try to find the correct HOOD earnings link."""
import urllib.request, urllib.error

urls = [
    "https://investors.robinhood.com/news-events/press-releases/detail/48/robinhood-reports-first-quarter-2026-results",
    "https://investors.robinhood.com/news-events/press-releases/default.aspx",
    "https://investors.robinhood.com/overview/default.aspx",
    "https://investors.robinhood.com/",
    "https://about.robinhood.com/us-en/news/",
    "https://finance.yahoo.com/quote/HOOD/",
]

for url in urls:
    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=8) as resp:
            print(f"✅ {resp.status} | {url}")
    except urllib.error.HTTPError as e:
        if e.code == 429:
            print(f"⚠️ 429 (rate limit) | {url}")
        else:
            print(f"❌ {e.code} | {url}")
    except Exception as e:
        print(f"❓ {type(e).__name__} | {url}: {str(e)[:60]}")
