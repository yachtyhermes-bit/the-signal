import re, subprocess, sys, html

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"

def fetch(url):
    r = subprocess.run(["curl", "-s", "-L", "-A", UA, "--max-time", "30", url], capture_output=True, text=True)
    return r.stdout

def strip(body):
    body = re.sub(r'<(script|style)[^>]*>.*?</\1>', ' ', body, flags=re.S|re.I)
    body = re.sub(r'<[^>]+>', ' ', body)
    body = html.unescape(body)
    return re.sub(r'\s+', ' ', body)

url = sys.argv[1]
start = int(sys.argv[2]) if len(sys.argv) > 2 else 0
length = int(sys.argv[3]) if len(sys.argv) > 3 else 6000
text = strip(fetch(url))
low = text.lower()
idx = low.find("c2i")
if idx == -1: idx = low.find("infineon")
if idx == -1: idx = 0
s = idx + start
print(text[s:s+length])
