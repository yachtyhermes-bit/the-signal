import urllib.request, json, re, sys

# Try Yahoo Finance front page
try:
    req = urllib.request.Request(
        "https://finance.yahoo.com/topic/stock-market-news/",
        headers={"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"}
    )
    with urllib.request.urlopen(req, timeout=10) as resp:
        html = resp.read().decode('utf-8', errors='replace')
        # Extract story headlines
        items = re.findall(r'<h3[^>]*>.*?<a[^>]*href="(https?://finance\.yahoo\.com[^"]*)"[^>]*>(.*?)</a>.*?</h3>', html, re.DOTALL)
        for url, title in items[:20]:
            title_clean = re.sub(r'<[^>]+>', '', title).strip()
            print(f"{title_clean[:120]}")
        if not items:
            # Try alternative pattern
            items2 = re.findall(r'<a[^>]*href="(https?://finance\.yahoo\.com/video/[^"]*)"[^>]*>(.*?)</a>', html, re.DOTALL)
            for url, title in items2[:10]:
                title_clean = re.sub(r'<[^>]+>', '', title).strip()
                print(f"[VIDEO] {title_clean[:120]}")
            if not items2:
                # Just print some text to see what we got
                text = re.sub(r'<[^>]+>', ' ', html)
                text = re.sub(r'\s+', ' ', text)
                # Find news-like patterns
                for match in re.finditer(r'(?:Stock|Market|Shares|S&P|Nasdaq|Dow|AI|Defense|Space|Cyber|Quantum|Earnings|Deal|Buy|Sell|Surge|Plunge|Rally|Jump|Drop)[^.]{20,120}\.', text):
                    print(match.group().strip())
except Exception as e:
    print(f"Yahoo error: {e}", file=sys.stderr)

print("===BREAKER===")

# Try Reuters
try:
    req = urllib.request.Request(
        "https://www.reuters.com/markets/",
        headers={"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"}
    )
    with urllib.request.urlopen(req, timeout=10) as resp:
        html = resp.read().decode('utf-8', errors='replace')
        headlines = re.findall(r'<h[1-6][^>]*>(.*?)</h[1-6]>', html, re.DOTALL)
        for h in headlines[:20]:
            clean = re.sub(r'<[^>]+>', '', h).strip()
            if len(clean) > 20:
                print(clean[:150])
except Exception as e:
    print(f"Reuters error: {e}", file=sys.stderr)
