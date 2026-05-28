#!/usr/bin/env node
// Static site generator — reads article JSONs, outputs dist/ folder
const fs = require('fs');
const path = require('path');

const ROOT = __dirname;
const ARTICLES_DIR = path.join(ROOT, 'articles', 'posts');
const DIST = path.join(ROOT, 'dist');
const PUBLIC = path.join(ROOT, 'public');
const DATA_DIR = path.join(ROOT, 'data');

const SECTORS = {
  ai: { name: 'AI', tickers: ['NVDA','AMD','AVGO','MRVL','TSM','ASML','MU','CBRS','CRWV','NBIS'], color: '#3b82f6' },
  cyber: { name: 'Cybersecurity', tickers: ['CRWD','PANW','FTNT','ZS','S','CHKP','CYBR','TENB','RBRK'], color: '#22c55e' },
  defense: { name: 'Defense', tickers: ['LMT','RTX','NOC','GD','LHX','KTOS','AVAV','PL','AXON','GE'], color: '#fbbf24' },
  space: { name: 'Space', tickers: ['RKLB','RDW','LUNR','ASTS'], color: '#a78bfa' },
  'mega-cap': { name: 'Mega-Cap', tickers: ['AAPL','MSFT','GOOGL','AMZN','META','TSLA'], color: '#f87171' },
  quantum: { name: 'Quantum', tickers: ['IONQ','QBTS','QUBT','RGTI'], color: '#06b6d4' },
};

const COMPANY_INFO = {
  'NVDA': { name: 'NVIDIA Corporation', url: 'https://www.nvidia.com/' },
  'CBRS': { name: 'Cerebras Systems', url: 'https://www.cerebras.net/' },
  'PLTR': { name: 'Palantir Technologies', url: 'https://www.palantir.com/' },
  'RKLB': { name: 'Rocket Lab USA', url: 'https://www.rocketlabusa.com/' },
  'RDW': { name: 'Redwire Corporation', url: 'https://www.rdw.com/' },
  'AMD': { name: 'Advanced Micro Devices', url: 'https://www.amd.com/' },
  'AVGO': { name: 'Broadcom Inc.', url: 'https://www.broadcom.com/' },
  'CRWD': { name: 'CrowdStrike Holdings', url: 'https://www.crowdstrike.com/' },
  'PANW': { name: 'Palo Alto Networks', url: 'https://www.paloaltonetworks.com/' },
  'LMT': { name: 'Lockheed Martin', url: 'https://www.lockheedmartin.com/' },
  'RTX': { name: 'RTX Corporation', url: 'https://www.rtx.com/' },
  'NOC': { name: 'Northrop Grumman', url: 'https://www.northropgrumman.com/' },
  'MSFT': { name: 'Microsoft Corporation', url: 'https://www.microsoft.com/' },
  'GOOGL': { name: 'Alphabet Inc.', url: 'https://abc.xyz/' },
  'AMZN': { name: 'Amazon.com Inc.', url: 'https://www.amazon.com/' },
  'META': { name: 'Meta Platforms', url: 'https://about.meta.com/' },
  'TSLA': { name: 'Tesla Inc.', url: 'https://www.tesla.com/' },
  'AAPL': { name: 'Apple Inc.', url: 'https://www.apple.com/' },
  'MRVL': { name: 'Marvell Technology', url: 'https://www.marvell.com/' },
  'TSM': { name: 'Taiwan Semiconductor', url: 'https://www.tsmc.com/' },
  'ASML': { name: 'ASML Holding', url: 'https://www.asml.com/' },
  'MU': { name: 'Micron Technology', url: 'https://www.micron.com/' },
  'FTNT': { name: 'Fortinet Inc.', url: 'https://www.fortinet.com/' },
  'ZS': { name: 'Zscaler Inc.', url: 'https://www.zscaler.com/' },
  'S': { name: 'SentinelOne Inc.', url: 'https://www.sentinelone.com/' },
  'CHKP': { name: 'Check Point Software', url: 'https://www.checkpoint.com/' },
  'CYBR': { name: 'CyberArk Software', url: 'https://www.cyberark.com/' },
  'TENB': { name: 'Tenable Holdings', url: 'https://www.tenable.com/' },
  'DDOG': { name: 'Datadog Inc.', url: 'https://www.datadoghq.com/' },
  'SNOW': { name: 'Snowflake Inc.', url: 'https://www.snowflake.com/' },
  'NOW': { name: 'ServiceNow Inc.', url: 'https://www.servicenow.com/' },
  'NET': { name: 'Cloudflare Inc.', url: 'https://www.cloudflare.com/' },
  'AI': { name: 'C3.ai Inc.', url: 'https://c3.ai/' },
  'GD': { name: 'General Dynamics', url: 'https://www.gd.com/' },
  'LHX': { name: 'L3Harris Technologies', url: 'https://www.l3harris.com/' },
  'KTOS': { name: 'Kratos Defense & Security', url: 'https://www.kratosdefense.com/' },
  'AVAV': { name: 'AeroVironment Inc.', url: 'https://www.avinc.com/' },
  'LUNR': { name: 'Intuitive Machines', url: 'https://www.intuitivemachines.com/' },
  'ASTS': { name: 'AST SpaceMobile', url: 'https://www.ast-science.com/' },
  'PL': { name: 'Planet Labs', url: 'https://www.planet.com/' },
  'AXON': { name: 'Axon Enterprise', url: 'https://www.axon.com/' },
  'CRWV': { name: 'CoreWeave Inc.', url: 'https://www.coreweave.com/' },
  'GE': { name: 'GE Aerospace', url: 'https://www.geaerospace.com/' },
  'RBRK': { name: 'Rubrik Inc.', url: 'https://www.rubrik.com/' },
  'NBIS': { name: 'Nebius Group', url: 'https://nebius.com/' },
  'IONQ': { name: 'IonQ Inc.', url: 'https://ionq.com/' },
  'QBTS': { name: 'D-Wave Quantum Inc.', url: 'https://www.dwavesys.com/' },
  'QUBT': { name: 'Quantum Computing Inc.', url: 'https://www.quantumcomputinginc.com/' },
  'RGTI': { name: 'Rigetti Computing Inc.', url: 'https://www.rigetti.com/' },
};

// === Load articles ===
function loadArticles() {
  const index = [];
  if (fs.existsSync(ARTICLES_DIR)) {
    const files = fs.readdirSync(ARTICLES_DIR).filter(f => f.endsWith('.json'));
    for (const file of files) {
      try {
        const article = JSON.parse(fs.readFileSync(path.join(ARTICLES_DIR, file), 'utf8'));
        index.push(article);
      } catch (e) { console.error(`Error reading ${file}:`, e.message); }
    }
  }
  return index.sort((a, b) => new Date(b.date) - new Date(a.date));
}

function formatDate(iso) {
  return new Date(iso).toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' });
}

function formatDateLong(iso) {
  return new Date(iso).toLocaleDateString('en-US', { weekday: 'long', month: 'long', day: 'numeric', year: 'numeric' });
}

function readMin(a) {
  return Math.max(1, Math.ceil((a.summary || '').split(' ').length / 200));
}

const TICKER_SYMBOLS = ['NVDA','PLTR','AVGO','AMD','GOOGL','META','MSFT','AMZN','TSLA','MU'];

function renderTickerTape(prices) {
  let items = '';
  const tickers = TICKER_SYMBOLS;
  for (let r = 0; r < 2; r++) {
    for (const sym of tickers) {
      const p = prices && prices[sym];
      if (!p || !p.price) continue;
      const prc = p.price.toFixed(2);
      const chg = p.changePercent;
      const cls = chg >= 0 ? 'up' : 'down';
      const chgStr = (chg >= 0 ? '+' : '') + chg.toFixed(2);
      items += `<span class="ticker-item"><span class="ticker-sym">${sym}</span><span class="ticker-prc">$${prc}</span><span class="ticker-chg ${cls}">${chgStr}%</span></span>`;
    }
  }
  if (!items) {
    for (let r = 0; r < 2; r++) {
      for (const sym of tickers) {
        items += `<span class="ticker-item"><span class="ticker-sym">${sym}</span><span class="ticker-prc">$---.--</span><span class="ticker-chg">0.00%</span></span>`;
      }
    }
  }
  return `<div class="ticker-tape"><div class="ticker-track">${items}</div></div>`;
}

