import sys, re, subprocess, html

def fetch(url):
    # resolve google news redirect
    if 'news.google.com/rss/articles' in url:
        r = subprocess.run(['curl','-s','-L','--compressed','-A','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36', url], capture_output=True, text=True, timeout=45)
        content = r.stdout
    else:
        r = subprocess.run(['curl','-s','-L','--compressed','-A','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36', url], capture_output=True, text=True, timeout=45)
        content = r.stdout
    # strip scripts/styles/tags
    content = re.sub(r'<(script|style)[^>]*>.*?</\1>', ' ', content, flags=re.S|re.I)
    content = re.sub(r'<[^>]+>', ' ', content)
    content = html.unescape(content)
    content = re.sub(r'\s+', ' ', content)
    return content[:4000]

for url in sys.argv[1:]:
    print("="*100)
    print("URL:", url[:120])
    try:
        print(fetch(url))
    except Exception as e:
        print("ERR", e)
