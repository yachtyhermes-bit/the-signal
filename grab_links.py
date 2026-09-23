import re, subprocess, html

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"

targets = {
 "evertiq": "https://evertiq.com/news",
 "devdiscourse": "https://www.devdiscourse.com/search?q=Infineon+C2i+Semiconductors",
 "thelec": "https://thelec.kr/news/articleList.html?sc_word=Infineon+C2i",
 "digitimes": "https://www.digitimes.com/tag/infineon/001.html",
 "inc42": "https://inc42.com/buzz/",
 "moneycontrol": "https://www.moneycontrol.com/news/business/",
}

for name, url in targets.items():
    try:
        r = subprocess.run(["curl", "-s", "-A", UA, "--max-time", "25", url], capture_output=True, text=True)
        body = r.stdout
        # find hrefs whose context mentions c2i or infineon
        links = set()
        for m in re.finditer(r'<a[^>]+href="([^"]+)"[^>]*>(.*?)</a>', body, re.S|re.I):
            href, text = m.group(1), re.sub(r'<[^>]+>', '', m.group(2))
            joined = (href + " " + text).lower()
            if "c2i" in joined or ("infineon" in joined and "acqui" in joined):
                links.add((html.unescape(href), re.sub(r'\s+', ' ', text).strip()[:90]))
        print(f"=== {name} ({len(links)} matches) ===")
        for h, t in list(links)[:10]:
            print(f"  {h}  |  {t}")
    except Exception as e:
        print(f"=== {name} ERROR {e} ===")
