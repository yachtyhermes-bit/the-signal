import subprocess, re, sys, urllib.parse
from xml.etree import ElementTree as ET

def news(q, n=12):
    url = "https://news.google.com/rss/search?q=" + urllib.parse.quote(q) + "&hl=en-US&gl=US&ceid=US:en"
    out = subprocess.run(["curl","-s","--compressed","-A","Mozilla/5.0",url], capture_output=True, text=True).stdout
    try:
        root = ET.fromstring(out)
    except Exception as e:
        print("PARSE ERR", e); return
    print("#### QUERY:", q)
    for it in root.iter("item"):
        t = it.findtext("title"); d = it.findtext("pubDate")
        src = it.find("source")
        print(f"  [{d}] {t}  <{(src.text if src is not None else '?')}>")
    print()

for q in sys.argv[1:]:
    news(q)
