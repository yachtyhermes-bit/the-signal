import urllib.parse, urllib.request, re, html
queries = [
 "Akamai Anthropic 1.8 billion deal May 2026",
 "\"No Nvidia Needed\" Akamai Anthropic",
 "Anthropic compute commitments total 2026 billion deals",
 "Anthropic Nscale deal August 2026",
 "Anthropic Google TPU deal billion 2026",
]
for q in queries:
    url="https://news.google.com/rss/search?q="+urllib.parse.quote(q)+"&hl=en-US&gl=US&ceid=US:en"
    req=urllib.request.Request(url, headers={'User-Agent':'Mozilla/5.0'})
    try:
        d=urllib.request.urlopen(req, timeout=25).read().decode('utf-8','ignore')
    except Exception as e:
        print("ERR",q,e); continue
    print("="*8, q)
    for m in list(re.finditer(r'<item>(.*?)</item>', d, re.S))[:22]:
        b=m.group(1)
        def g(t):
            mm=re.search(r'<%s>(.*?)</%s>'%(t,t), b, re.S)
            return html.unescape(re.sub(r'<!\[CDATA\[|\]\]>','',mm.group(1))).strip() if mm else ''
        print(" -", g('title'), "||", g('pubDate'), "||", g('link'))
    print()
