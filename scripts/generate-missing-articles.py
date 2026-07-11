#!/usr/bin/env python3
"""Generate missing article pages from backup homepage's embedded JSON."""
import re, json, os, sys

DIST = '/home/chino/thesignal/dist'
BACKUP = '/home/chino/thesignal/_backup_base/index.html'

with open(BACKUP) as f:
    html = f.read()

m = re.search(r'<script id="articles-data" type="application/json">(.+?)</script>', html)
if not m:
    print("ERROR: articles-data not found in backup")
    sys.exit(1)

articles = json.loads(m.group(1))
print(f"Loaded {len(articles)} articles from backup")

# Article page template (minimal, matches build.js style)
template = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title} — The Signal</title>
<meta name="description" content="{subtitle}">
<link rel="stylesheet" href="/css/main.css">
<link rel="stylesheet" href="/css/pulse-badge.css">
<script async src="https://www.googletagmanager.com/gtag/js?id=G-98KDVDFBCW"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag('js',new Date());gtag('config','G-98KDVDFBCW');</script>
<script src="/js/prices.js" defer></script>
<script src="/js/search.js" defer></script>
<script src="/js/auth.js?v=2" defer></script>
<script src="/js/pulse.js" defer></script>
<script src="/js/theme.js" defer></script>
<script src="/js/comments.js" defer></script>
<script src="/js/share.js" defer></script>
<script src="/js/hive.js?v=2" defer></script>
</head>
<body>
<nav class="nav"><div class="nav-inner">
<a href="/" class="logo"><img src="/img/logo-hex.jpg" alt="The Signal" class="logo-img"><span class="logo-text"><span class="logo-the">THE</span> <strong>SIGNAL</strong></span></a>
<div class="nav-links">
<a href="/sector/ai" class="nav-link">AI</a>
<a href="/sector/cyber" class="nav-link">Cyber</a>
<a href="/sector/defense" class="nav-link">Defense</a>
<a href="/sector/space" class="nav-link">Space</a>
<a href="/sector/mega-cap" class="nav-link">Mega-Cap</a>
<a href="/sector/quantum" class="nav-link">Quantum</a>
<a href="/sector/ai-power" class="nav-link">AI Power</a>
<a href="/sector/fintech" class="nav-link">FinTech</a>
<a href="/sector/etfs" class="nav-link">ETFs</a>
<a href="/hive" class="nav-link">Hive</a>
</div>
<div class="nav-actions">
<button class="nav-btn search-btn" id="searchToggle" aria-label="Search"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg></button>
<button class="nav-btn auth-btn" id="authToggle"><span class="auth-label">Sign In</span></button>
<button class="nav-btn hamburger-btn" id="hamburgerToggle" aria-label="Menu"><span class="hamburger-line"></span><span class="hamburger-line"></span><span class="hamburger-line"></span></button>
</div>
</div></nav>
<div class="mobile-menu" id="mobileMenu"><div class="mobile-menu-links">
<a href="/sector/ai" class="mobile-nav-link">AI</a>
<a href="/sector/cyber" class="mobile-nav-link">Cyber</a>
<a href="/sector/defense" class="mobile-nav-link">Defense</a>
<a href="/sector/space" class="mobile-nav-link">Space</a>
<a href="/sector/mega-cap" class="mobile-nav-link">Mega-Cap</a>
<a href="/sector/quantum" class="mobile-nav-link">Quantum</a>
<a href="/sector/ai-power" class="mobile-nav-link">AI Power</a>
<a href="/sector/fintech" class="mobile-nav-link">FinTech</a>
<a href="/sector/etfs" class="mobile-nav-link">ETFs</a>
<a href="/hive" class="mobile-nav-link">Hive</a>
</div></div>
<main class="main"><article class="article-page">
<div class="article-breadcrumb"><a href="/">Home</a> / <a href="/sector/{sector}">{sector_label}</a> / {ticker}</div>
<div class="article-ticker">{ticker}</div>
<h1 class="article-title">{title}</h1>
<p class="article-subtitle">{subtitle}</p>
<div class="article-meta"><span class="article-date">{date}</span><span class="article-author">The Signal</span></div>
{image_html}
<div class="article-body">{body}</div>
<div class="article-tags">{tags}</div>
<div class="article-links">{links}</div>
</article></main>
<div class="search-overlay" id="searchOverlay"><div class="search-backdrop" id="searchBackdrop"></div><div class="search-modal"><div class="search-header"><input type="text" class="search-input" id="searchInput" placeholder="Search articles by title, ticker, sector, or tag…"><button class="search-close" id="searchClose" aria-label="Close search"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="18" y1="6" x2="6" y2="18"></line><line x1="6" y1="6" x2="18" y2="18"></line></svg></button></div><div class="search-results" id="searchResults"></div><div class="search-empty" id="searchEmpty">Start typing to search articles…</div></div></div>
<label class="theme-switch" id="themeSwitch" aria-label="Toggle theme"><input type="checkbox" id="themeToggleInput"><span class="theme-slider"><svg class="theme-switch-sun" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="5"></circle><line x1="12" y1="1" x2="12" y2="3"></line><line x1="12" y1="21" x2="12" y2="23"></line><line x1="4.22" y1="4.22" x2="5.64" y2="5.64"></line><line x1="18.36" y1="18.36" x2="19.78" y2="19.78"></line><line x1="1" y1="12" x2="3" y2="12"></line><line x1="21" y1="12" x2="23" y2="12"></line><line x1="4.22" y1="19.78" x2="5.64" y2="18.36"></line><line x1="18.36" y1="5.64" x2="19.78" y2="4.22"></line></svg><svg class="theme-switch-moon" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"></path></svg></span></label>
</body></html>"""

generated = 0
for a in articles:
    slug = a['slug']
    dest = os.path.join(DIST, 'article', slug)
    dest_file = os.path.join(dest, 'index.html')
    
    if os.path.exists(dest_file):
        continue  # Already exists from build.js
    
    os.makedirs(dest, exist_ok=True)
    
    # Parse body - it might contain escaped HTML
    body = a.get('bodyHtml', a.get('body', ''))
    # Remove \n and \" escaping from JSON
    body = body.replace('\\n', '\n').replace('\\"', '"').replace('\\\\', '\\')
    
    # Image - handle both string and object formats
    img = a.get('image', {})
    if isinstance(img, str):
        img_src = img
        img_caption = ''
    else:
        img_src = img.get('src', '/img/articles/_default.jpg') if img else '/img/articles/_default.jpg'
        img_caption = img.get('caption', '') if img else ''
    image_html = f'<img src="{img_src}" alt="{img_caption}" class="article-hero">' if img_src else ''
    
    # Tags
    tags = a.get('tags', [])
    tags_html = ' '.join([f'<span class="article-tag">{t}</span>' for t in tags])
    
    # Links - handle different key names
    links = a.get('links', [])
    links_html = '<h4>🔗 LEARN MORE</h4><ul>'
    for l in links:
        label = l.get('label') or l.get('text') or l.get('title') or 'Learn more'
        url = l.get('url') or l.get('href') or '#'
        links_html += f'<li><a href="{url}">{label}</a></li>'
    links_html += '</ul>'
    
    # Sector label
    sector_map = {'ai': 'AI', 'cyber': 'Cyber', 'defense': 'Defense', 'space': 'Space', 'mega-cap': 'Mega-Cap', 'quantum': 'Quantum', 'ai-power': 'AI Power', 'fintech': 'FinTech', 'etfs': 'ETFs', 'semiconductors': 'Semiconductors'}
    sector_label = sector_map.get(a.get('sector', ''), a.get('sector', ''))

    # Date
    date_str = a.get('date', '')
    if date_str:
        try:
            from datetime import datetime
            dt = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
            date_str = dt.strftime('%A, %B %d, %Y')
        except:
            pass
    
    # Escape HTML entities in text fields
    def esc(s):
        return s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;')
    
    html = template.format(
        title=esc(a.get('title', '')),
        subtitle=esc(a.get('subtitle', a.get('summary', ''))),
        sector=a.get('sector', ''),
        sector_label=sector_label,
        ticker=a.get('ticker', ''),
        date=date_str,
        image_html=image_html,
        body=body,
        tags=tags_html,
        links=links_html
    )
    
    with open(dest_file, 'w') as f:
        f.write(html)
    
    generated += 1

print(f"Generated {generated} missing article pages")
PYEOF