function getYouTubeId(url) {
  const m = url.match(/(?:youtube\.com\/watch\?v=|youtu\.be\/|youtube\.com\/embed\/)([a-zA-Z0-9_-]+)/);
  return m ? m[1] : '';
}

function esc(s) {
  return String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;').replace(/'/g, '&#39;');
}

// Render image with WebP support, lazy loading, and CLS prevention
function renderImg(src, alt, cls, eager) {
  const webpSrc = src.replace(/\.(jpg|jpeg|png)$/i, '.webp');
  const lazyAttr = eager ? 'loading="eager"' : 'loading="lazy" decoding="async"';
  return '<picture>' +
    '<source srcset="' + esc(webpSrc) + '" type="image/webp">' +
    '<img src="' + esc(src) + '" alt="' + esc(alt) + '"' +
    (cls ? ' class="' + cls + '"' : '') +
    ' ' + lazyAttr + ' width="1200" height="675">' +
    '</picture>';
}

// === HTML rendering ===
function renderHeader(title, desc, article, allArticles, canonical) {
  let ogExtra = '';
  let ldJson = '';
  const canon = canonical ? canonical : article
    ? `https://readthesignal.net/article/${article.slug}`
    : 'https://readthesignal.net/';
  const canonTag = `  <link rel="canonical" href="${canon}">\n`;
  if (article) {
    const img = typeof article.image === 'object' ? article.image.src : article.image;
    const absImg = img ? (img.startsWith('http') ? img : 'https://readthesignal.net' + (img.startsWith('/') ? '' : '/') + img) : '';
    ogExtra = `<meta property="og:title" content="${esc(article.title)}">
    <meta property="og:description" content="${esc(article.summary)}">
    <meta property="og:type" content="article">
    <meta property="og:url" content="https://readthesignal.net/article/${article.slug}">
    ${img ? `<meta property="og:image" content="${absImg}"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="675">` : ''}
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="${esc(article.title)}">
    <meta name="twitter:description" content="${esc(article.summary)}">
    ${img ? `<meta name="twitter:image" content="${absImg}">` : ''}`;
    ldJson = `<script type="application/ld+json">
    {
      "@context": "https://schema.org",
      "@type": "NewsArticle",
      "headline": ${JSON.stringify(article.title)},
      "description": ${JSON.stringify(article.summary)},
      "datePublished": "${article.date}",
      "dateModified": "${article.date}",
      "mainEntityOfPage": {"@type":"WebPage","@id":"https://readthesignal.net/article/${article.slug}"},
      "author": {"@type":"Organization","name":"The Signal","url":"https://readthesignal.net"},
      "publisher": {"@type":"Organization","name":"The Signal","logo":{"@type":"ImageObject","url":"https://readthesignal.net/img/logo-hex.jpg","width":600,"height":60}},
      "image": ${JSON.stringify(img || 'https://readthesignal.net/img/logo-hex.jpg')},
      "thumbnailUrl": ${JSON.stringify(img || 'https://readthesignal.net/img/logo-hex.jpg')},
      "isAccessibleForFree": true,
      "wordCount": ${(article.bodyHtml || '').replace(/<[^>]+>/g, '').split(/\s+/).filter(Boolean).length},
      "keywords": ${JSON.stringify(article.tags.join(', '))},
      "articleSection": "${SECTORS[article.sector]?.name || article.sector}"
    }
    </script>
    <script type="application/ld+json">
    {
      "@context": "https://schema.org",
      "@type": "BreadcrumbList",
      "itemListElement": [{
        "@type": "ListItem",
        "position": 1,
        "name": "The Signal",
        "item": "https://readthesignal.net"
      },{
        "@type": "ListItem",
        "position": 2,
        "name": "${SECTORS[article.sector]?.name || article.sector}",
        "item": "https://readthesignal.net/sector/${article.sector}"
      },{
        "@type": "ListItem",
        "position": 3,
        "name": ${JSON.stringify(article.title)},
        "item": "https://readthesignal.net/article/${article.slug}"
      }]
    }
    </script>`;
  } else {
    // Homepage / section pages — Organization + WebSite schema
    ldJson = `<script type="application/ld+json">
    {
      "@context": "https://schema.org",
      "@type": "Organization",
      "name": "The Signal",
      "url": "https://readthesignal.net",
      "logo": {"@type":"ImageObject","url":"https://readthesignal.net/img/logo-hex.jpg","width":600,"height":60},
      "description": "Market intelligence for AI, defense, space, and cybersecurity stocks."
    }
    </script>
    <script type="application/ld+json">
    {
      "@context": "https://schema.org",
      "@type": "WebSite",
      "name": "The Signal",
      "url": "https://readthesignal.net",
      "potentialAction": {
        "@type": "SearchAction",
        "target": {
          "@type": "EntryPoint",
          "urlTemplate": "https://readthesignal.net/?q={search_term_string}"
        },
        "query-input": "required name=search_term_string"
      }
    }
    </script>`;
  }
  return `<!DOCTYPE html>\n<html lang="en">\n<head>\n  <meta charset="UTF-8">\n  <meta name="viewport" content="width=device-width, initial-scale=1.0">\n  <meta name="theme-color" content="#08080e">\n  ${canonTag}  <link rel="icon" type="image/x-icon" href="/favicon.ico">\n  <link rel="apple-touch-icon" sizes="180x180" href="/img/apple-touch-icon.png">\n  <meta name="robots" content="max-image-preview:large">\n  <link rel="preconnect" href="https://fonts.googleapis.com">\n  <link href="https://fonts.googleapis.com/css2?family=Anton&family=Inter:wght@400;500;600;700;800;900&family=JetBrains+Mono:wght@500;700&display=swap" rel="stylesheet">\n  <link rel="stylesheet" href="/css/main.css?v=8">
  <link rel="stylesheet" href="/css/pulse-badge.css">\n  <!-- Google tag (gtag.js) -->\n  <script async src="https://www.googletagmanager.com/gtag/js?id=G-98KDVDFBCW"></script>\n  <script>\n    window.dataLayer = window.dataLayer || [];\n    function gtag(){dataLayer.push(arguments);}\n    gtag('js', new Date());\n    gtag('config', 'G-98KDVDFBCW');\n  </script>\n  <script src="/js/prices.js" defer></script>\n  <script src="/js/search.js" defer></script>\n  <script src="/js/auth.js?v=2" defer></script>\n  <script src="/js/pulse.js" defer></script>\n  <script src="/js/theme.js" defer></script>\n  <script src="/js/comments.js" defer></script>\n  <script src="/js/share.js" defer></script>\n  <script src="/js/hive.js?v=2" defer></script>\n  <title>${esc(title)}</title>\n  <meta name="description" content="${esc(desc)}">\n  <meta property="og:title" content="${esc(title)}">\n  <meta property="og:description" content="${esc(desc)}">\n  ${ogExtra}${ldJson ? '\n  ' + ldJson : ''}\n</head>\n<body>\n  <nav class="nav">\n    <div class="nav-inner">\n      <a href="/" class="logo"><img src="/img/logo-hex.jpg" alt="The Signal" class="logo-img"><span class="logo-text"><span class="logo-the">THE</span> <strong>SIGNAL</strong></span></a>\n      <div class="nav-links">\n        <a href="/sector/ai" class="nav-link">AI</a>\n        <a href="/sector/cyber" class="nav-link">Cyber</a>\n        <a href="/sector/defense" class="nav-link">Defense</a>\n        <a href="/sector/space" class="nav-link">Space</a>\n        <a href="/sector/mega-cap" class="nav-link">Mega-Cap</a>\n        <a href="/sector/quantum" class="nav-link">Quantum</a>\n        <a href="/hive" class="nav-link">Hive</a>\n      </div>\n      <div class="nav-actions">\n        <button class="nav-btn search-btn" id="searchToggle" aria-label="Search">\n          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">\n            <circle cx="11" cy="11" r="8"></circle>\n            <line x1="21" y1="21" x2="16.65" y2="16.65"></line>\n          </svg>\n        </button>\n        <div class="auth-container" id="authContainer">\n            <button class="nav-btn auth-btn" id="authToggle" aria-label="Sign In">\n              <div class="auth-btn-avatar" id="authBtnAvatar">\n                <span class="auth-btn-initial" id="authBtnInitial"></span>\n                <img class="auth-btn-img" id="authBtnImg" src="" alt="" style="display:none">\n              </div>\n              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="auth-btn-icon" id="authBtnIcon">\n                <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path>\n                <circle cx="12" cy="7" r="4"></circle>\n              </svg>\n              <span class="auth-label" id="authLabel">Sign In</span>\n            </button>\n            <div class="auth-dropdown" id="authDropdown">\n              <div class="auth-profile" id="authProfile" style="display:none">\n                <div class="auth-profile-header">\n                  <div class="auth-profile-avatar" id="authProfileAvatar">\n                    <img id="authProfileImg" src="" alt="" style="display:none">\n                    <span class="auth-profile-initial" id="authProfileInitial"></span>\n                  </div>\n                  <div class="auth-profile-info">\n                    <span class="auth-profile-name" id="authProfileName"></span>\n                    <span class="auth-profile-username" id="authProfileUsername"></span>\n                  </div>\n                </div>\n                <div class="auth-profile-stats" id="authProfileStats">\n                  <div class="auth-stat">\n                    <span class="auth-stat-label">Portfolio</span>\n                    <span class="auth-stat-value" id="authStatValue">—</span>\n                  </div>\n                  <div class="auth-stat">\n                    <span class="auth-stat-label">Return</span>\n                    <span class="auth-stat-value" id="authStatReturn">—</span>\n                  </div>\n                </div>\n                <div class="auth-profile-links">\n                  <a href="/hive" class="auth-profile-link">🐝 My Hive</a>\n                  <a href="/hive" class="auth-profile-link" onclick="navigateToHiveLeaderboard(event)">🏆 Leaderboard</a>\n                </div>\n                <button class="auth-profile-signout" id="authSignOut">Sign Out</button>\n              </div>\n              <div class="auth-guest" id="authGuest">\n                <button class="auth-option" onclick="showHiveJoinModal(\'login\')" style="display:flex"><span class="auth-option-icon">🔑</span> Sign In</button>\n                <button class="auth-option" onclick="showHiveJoinModal(\'register\')" style="display:flex"><span class="auth-option-icon">✨</span> Create Account</button>\n              </div>\n            </div>\n        <button class="nav-btn hamburger-btn" id="hamburgerToggle" aria-label="Menu">\n          <span class="hamburger-line"></span>\n          <span class="hamburger-line"></span>\n          <span class="hamburger-line"></span>\n        </button>\n      ${article ? '<label class="theme-switch" id="themeSwitch" aria-label="Toggle theme"><input type="checkbox" id="themeToggleInput"><span class="theme-slider"><svg class="theme-switch-sun" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="5"></circle><line x1="12" y1="1" x2="12" y2="3"></line><line x1="12" y1="21" x2="12" y2="23"></line><line x1="4.22" y1="4.22" x2="5.64" y2="5.64"></line><line x1="18.36" y1="18.36" x2="19.78" y2="19.78"></line><line x1="1" y1="12" x2="3" y2="12"></line><line x1="21" y1="12" x2="23" y2="12"></line><line x1="4.22" y1="19.78" x2="5.64" y2="18.36"></line><line x1="18.36" y1="5.64" x2="19.78" y2="4.22"></line></svg><svg class="theme-switch-moon" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"></path></svg></span></label>' : ''}\n      </div>\n    </div>\n  </nav>\n  <div class="mobile-menu" id="mobileMenu">\n    <div class="mobile-menu-links">\n      <a href="/sector/ai" class="mobile-nav-link">AI</a>\n      <a href="/sector/cyber" class="mobile-nav-link">Cyber</a>\n      <a href="/sector/defense" class="mobile-nav-link">Defense</a>\n      <a href="/sector/space" class="mobile-nav-link">Space</a>\n      <a href="/sector/mega-cap" class="mobile-nav-link">Mega-Cap</a>\n      <a href="/sector/quantum" class="mobile-nav-link">Quantum</a>\n      <a href="/hive" class="mobile-nav-link">Hive</a>\n    </div>\n  </div>\n\n  <!-- Search Overlay -->\n  <div class="search-overlay" id="searchOverlay">\n    <div class="search-backdrop" id="searchBackdrop"></div>\n    <div class="search-modal">\n      <div class="search-header">\n        <input type="text" class="search-input" id="searchInput" placeholder="Search articles by title, ticker, sector, or tag…" autofocus>\n        <button class="search-close" id="searchClose" aria-label="Close search">\n          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">\n            <line x1="18" y1="6" x2="6" y2="18"></line>\n            <line x1="6" y1="6" x2="18" y2="18"></line>\n          </svg>\n        </button>\n      </div>\n      <div class="search-results" id="searchResults"></div>\n      <div class="search-empty" id="searchEmpty">Start typing to search articles…</div>\n    </div>\n  </div>\n\n  <script id="articles-data" type="application/json">${JSON.stringify(allArticles || [])}</script>\n  <main class="main">`;
}

