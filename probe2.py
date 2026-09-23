import re, subprocess, html

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"

targets = {
 "thelec_net_search": "https://www.thelec.net/news/articleList.html?sc_word=C2i",
 "moneycontrol_tag": "https://www.moneycontrol.com/news/tags/infineon.html",
 "cnbctv18_tag": "https://www.cnbctv18.com/tags/infineon.htm",
 "devdiscourse_tech": "https://www.devdiscourse.com/article/technology",
 "digitimes_c2i_tag": "https://www.digitimes.com/tag/c2i/001.html",
}

for name, url in targets.items():
    try:
        r = subprocess.run(["curl", "-s", "-L", "-A", UA, "--max-time", "25", url], capture_output=True, text=True)
        body = r.stdout
        links = set()
        for m in re.finditer(r'<a[^>]+href="([^"]+)"[^>]*>(.*?)</a>', body, re.S|re.I):
            href, text = m.group(1), re.sub(r'<[^>]+>', '', m.group(2))
            j = (href + " " + text).lower()
            if "c2i" in j or ("infineon" in j and "acqui" in j):
                links.add((html.unescape(href), re.sub(r'\s+', ' ', text).strip()[:90]))
        print(f"=== {name}: len={len(body)}, {len(links)} hits ===")
        for h, t in list(links)[:12]:
            print(f"  {h}  |  {t}")
    except Exception as e:
        print(f"=== {name} ERROR {e} ===")
