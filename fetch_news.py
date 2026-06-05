import urllib.request, json, sys

# Try to get market news from various free sources
sources = [
    ("https://finance.yahoo.com/news/", "Yahoo Finance"),
]

# Use a simple approach - fetch from finviz
try:
    req = urllib.request.Request(
        "https://finviz.com/news.ashx",
        headers={"User-Agent": "Mozilla/5.0"}
    )
    with urllib.request.urlopen(req, timeout=10) as resp:
        data = resp.read().decode()
        # Extract news items
        import re
        items = re.findall(r'<a class="nn-tab-link".*?href="(.*?)".*?>(.*?)</a>', data, re.DOTALL)
        for url, title in items[:30]:
            title_clean = re.sub(r'<[^>]+>', '', title).strip()
            print(f"{title_clean[:120]} | {url[:80]}")
except Exception as e:
    print(f"finviz error: {e}", file=sys.stderr)

print("---SEPARATOR---")

# Try finviz news JSON
try:
    req = urllib.request.Request(
        "https://finviz.com/api/news.ashx",
        headers={"User-Agent": "Mozilla/5.0"}
    )
    with urllib.request.urlopen(req, timeout=10) as resp:
        data = resp.read().decode()
        print(data[:3000])
except Exception as e:
    print(f"finviz api error: {e}", file=sys.stderr)