function renderFooter() {
  return `  </main>
  <footer class="footer">
    <div class="footer-inner">
      <div class="footer-brand"><img src="/img/logo-hex.jpg" alt="The Signal" class="footer-logo"> THE <strong>SIGNAL</strong></div>
      <div class="footer-tag">The Signal Editorial Team · readthesignal.net</div>
      <div class="footer-copy">© ${new Date().getFullYear()} The Signal — Market Intelligence. Data from public sources.</div>
    </div>
  <script src="/js/prices.js" defer></script>
  <script src="/js/search.js" defer></script>
  <script src="/js/auth.js?v=2" defer></script>
  <script src="/js/pulse.js" defer></script>\n  <script src="/js/theme.js" defer></script>\n  <script src="/js/comments.js" defer></script>\n  <script src="/js/share.js" defer></script>\n  <script src="/js/hive.js?v=2" defer></script>
  <script>
  document.addEventListener('DOMContentLoaded', function(){
    var btn = document.getElementById('hamburgerToggle');
    var menu = document.getElementById('mobileMenu');
    if (btn && menu) {
      btn.addEventListener('click', function(){
        menu.classList.toggle('mobile-menu-open');
        btn.classList.toggle('hamburger-active');
      });
      document.addEventListener('click', function(e){
        if (!btn.contains(e.target) && !menu.contains(e.target)) {
          menu.classList.remove('mobile-menu-open');
          btn.classList.remove('hamburger-active');
        }
      });
    }
  });
  </script>
  <script>
  document.addEventListener('DOMContentLoaded', function(){
    var observer = new IntersectionObserver(function(entries){
      entries.forEach(function(e){
        if(e.isIntersecting){ e.target.classList.add('reveal'); observer.unobserve(e.target); }
      });
    }, { threshold: 0.15 });
    document.querySelectorAll('.sc-card, .detail-card-link, .sc-table-container, .newsletter-inner').forEach(function(el){ observer.observe(el); });
  });
  </script>
</html>`;
}

