import re, subprocess, html, urllib.parse

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"

feeds = {
 "evertiq": "http://feeds2.feedburner.com/EvertiqCom/All",
 "inc42_buzz": "https://inc42.com/buzz/feed/",
 "devdiscourse_tech": "https://www.devdiscourse.com/rss/technology",
 "newelectronics": "https://www.newelectronics.co.uk/feed/",
 "thelec": "https://thelec.kr/rss/all.xml",
 "moneycontrol": "https://www.moneycontrol.com/rss/business.xml",
 "digitimes": "https://www.digitimes.com/rss/edition/1.xml",
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
            if "c2i" in title.lower() or "infineon" in title.lower():
                hits.append((html.unescape(title), link))
        print(f"=== {name}: {len(items)} items, {len(hits)} hits ===")
        for t, l in hits[:6]:
            print(f"  T: {t}")
            print(f"  L: {l}")
    except Exception as e:
        print(f"=== {name} ERROR {e} ===")
