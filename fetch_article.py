import re, subprocess, sys, html

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"

def fetch(url):
    r = subprocess.run(["curl", "-s", "-L", "-A", UA, "--max-time", "30", url], capture_output=True, text=True)
    return r.stdout

def strip(body):
    # remove scripts/styles
    body = re.sub(r'<(script|style)[^>]*>.*?</\1>', ' ', body, flags=re.S|re.I)
    body = re.sub(r'<[^>]+>', ' ', body)
    body = html.unescape(body)
    body = re.sub(r'\s+', ' ', body)
    return body

for url in sys.argv[1:]:
    print("="*100)
    print("URL:", url)
    print("="*100)
    body = fetch(url)
    text = strip(body)
    # print the region containing c2i / infineon mentions
    low = text.lower()
    idx = low.find("c2i")
    if idx == -1:
        idx = low.find("infineon")
    if idx != -1:
        start = max(0, idx - 200)
        print(text[start:start+6000])
    else:
        print("NO MATCH; first 1500 chars:")
        print(text[:1500])