function renderCard(a, prices) {
  const sentLabel = a.sentiment === 'bullish' ? '▲ Bullish' : a.sentiment === 'bearish' ? '▼ Bearish' : '– Neutral';
  const img = typeof a.image === 'object' ? a.image : (a.image ? { src: a.image } : null);
  const imgHtml = img ? `<div class="card-image">${renderImg(img.src, a.title)}</div>` : '';
  const p = prices ? prices[a.ticker] : null;
  const priceHtml = p && p.price
    ? `<span class="price-chip ${p.changePercent >= 0 ? 'up' : 'down'}">$${p.price.toFixed(2)} <span>${(p.changePercent >= 0 ? '+' : '')}${p.changePercent.toFixed(2)}%</span></span>`
    : '';
  return `<a href="/article/${a.slug}" class="article-card">
    ${imgHtml}
    <div class="card-body">
    <div class="card-top">
      <span class="ticker-badge ${a.sentiment || 'neutral'}">${a.ticker}</span>
      ${priceHtml}
      <span class="sentiment-label ${a.sentiment || 'neutral'}">${sentLabel}</span>
    </div>
    <h3 class="card-title">${esc(a.title)}</h3>
    <p class="card-summary">${esc(a.summary.length > 200 ? a.summary.slice(0, 200) + '...' : a.summary)}</p>
    <div class="card-meta">
      <span>${formatDate(a.date)}</span>
      <span>${readMin(a)} min read</span>
    </div>
    </div>
  </a>`;
}

function renderFeatured(a) {
  const sentLabel = a.sentiment === 'bullish' ? '▲ Bullish' : a.sentiment === 'bearish' ? '▼ Bearish' : '– Neutral';
  const img = typeof a.image === 'object' ? a.image : (a.image ? { src: a.image } : null);
  const imgHtml = img ? `<div class="featured-image">${renderImg(img.src, a.title, null, true)}</div>` : '';
  return `<a href="/article/${a.slug}" class="featured-card">
    <div class="featured-content">
      <div class="featured-label">Featured Story</div>
      <div class="featured-ticker">
        <span class="ticker-badge ${a.sentiment || 'neutral'}">${a.ticker}</span>
        <span class="sentiment-label ${a.sentiment || 'neutral'}">${sentLabel}</span>
      </div>
      <h3 class="featured-title">${esc(a.title)}</h3>
      <p class="featured-summary">${esc(a.summary)}</p>
      <div class="featured-meta">
        <span>${formatDate(a.date)}</span>
        <span>${readMin(a)} min read</span>
      </div>
    </div>
    ${imgHtml}
  </a>`;
}

function renderSectorBadge(key, name) {
  const cssMap = {
    'ai': 'ai', 'cyber': 'cyber', 'defense': 'defense',
    'space': 'space', 'mega-cap': 'megacap'
  };
  const cssClass = cssMap[key] || 'ai';
  return `<a href="/sector/${key}" class="sector-badge ${cssClass}">${name.toUpperCase()}</a>`;
}

function renderVideoCard(v) {
  const vid = getYouTubeId(v.url);
  if (!vid) return '';
  return `<div class="video-section">
    <div class="video-section-title">▶ ${esc(v.source)}</div>
    <div class="video-embed">
      <iframe src="https://www.youtube.com/embed/${vid}" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen loading="lazy"></iframe>
    </div>
    <div class="video-info">
      <div class="video-info-title">${esc(v.title)}</div>
    </div>
  </div>`;
}

function cleanupBody(html) {
  // Strip literal \n text between HTML tags — subagents often write them
  var result = html.replace(/>\\n\\n</g, '><').replace(/>\\n</g, '><');
  // Also strip actual newline characters between tags (from JSON-escaped \n)
  result = result.replace(/>\n\n</g, '><').replace(/>\n</g, '><');
  return result;
}

function injectVideos(bodyHtml, videos) {
  let result = cleanupBody(bodyHtml);
  if (videos && videos.length) {
    for (let i = 0; i < videos.length; i++) {
      const marker = `<!-- VIDEO ${i} -->`;
      const card = renderVideoCard(videos[i]);
      if (card) result = result.replace(marker, card);
    }
  }
  return result;
}

// Build ticker → best article slug map for internal linking
function buildTickerLinkMap(articles) {
  var map = {};
  for (var i = 0; i < articles.length; i++) {
    var a = articles[i];
    if (a.ticker) {
      // Keep the most recent article for each ticker
      if (!map[a.ticker] || new Date(a.date) > new Date(map[a.ticker].date)) {
        map[a.ticker] = a;
      }
    }
  }
  return map;
}

// Inject inline links: replace $TICKER mentions with links to related articles
function injectInlineLinks(html, tickerLinkMap, currentSlug) {
  if (!tickerLinkMap) return html;
  var result = html;
  var linkedTickers = {};
  for (var ticker in tickerLinkMap) {
    if (!tickerLinkMap.hasOwnProperty(ticker)) continue;
    var target = tickerLinkMap[ticker];
    if (target.slug === currentSlug) continue;
    var regex = new RegExp('\\$' + ticker + '(?![^<]*</a>)', 'g');
    if (regex.test(result)) {
      linkedTickers[ticker] = target;
      result = result.replace(regex, '<a href="/article/' + target.slug + '">$' + ticker + '</a>');
    }
  }
  // Also inject a "Read more" box for the first linked ticker, if not already inside one
  var tickerKeys = Object.keys(linkedTickers);
  if (tickerKeys.length > 0) {
    var firstTicker = linkedTickers[tickerKeys[0]];
    var readMoreBox = '<div class="related-inline"><strong>📖 Read more:</strong> <a href="/article/' + firstTicker.slug + '">' + esc(firstTicker.title) + '</a></div>';
    // Insert after the first <h2> in the article (natural break point)
    result = result.replace('<h2>', readMoreBox + '\n<h2>');
  }
  return result;
}

function renderPulse() {
  return `<section class="pulse-section" id="pulseSection">
    <div class="pulse-header">
      <img src="/img/logo-hex.jpg" alt="Pulse" class="pulse-avatar">
      <div class="pulse-header-text">
        <h2 class="pulse-title">Ask <span class="pulse-gradient">Pulse</span></h2>
        <p class="pulse-desc">Your AI research agent — ask about real-time market data, earnings, contracts, or any covered stock. Pulse searches the web to get you answers that go beyond our articles.</p>
      </div>
    </div>
    <div class="pulse-chat" id="pulseChat">
      <div class="pulse-messages" id="pulseMessages">
        <div class="pulse-message pulse-message-bot">
          <img src="/img/logo-hex.jpg" alt="Pulse" class="pulse-message-avatar">
          <div class="pulse-bubble">Hey, I'm <strong>Pulse</strong>. Ask me anything — earnings data, stock analysis, market moves, or company filings. I search the web for real-time info.</div>
        </div>
      </div>
      <div class="pulse-input-area">
        <input type="text" class="pulse-input" id="pulseInput" placeholder="e.g. What were Nvidia's latest earnings?">
        <button class="pulse-send" id="pulseSend" aria-label="Send">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <line x1="22" y1="2" x2="11" y2="13"></line>
            <polygon points="22 2 15 22 11 13 2 9 22 2"></polygon>
          </svg>
        </button>
      </div>
    </div>
  </section>`;
}


