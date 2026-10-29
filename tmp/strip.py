import sys, re, html
from html.parser import HTMLParser

class P(HTMLParser):
    def __init__(self):
        super().__init__()
        self.skip = 0
        self.out = []
    def handle_starttag(self, tag, attrs):
        if tag in ('script','style','noscript','svg'):
            self.skip += 1
        if tag in ('p','div','tr','br','h1','h2','h3','h4','li','table','section'):
            self.out.append('\n')
        if tag in ('td','th'):
            self.out.append(' | ')
    def handle_endtag(self, tag):
        if tag in ('script','style','noscript','svg') and self.skip:
            self.skip -= 1
    def handle_data(self, d):
        if not self.skip:
            self.out.append(d)

def conv(txt):
    p = P(); p.feed(txt)
    s = ''.join(p.out)
    s = html.unescape(s)
    s = re.sub(r'[ \t\xa0]+', ' ', s)
    s = re.sub(r'\n\s*\n+', '\n', s)
    return s.strip()

if __name__ == '__main__':
    for f in sys.argv[1:]:
        raw = open(f, encoding='utf-8', errors='ignore').read()
        print(f"\n########## {f} ##########")
        print(conv(raw))
