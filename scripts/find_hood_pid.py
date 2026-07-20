#!/usr/bin/env python3
"""Try Robinhood IR press release IDs."""
import urllib.request, urllib.error

for pid in [47, 49, 50, 51, 52, 53, 46, 45, 44]:
    url = f"https://investors.robinhood.com/news-events/press-releases/detail/{pid}/robinhood-reports-first-quarter-2026-results"
    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=5) as resp:
            print(f"✅ {resp.status} | ID={pid}: {url}")
            break
    except urllib.error.HTTPError as e:
        if e.code != 404:
            print(f"⚠️ {e.code} | ID={pid}")
    except Exception as e:
        print(f"❓ ID={pid}: {str(e)[:50]}")

# If none found, try generic Q1 2026
try:
    req = urllib.request.Request("https://investors.robinhood.com/news-events/press-releases/robinhood-reports-first-quarter-2026-results")
    with urllib.request.urlopen(req, timeout=5) as resp:
        print(f"✅ Generic: {resp.status}")
except Exception as e:
    print(f"❌ Generic: {e}")