function renderScorecard(prices) {
  var sc;
  try { sc = JSON.parse(fs.readFileSync(path.join(DATA_DIR, 'scorecard.json'), 'utf8')); } catch(e) { return ''; }
  if (!sc || !sc.length) return '';
  var svgW = 100, svgH = 48, cx = svgW / 2, cy = svgH - 2, r = 40;
  var circ = Math.PI * r;
  var cards = '';
  for (var i = 0; i < sc.length; i++) {
    var s = sc[i];
    var offset = circ - (s.score / 100) * circ;
    var angle = (s.score / 100) * 180 - 90;
    var tipX = cx, tipY = cy - 38;
    var drivers = '';
    for (var j = 0; j < (s.drivers || []).length; j++) {
      drivers += '<div class="sc-driver"><span class="sc-dot" style="background:' + s.color + '"></span>' + esc(s.drivers[j]) + '</div>';
    }
    var signalLabel = esc(s.signal).toUpperCase() + ' SIGNAL ' + s.score;
    cards += '<div class="sc-card" data-sc-idx="' + i + '">' +
      '<div class="sc-card-header">' +
        '<img class="sc-logo" src="' + esc(s.logo) + '" alt="' + esc(s.ticker) + '" onerror="this.style.display=' + "'none'" + '" crossorigin="anonymous">' +
        '<div class="sc-card-info">' +
          '<div class="sc-card-name">' + esc(s.ticker) + '</div>' +
          '<div class="sc-card-sub">' + esc(s.name) + '</div>' +
        '</div>' +
      '</div>' +
      '<div class="sc-gauge-wrap">' +
        '<svg width="' + svgW + '" height="' + svgH + '" viewBox="0 0 ' + svgW + ' ' + svgH + '" class="sc-gauge-svg">' +
          '<defs>' +
            '<filter id="glow-' + s.ticker + '"><feGaussianBlur stdDeviation="3" result="coloredBlur"/><feMerge><feMergeNode in="coloredBlur"/><feMergeNode in="SourceGraphic"/></feMerge></filter>' +
            '<filter id="arcglow-' + s.ticker + '"><feGaussianBlur stdDeviation="2" result="blur"/><feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge></filter>' +
          '</defs>' +
          '<path d="M ' + (cx - r) + ' ' + cy + ' A ' + r + ' ' + r + ' 0 0 1 ' + (cx + r) + ' ' + cy + '" fill="none" stroke="#1e293b" stroke-width="8" stroke-linecap="round"/>' +
          '<path d="M ' + (cx - r) + ' ' + cy + ' A ' + r + ' ' + r + ' 0 0 1 ' + (cx + r) + ' ' + cy + '" fill="none" stroke="' + s.color + '" stroke-width="8" stroke-linecap="round" stroke-dasharray="' + circ + '" stroke-dashoffset="' + offset + '" filter="url(#arcglow-' + s.ticker + ')"/>' +
          '<polygon points="' + (cx - 4) + ',' + (cy - 2) + ' ' + (cx + 4) + ',' + (cy - 2) + ' ' + tipX + ',' + tipY + '" fill="' + s.color + '" stroke="rgba(255,255,255,0.3)" stroke-width="0.5" transform="rotate(' + angle + ', ' + cx + ', ' + cy + ')" filter="url(#glow-' + s.ticker + ')"/>' +
        '</svg>' +
      '</div>' +
      '<div class="sc-signal-label" style="color:' + s.color + '">' + signalLabel + '</div>' +
      '<div class="sc-drivers">' + drivers + '</div>' +
    '</div>';
  }
  var tickers = [];
  for (var i = 0; i < sc.length; i++) {
    tickers.push(sc[i]);
  }
  var metricRows = '';
  var metricDefs = [
    { label: 'Revenue (TTM)', key: 'revenue', cls: '' },
    { label: 'Rev Growth (YoY)', key: 'growth', cls: 'positive' },
    { label: 'Net Income', key: 'netIncome', cls: '' },
    { label: 'P/E Ratio', key: 'pe', cls: '' },
    { label: 'Price/Sales', key: 'ps', cls: '' },
    { label: 'Target Upside', key: 'upside', cls: 'positive' }
  ];
  for (var m = 0; m < metricDefs.length; m++) {
    var def = metricDefs[m];
    var row = '<tr><td class="metric-label">' + def.label + '</td>';
    for (var t = 0; t < tickers.length; t++) {
      var s = tickers[t];
      var val = '---';
      if (def.key === 'upside') {
        val = s.upside || (s.metrics ? s.metrics[def.key] : null) || '---';
      } else if (s.metrics) {
        val = s.metrics[def.key] || '---';
      }
      row += '<td' + (def.cls ? ' class="' + def.cls + '"' : '') + '>' + esc(val) + '</td>';
    }
    row += '</tr>';
    metricRows += row;
  }
  var thRow = '<tr><th>Metric</th>';
  for (var t = 0; t < tickers.length; t++) {
    thRow += '<th>' + esc(tickers[t].ticker) + '</th>';
  }
  thRow += '</tr>';
  return '<div class="section-divider"></div>' +
    '<section class="scorecard-section">' +
    '<div class="scorecard-inner">' +
      '<div class="scorecard-header-top">' +
        '<img class="sc-header-logo" src="/img/logo-hex.jpg" alt="The Signal">' +
        '<h2 class="scorecard-title">Signal <span>Scorecard</span></h2>' +
      '</div>' +
      '<p class="scorecard-subtitle">High-signal intelligence powered by our proprietary AI engine</p>' +
      '<div class="scorecard-grid" id="scorecardGrid">' + cards + '</div>' +
      '<div class="sc-table-container">' +
        '<div class="sc-table-header"><h3><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="vertical-align:middle;margin-right:6px"><rect x="3" y="12" width="4" height="8"/><rect x="10" y="6" width="4" height="14"/><rect x="17" y="2" width="4" height="18"/></svg>Key Metrics (TTM)</h3></div>' +
        '<div class="sc-table-scroll">' +
          '<table class="sc-table">' +
            '<thead>' + thRow + '</thead>' +
            '<tbody>' + metricRows + '</tbody>' +
          '</table>' +
        '</div>' +
      '</div>' +
    '</div>' +
  '</section>';
}

function renderSignalHighlights(prices) {
  var hl;
  try { hl = JSON.parse(fs.readFileSync(path.join(DATA_DIR, 'highlights.json'), 'utf8')); } catch(e) { hl = null; }
  if (!hl || !hl.length) {
    // Fallback: render nothing if no data
    return '';
  }
  function card(ticker, name, fairVal, upsidePct, rev, growth, ni, consensus, target, buyPct) {
    var p = prices && prices[ticker];
    var price = p && p.price ? '$' + p.price.toFixed(2) : '$---';
    var cls = p && p.changePercent >= 0 ? 'up' : 'down';
    var chg = p && p.changePercent ? ((p.changePercent >= 0 ? '+' : '') + p.changePercent.toFixed(2) + '%') : '0.00%';
    var holdPct = 100 - buyPct;
    var upArrow = upsidePct && upsidePct.indexOf('-') !== 0 ? 'detail-fv-upside' : '';
    return '<a href="/ticker/' + ticker + '" class="detail-card-link">' +
      '<div class="detail-card-accent"></div>' +
      '<div class="detail-card-inner">' +
        '<div class="detail-header">' +
          '<div class="detail-header-left">' +
            '<div class="detail-badge">Signal Highlight</div>' +
            '<div class="detail-ticker">' + ticker + '</div>' +
            '<div class="detail-name">' + esc(name) + '</div>' +
          '</div>' +
          '<div class="detail-header-right">' +
            '<div class="detail-price">' + price + '</div>' +
            '<div class="detail-change ' + cls + '">' + chg + '</div>' +
          '</div>' +
        '</div>' +
        '<div class="detail-card-section">' +
          '<div class="detail-section-title">Fair Value</div>' +
          '<div class="detail-fair-value">' +
            '<div class="detail-fv-status"><span class="detail-fv-badge">Undervalued</span></div>' +
            '<div class="detail-fv-rows">' +
              '<div class="detail-fv-row"><span class="detail-fv-label">Fair Value</span><span class="detail-fv-val">$' + fairVal + '</span></div>' +
              '<div class="detail-fv-row"><span class="detail-fv-label">Current Price</span><span class="detail-fv-val">' + price + '</span></div>' +
              '<div class="detail-fv-row"><span class="detail-fv-label">Upside</span><span class="detail-fv-val ' + upArrow + '">' + upsidePct + '</span></div>' +
            '</div>' +
          '</div>' +
        '</div>' +
        '<div class="detail-card-section">' +
          '<div class="detail-section-title">Earnings</div>' +
          '<div class="detail-earnings">' +
            '<div class="detail-earn-row"><span class="detail-earn-label">Revenue (TTM)</span><span class="detail-earn-val">' + rev + '</span></div>' +
            '<div class="detail-earn-row"><span class="detail-earn-label">Revenue Growth</span><span class="detail-earn-val detail-revision-up">' + growth + '</span></div>' +
            '<div class="detail-earn-row"><span class="detail-earn-label">Net Income</span><span class="detail-earn-val">' + ni + '</span></div>' +
          '</div>' +
        '</div>' +
        '<div class="detail-card-section detail-section-last">' +
          '<div class="detail-section-title">Analyst Ratings</div>' +
          '<div class="detail-analyst">' +
            '<div class="detail-ana-top">' +
              '<span class="detail-consensus-badge">' + consensus + '</span>' +
              '<span class="detail-ana-target">Target <strong>$' + target + '</strong></span>' +
            '</div>' +
            '<div class="detail-rating-bar">' +
              '<div class="detail-rating-seg detail-rating-buy" style="width:' + buyPct + '%"></div>' +
              '<div class="detail-rating-seg detail-rating-hold" style="width:' + holdPct + '%"></div>' +
            '</div>' +
            '<div class="detail-rating-legend">' +
              '<span class="detail-legend-item"><span class="detail-rating-dot detail-dot-buy"></span>Buy</span>' +
              '<span class="detail-legend-item"><span class="detail-rating-dot detail-dot-hold"></span>Hold</span>' +
            '</div>' +
          '</div>' +
        '</div>' +
      '</div>' +
    '</a>';
  }
  var cards = '';
  for (var i = 0; i < hl.length; i++) {
    var h = hl[i];
    if (!h || !h.ticker || !h.analyst) continue;
    var total = (h.analyst.buys || 0) + (h.analyst.holds || 0) + (h.analyst.sells || 0);
    var buyPct = total > 0 ? Math.round((h.analyst.buys || 0) / total * 100) : 50;
    var upsideStr = h.fairValue && h.fairValue.upside ? h.fairValue.upside.replace('+', '') : '0%';
    var targetStr = h.analyst && h.analyst.target ? h.analyst.target.toFixed(2) : '0';
    var fairValStr = h.fairValue && h.fairValue.price ? h.fairValue.price.toFixed(2) : '0.00';
    cards += card(
      h.ticker,
      h.name || h.ticker,
      fairValStr,
      upsideStr,
      h.earnings && h.earnings.revTtm || 'N/A',
      h.earnings && h.earnings.revGrowth || 'N/A',
      h.earnings && h.earnings.netIncome || 'N/A',
      h.analyst.consensus || 'N/A',
      targetStr,
      buyPct
    );
  }
  if (!cards) return '';
  return '<div class="section-divider"></div>' +
    '<section class="detail-stocks-section">' +
    '<div class="detail-stocks-header"><span class="detail-star">*</span> Signal Highlights</div>' +
    '<div class="detail-stocks-grid">' + cards + '</div>' +
  '</section>';
}

