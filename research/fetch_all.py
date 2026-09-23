import subprocess, re, html, sys, urllib.parse

UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36'

def rss_links(query, n=3):
    q = urllib.parse.quote(query)
    r = subprocess.run(['curl','-s', f'https://news.google.com/rss/search?q={q}&hl=en-US&gl=US&ceid=US:en'], capture_output=True, text=True, timeout=45)
    items = re.findall(r'<item>(.*?)</item>', r.stdout, re.S)
    out = []
    for it in items[:n]:
        t = re.search(r'<title>(.*?)</title>', it, re.S)
        l = re.search(r'<link>(.*?)</link>', it, re.S)
        out.append((t.group(1).strip() if t else '', l.group(1).strip() if l else ''))
    return out

def fetch(url):
    r = subprocess.run(['curl','-s','-L','--compressed','-A',UA, url], capture_output=True, text=True, timeout=45)
    c = r.stdout
    c = re.sub(r'<(script|style|noscript)[^>]*>.*?</\1>', ' ', c, flags=re.S|re.I)
    c = re.sub(r'<[^>]+>', ' ', c)
    c = html.unescape(c)
    c = re.sub(r'\s+', ' ', c)
    return c[:5000]

jobs = [
    ('Reuters 7-year missile deals', 'Pentagon signs 7-year deals to increase missile production'),
    ('Anadolu triple Patriot quadruple THAAD', 'Anadolu triple Patriot quadruple THAAD production'),
    ('Stocktwits counter-drone', 'LMT Stock Gains Premarket Lockheed Martin Reveals New Counter-Drone'),
    ('Stocktwits GM-LMT', 'GM LMT Stocks Gain Overnight General Motors Lockheed Martin Weapons Parts'),
    ('DIE Javelin Tata', 'Raytheon Lockheed Martin select Tata Javelin co-production India Defence Industry Europe'),
    ('Breaking Defense PAC-3 54B', 'Army adds 54B to Lockheed PAC-3 agreement'),
    ('GovCon Wire backlog', 'Lockheed Martin Lifts 2026 Guidance on Record 230B Backlog'),
]
for name, q in jobs:
    print('#'*110)
    print('### ', name)
    links = rss_links(q, 2)
    for title, url in links:
        print('-- TITLE:', title)
        try:
            txt = fetch(url)
            print(txt[:3500])
        except Exception as e:
            print('ERR', e)
        print()
        break
