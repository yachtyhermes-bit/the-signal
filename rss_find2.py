import re, subprocess, html

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"

feeds = {
 "moneycontrol_latest": "https://www.moneycontrol.com/rss/latestnews.xml",
 "moneycontrol_companies": "https://www.moneycontrol.com/rss/companies.xml",
 "devdiscourse_all": "https://www.devdiscourse.com/rss",
 "newelectronics_rss": "https://www.newelectronics.co.uk/rss/",
 "thelec_rss2": "https://thelec.kr/rss/english.xml",
 "cnbctv18_rss": "https://www.cnbctv18.com/feed/",
}

for name, url in feeds.items():
    try:
        r = subprocess.run(["curl", "-s", "-L", "-A", UA, "--max-time", "25", url], capture_output=True, text=True)
        body = r.stdout
        items = re.findall(r'<item>(.*?)</item>', body, re.S)
        hits = []
        for it in items:
            t = re.search(r'<title>(?:<!\[CDATA\[)?(.*?)(?:\]\]>)?</title>', it, re.S)
            l = re.search(r'<link>(.*?)</link>', it, re.S)
            title = (t.group(1) if t else "").strip()
            link = (l.group(1) if l else "").strip()
            if "c2i" in title.lower() or ("infineon" in title.lower()):
                hits.append((html.unescape(title), link))
        print(f"=== {name}: {len(items)} items, {len(hits)} hits ===")
        for t, l in hits[:6]:
            print(f"  T: {t}\n  L: {l}")
    except Exception as e:
        print(f"=== {name} ERROR {e} ===")