function renderNewsletter() {
  return '<div class="section-divider"></div>' +
    '<section class="newsletter-section" id="subscribe">' +
    '<div class="newsletter-inner">' +
      '<div class="newsletter-badge">Early Access</div>' +
      '<h2 class="newsletter-title">Get the <span class="newsletter-gradient">Signal</span> in your inbox</h2>' +
      '<p class="newsletter-desc">Weekly stock intelligence on AI, defense, space &amp; cyber. No spam. Unsubscribe anytime.</p>' +
      '<form class="newsletter-form" id="newsletterForm">' +
        '<input type="email" class="newsletter-input" id="newsletterEmail" placeholder="your@email.com" required autocomplete="email">' +
        '<button type="submit" class="newsletter-btn">Subscribe</button>' +
      '</form>' +
      '<p class="newsletter-status" id="newsletterStatus"></p>' +
    '</div>' +
  '</section>';
}

function renderHiveHome() {
  return '<div class="section-divider"></div>' +
    '<section class="hive-home-section" id="hiveHomeSection">' +
    '<div class="hive-home-inner">' +
      '<div class="hive-home-header">' +
        '<div class="hive-home-title">🐝 The Hive</div>' +
        '<a href="/hive" class="hive-home-cta">Enter The Hive →</a>' +
      '</div>' +
      '<div class="hive-home-grid">' +
        '<div class="hive-home-card">' +
          '<div class="hive-home-card-title">Signal Master Spotlight</div>' +
          '<div class="hive-spotlight-holdings">' +
            '<div class="hive-loading"><div class="hive-spinner"></div><span>Loading...</span></div>' +
          '</div>' +
        '</div>' +
        '<div class="hive-home-card">' +
          '<div class="hive-home-card-title">Leaderboard Top 5</div>' +
          '<div class="hive-preview-entries">' +
            '<div class="hive-loading"><div class="hive-spinner"></div><span>Loading...</span></div>' +
          '</div>' +
        '</div>' +
      '</div>' +
    '</div>' +
  '</section>';
}

// === Build pages ===
function buildHome(articles, prices) {
  const ticker = renderTickerTape(prices);
  const hero = `<section class="hero">
    <div class="hero-video-bg">
      <video autoplay muted loop playsinline src="/img/hero-bg.mp4" style="position:absolute;top:0;left:0;width:100%;height:100%;object-fit:cover;opacity:0.55;pointer-events:none;"></video>
    </div>
    <div class="hero-content">
      <div class="hero-badge">
        <span class="hero-badge-dot"></span>
        Live Market Intelligence
      </div>
      <h1 class="hero-title">Read the <span class="hero-gradient">signal</span> before the market moves</h1>
      <p class="hero-sub">Deep-dive analysis on the stocks shaping the future — AI, defense, space, cybersecurity, and the mega-cap giants that connect them all.</p>
      <p class="hero-desc">The Signal delivers sharp analysis on the stocks shaping tomorrow — AI, defense, space, cybersecurity, and the mega-cap movers that connect them all. Earnings deep-dives, contract analysis, and market-moving insights. No fluff, no noise — just what matters for your portfolio.</p>
    </div>
  </section>
  <div class="focus-bar">
    <a href="/sector/ai" class="focus-item focus-ai">AI</a>
    <span class="focus-divider">·</span>
    <a href="/sector/cyber" class="focus-item focus-cyber">Cyber</a>
    <span class="focus-divider">·</span>
    <a href="/sector/defense" class="focus-item focus-defense">Defense</a>
    <span class="focus-divider">·</span>
    <a href="/sector/space" class="focus-item focus-space">Space</a>
    <span class="focus-divider">·</span>
    <a href="/sector/mega-cap" class="focus-item focus-mega">Mega-Cap</a>
  </div>`;
  const hasFeatured = articles.length > 0;
  const featured = hasFeatured ? renderFeatured(articles[0]) : '';
  const gridFirst4 = hasFeatured && articles.length > 1
    ? `<div class="article-grid">${articles.slice(1, 5).map(a => renderCard(a, prices)).join('\n      ')}</div>`
    : '';
  const gridRest = hasFeatured && articles.length > 5
    ? `<section class="feed feed-continued"><div class="article-grid">${articles.slice(5, 9).map(a => renderCard(a, prices)).join('\n      ')}</div></section>`
    : '';
  const gridRemaining = hasFeatured && articles.length > 9
    ? `<div class="section-divider"></div><section class="feed feed-continued"><div class="article-grid">${articles.slice(9).map(a => renderCard(a, prices)).join('\n      ')}</div></section>`
    : '';
  const pulse = renderPulse();

  const feed = `<section class="feed">
    <div class="feed-header">
      <h2 class="feed-title"><span class="dot"></span> Live Feed</h2>
      <div class="feed-sectors">
        ${Object.keys(SECTORS).map(s => renderSectorBadge(s, SECTORS[s].name)).join('\n        ')}
      </div>
    </div>
    ${hasFeatured ? featured : ''}
    ${hasFeatured ? pulse : ''}
    ${gridFirst4}
  </section>`;

  const html = renderHeader('The Signal — Market Intelligence for AI, Defense, Space & Cyber',
    'The Signal delivers sharp analysis on AI, defense, space, and cybersecurity stocks. Earnings deep-dives, contract analysis, and market-moving insights.',
    null, articles)
    + ticker + hero + feed + renderScorecard(prices) + gridRest + renderSignalHighlights(prices) + renderHiveHome() + renderNewsletter() + gridRemaining + renderFooter();
  fs.mkdirSync(DIST, { recursive: true });
  fs.writeFileSync(path.join(DIST, 'index.html'), html);
  console.log('  ✓ index.html');
}

function buildHive() {
  const body = '<div class="hive-app">' +
    '<div class="hive-header-area">' +
      '<div>' +
        '<div class="hive-header-title"><span class="hive-header-icon">🐝</span> The Hive</div>' +
        '<div class="hive-header-sub">Simulated trading &amp; portfolio leaderboard for The Signal community</div>' +
      '</div>' +
    '</div>' +
    '<div class="hive-auth-bar" id="hiveAuthSection">' +
      '<div id="authOptions">' +
        '<button class="hive-cta-btn" onclick="showHiveJoinModal(\'login\')" style="font-size:12px;padding:6px 14px">Sign In</button>' +
        '<button class="hive-cta-btn hive-cta-sm" onclick="showHiveJoinModal(\'register\')" style="font-size:12px;padding:6px 14px;background:transparent;border:1px solid var(--border);color:var(--text-secondary)">Register</button>' +
      '</div>' +
      '<div id="authUserInfo" style="display:none;align-items:center;gap:8px">' +
        '<span id="authName" class="hive-auth-name"></span>' +
        '<button class="hive-cta-btn" onclick="hiveLogout()" style="font-size:11px;padding:4px 12px;background:transparent;border:1px solid var(--border);color:var(--text-muted)">Sign Out</button>' +
      '</div>' +
    '</div>' +
    '<div class="hive-tabs" id="hiveTabs">' +
      '<button class="hive-tab hive-tab-active" data-tab="portfolio">Portfolio</button>' +
      '<button class="hive-tab" data-tab="leaderboard">Leaderboard</button>' +
      '<button class="hive-tab" data-tab="signalmaster">Signal Master</button>' +
      '<button class="hive-tab" data-tab="stocks">Stocks</button>' +
      '<button class="hive-tab" data-tab="rules">Rules</button>' +
    '</div>' +
    '<div id="hiveTabPortfolio" class="hive-tab-content hive-tab-active">' +
      '<div id="hivePortfolioContent">' +
        '<div class="hive-loading"><div class="hive-spinner"></div><span>Loading portfolio...</span></div>' +
      '</div>' +
    '</div>' +
    '<div id="hiveTabLeaderboard" class="hive-tab-content">' +
      '<div class="hive-lb-periods">' +
        '<button class="hive-lb-period-btn" data-period="weekly">Weekly</button>' +
        '<button class="hive-lb-period-btn hive-lb-period-active" data-period="monthly">30 Day</button>' +
        '<button class="hive-lb-period-btn" data-period="alltime">All-Time</button>' +
      '</div>' +
      '<div id="hiveLeaderboardContent">' +
        '<div class="hive-loading"><div class="hive-spinner"></div><span>Loading leaderboard...</span></div>' +
      '</div>' +
    '</div>' +
    '<div id="hiveTabSignalmaster" class="hive-tab-content">' +
      '<div id="hiveSignalMasterContent">' +
        '<div class="hive-loading"><div class="hive-spinner"></div><span>Loading Signal Master...</span></div>' +
      '</div>' +
    '</div>' +
    '<div id="hiveTabStocks" class="hive-tab-content">' +
      '<div id="hiveStocksContent">' +
        '<div class="hive-loading"><div class="hive-spinner"></div><span>Loading stocks...</span></div>' +
      '</div>' +
    '</div>' +
    '<div id="hiveTabRules" class="hive-tab-content">' +
      '<div id="hiveRulesContent"></div>' +
    '</div>' +
  '</div>';

  const html = renderHeader('The Hive — Simulated Trading & Portfolio Leaderboard — The Signal',
    'Join The Hive at The Signal. Get a $100,000 simulated portfolio to trade AI, defense, space, cyber, mega-cap, and quantum stocks. Compete on the leaderboard.',
    null, null, 'https://readthesignal.net/hive')
    + body + renderFooter();
  const dir = path.join(DIST, 'hive');
  fs.mkdirSync(dir, { recursive: true });
  fs.writeFileSync(path.join(dir, 'index.html'), html);
  console.log('  ✓ hive/index.html');
}

function buildArticle(article, allArticles) {
  const sentLabel = article.sentiment === 'bullish' ? '▲ Bullish' : article.sentiment === 'bearish' ? '▼ Bearish' : '– Neutral';
  const img = typeof article.image === 'object' ? article.image : (article.image ? { src: article.image } : null);
  const info = COMPANY_INFO[article.ticker] || {};
  const linksHtml = article.links && article.links.length
    ? `<div class="article-links"><h4>🔗 Learn More</h4><ul>${article.links.map(l => `<li><a href="${esc(l.url)}" target="_blank" rel="noopener">${esc(l.label)}</a></li>`).join('\n          ')}</ul></div>`
    : '';
  const tickerLinkMap = buildTickerLinkMap(allArticles || []);
  const bodyHtml = injectInlineLinks(injectVideos(article.bodyHtml || '', article.videos), tickerLinkMap, article.slug);

  // Build related articles
  let relatedHtml = '';
  if (allArticles && allArticles.length > 1) {
    const related = allArticles.filter(function(a) {
      if (a.slug === article.slug) return false;
      var sameSector = a.sector === article.sector;
      var sameTicker = a.ticker === article.ticker;
      var tagOverlap = false;
      if (article.tags && a.tags) {
        for (var i = 0; i < article.tags.length; i++) {
          if (a.tags.indexOf(article.tags[i]) !== -1) { tagOverlap = true; break; }
        }
      }
      return sameSector || sameTicker || tagOverlap;
    }).slice(0, 4);
    if (related.length > 0) {
      relatedHtml = `\n  <section class="related-articles">
    <h3 class="related-title">Related Articles</h3>
    <div class="related-grid">
      ${related.map(function(a) {
        const relImg = typeof a.image === 'object' ? a.image : (a.image ? { src: a.image } : null);
        return `<a href="/article/${a.slug}" class="related-card">
        ${relImg ? `<div class="related-card-image">${renderImg(relImg.src, a.title)}</div>` : ''}
        <div class="related-card-body">
          <span class="ticker-badge ${a.sentiment || 'neutral'}">${a.ticker}</span>
          <h4 class="related-card-title">${esc(a.title.length > 80 ? a.title.slice(0, 80) + '…' : a.title)}</h4>
          <span class="related-card-date">${formatDate(a.date)}</span>
        </div>
      </a>`;
      }).join('\n      ')}
    </div>
  </section>`;
    }
  }

  // Build Giscus comments
  const giscusHtml = `\n  <section class="article-comments">
    <h3 class="comments-title">Discussion</h3>
    <p class="comments-intro">Comments powered by Giscus — sign in with GitHub to join the discussion.</p>
    <div class="giscus-container">
      <script src="https://giscus.app/client.js"
        data-repo="[ENTER REPO HERE]"
        data-repo-id="[ENTER REPO ID HERE]"
        data-category="Announcements"
        data-category-id="[ENTER CATEGORY ID HERE]"
        data-mapping="specific"
        data-term="${article.slug}"
        data-strict="0"
        data-reactions-enabled="1"
        data-emit-metadata="0"
        data-input-position="top"
        data-theme="dark"
        data-lang="en"
        crossorigin="anonymous"
        async>
      </script>
    </div>
  </section>`;

  const body = `<article class="article-page">
    <div class="article-header">
      <div class="article-breadcrumbs">
        <a href="/">Home</a> / <a href="/sector/${article.sector}">${SECTORS[article.sector]?.name || article.sector.toUpperCase()}</a> / <span>${article.ticker}</span>
      </div>
      <div class="article-ticker-bar">
        <span class="ticker-badge large ${article.sentiment || 'neutral'}">${article.ticker}</span>
        <span class="sentiment-label large ${article.sentiment || 'neutral'}">${sentLabel}</span>
      </div>
      <h1 class="article-title">${esc(article.title)}</h1>
      ${article.subtitle ? `<p class="article-subtitle">${esc(article.subtitle)}</p>` : ''}
      <div class="article-meta">
        <span class="article-date">${formatDateLong(article.date)}</span>
        <span class="article-source">The Signal</span>
      </div>
    </div>
    ${img ? `<div class="article-image">${renderImg(img.src, article.title)}</div>` : ''}
    <div class="article-body">
      ${bodyHtml}
    </div>
    <div class="article-footer">
      <div class="article-tags">
        <span class="tag">$${article.ticker}</span>
        <span class="tag">${SECTORS[article.sector]?.name || article.sector}</span>
        ${(article.tags || []).map(t => `<span class="tag">${esc(t)}</span>`).join('\n        ')}
      </div>
      ${linksHtml}
    </div>
  </article>
  ${relatedHtml}
  ${giscusHtml}`;

  const html = renderHeader(article.title + ' — The Signal', article.summary, article, allArticles) + body + renderFooter();
  const dir = path.join(DIST, 'article', article.slug);
  fs.mkdirSync(dir, { recursive: true });
  fs.writeFileSync(path.join(dir, 'index.html'), html);
  console.log(`  ✓ article/${article.slug}/`);
}

function buildTicker(symbol, articles, prices) {
  const info = COMPANY_INFO[symbol] || {};
  const body = `<section class="ticker-page">
    <div class="ticker-hero">
      <div class="ticker-hero-left">
        <h1 class="ticker-symbol">$${symbol}</h1>
        <div class="ticker-price-block"><span class="price-missing">Price data refreshes at market open</span></div>
        ${info.url ? `<a href="${esc(info.url)}" target="_blank" rel="noopener" class="company-link">Visit Company Website →</a>` : ''}
      </div>
      <div class="ticker-hero-right">
        <span class="article-count">${articles.length} article${articles.length !== 1 ? 's' : ''}</span>
      </div>
    </div>
    <div class="article-grid">
      ${articles.length ? articles.map(a => renderCard(a, prices)).join('\n      ') : '<div class="empty-state">No articles yet for $' + symbol + '. Check back soon.</div>'}
    </div>
  </section>`;
  const html = renderHeader(symbol + ' Stock Analysis — The Signal',
    `Latest analysis for ${info.name || symbol} (${symbol}). Articles, earnings, and market intelligence.`,
    null, null, `https://readthesignal.net/ticker/${symbol}`)
    + body + renderFooter();
  const dir = path.join(DIST, 'ticker', symbol);
  fs.mkdirSync(dir, { recursive: true });
  fs.writeFileSync(path.join(dir, 'index.html'), html);
  console.log(`  ✓ ticker/${symbol}/`);
}

function buildSector(key, sec, articles, prices) {
  const pricesHtml = sec.tickers.map(t => {
    const info = COMPANY_INFO[t];
    return `<a href="/ticker/${t}" class="mini-price-card">
      <span class="mini-symbol">${t}</span>
      <span class="mini-change">${info ? '↗' : '–'}</span>
    </a>`;
  }).join('\n      ');
  const body = `<section class="sector-page">
    <div class="sector-header">
      <h1 class="sector-title">${sec.name}</h1>
      <div class="sector-tickers">
        ${sec.tickers.map(t => `<a href="/ticker/${t}" class="mini-ticker">${t}</a>`).join('\n        ')}
      </div>
    </div>
    <div class="sector-prices">
      ${pricesHtml}
    </div>
    <div class="article-grid">
      ${articles.length ? articles.map(a => renderCard(a, prices)).join('\n      ') : '<div class="empty-state">No articles yet in this sector.</div>'}
    </div>
  </section>`;
  const html = renderHeader(`${sec.name} Stocks — The Signal`,
    `Latest analysis of ${sec.name.toLowerCase()} stocks including ${sec.tickers.slice(0, 5).join(', ')}.`,
    null, null, `https://readthesignal.net/sector/${key}`)
    + body + renderFooter();
  const dir = path.join(DIST, 'sector', key);
  fs.mkdirSync(dir, { recursive: true });
  fs.writeFileSync(path.join(dir, 'index.html'), html);
  console.log(`  ✓ sector/${key}/`);
}

function buildSitemap(articles) {
  let xml = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n';
  xml += '  <url><loc>https://readthesignal.net/</loc><priority>1.0</priority></url>\n';
  for (const a of articles) {
    xml += `  <url><loc>https://readthesignal.net/article/${a.slug}</loc><lastmod>${a.date.split('T')[0]}</lastmod><priority>0.9</priority></url>\n`;
  }
  for (const key of Object.keys(SECTORS)) {
    xml += `  <url><loc>https://readthesignal.net/sector/${key}</loc><priority>0.7</priority></url>\n`;
  }
  const tickers = new Set(articles.map(a => a.ticker));
  for (const t of tickers) {
    xml += `  <url><loc>https://readthesignal.net/ticker/${t}</loc><priority>0.6</priority></url>\n`;
  }
  xml += '</urlset>';
  fs.writeFileSync(path.join(DIST, 'sitemap.xml'), xml);
  console.log('  ✓ sitemap.xml');
}

function buildRSS(articles) {
  let rss = `<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
<channel>
  <title>The Signal — Market Intelligence</title>
  <link>https://readthesignal.net/</link>
  <description>AI, defense, space &amp; cyber stock analysis</description>
  <atom:link href="https://readthesignal.net/rss" rel="self" type="application/rss+xml"/>`;
  for (const a of articles.slice(0, 50)) {
    rss += `
  <item>
    <title><![CDATA[${a.title}]]></title>
    <link>https://readthesignal.net/article/${a.slug}</link>
    <description><![CDATA[${a.summary}]]></description>
    <pubDate>${new Date(a.date).toUTCString()}</pubDate>
    <guid>https://readthesignal.net/article/${a.slug}</guid>
  </item>`;
  }
  rss += '\n</channel>\n</rss>';
  fs.writeFileSync(path.join(DIST, 'rss.xml'), rss);
  console.log('  ✓ rss.xml');
}

// === Write articles.json for price fetcher ===
function writeArticlesJson(articles) {
  const out = articles.map(a => ({
    slug: a.slug,
    title: a.title,
    summary: a.summary,
    ticker: a.ticker,
    sector: a.sector,
    sentiment: a.sentiment,
    date: a.date,
    image: typeof a.image === 'object' ? a.image.src : a.image
  }));
  fs.writeFileSync(path.join(DIST, 'data', 'articles.json'), JSON.stringify(out, null, 2));
  console.log('  ✓ articles.json (for price fetcher)');
}

// === Entry point ===
console.log('🏗️  Building The Signal...');
const articles = loadArticles();
console.log(`   Loaded ${articles.length} articles`);

// Load prices
let prices = {};
try {
  prices = JSON.parse(fs.readFileSync(path.join(DATA_DIR, 'prices.json'), 'utf8'));
  console.log(`   Loaded prices for ${Object.keys(prices).length} tickers`);
} catch (e) {
  console.log('   No price data found — using ticker defaults');
}

// Copy static assets
if (fs.existsSync(DIST)) fs.rmSync(DIST, { recursive: true });
fs.mkdirSync(DIST, { recursive: true });
fs.cpSync(PUBLIC, DIST, { recursive: true, dereference: true });
// Also ensure data dir exists in dist
fs.mkdirSync(path.join(DIST, 'data'), { recursive: true });
console.log('  ✓ static assets copied');

// Build pages
buildHome(articles, prices);
buildHive();

for (const a of articles) {
  buildArticle(a, articles);
}

// Ticker pages
const tickerMap = {};
for (const a of articles) {
  if (!tickerMap[a.ticker]) tickerMap[a.ticker] = [];
  tickerMap[a.ticker].push(a);
}
for (const [sym, arts] of Object.entries(tickerMap)) {
  buildTicker(sym, arts, prices);
}

// Sector pages
const sectorMap = {};
for (const a of articles) {
  if (!sectorMap[a.sector]) sectorMap[a.sector] = [];
  sectorMap[a.sector].push(a);
}
for (const [key, sec] of Object.entries(SECTORS)) {
  buildSector(key, sec, sectorMap[key] || [], prices);
}

buildSitemap(articles);
buildRSS(articles);
writeArticlesJson(articles);
console.log('✅ Build complete! Output in dist/');
