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
  ai: { name: 'AI', tickers: ['NVDA','AMD','AVGO','MRVL','TSM','ASML','MU','CBRS','CRWV'], color: '#3b82f6' },
  cyber: { name: 'Cybersecurity', tickers: ['CRWD','PANW','FTNT','ZS','S','CHKP','CYBR','TENB'], color: '#22c55e' },
  defense: { name: 'Defense', tickers: ['LMT','RTX','NOC','GD','LHX','KTOS','AVAV','PL','AXON','GE'], color: '#fbbf24' },
  space: { name: 'Space', tickers: ['RKLB','RDW','LUNR','ASTS'], color: '#a78bfa' },
  'mega-cap': { name: 'Mega-Cap', tickers: ['AAPL','MSFT','GOOGL','AMZN','META','TSLA'], color: '#f87171' },
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
  'GE': { name: 'GE Aerospace', url: 'https://www.geaerospace.com/' }
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

const TICKER_SYMBOLS = ['NVDA','PLTR','AVGO','AMD','GOOGL','META','MSFT','AMZN','TSLA','CRWV'];

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

// === HTML rendering ===
function renderHeader(title, desc, article, allArticles) {
  let ogExtra = '';
  let ldJson = '';
  if (article) {
    const img = typeof article.image === 'object' ? article.image.src : article.image;
    ogExtra = `<meta property="og:title" content="${esc(article.title)}">
    <meta property="og:description" content="${esc(article.summary)}">
    <meta property="og:type" content="article">
    <meta property="og:url" content="https://readthesignal.com/article/${article.slug}">
    ${img ? `<meta property="og:image" content="${esc(img)}"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="675">` : ''}
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="${esc(article.title)}">
    <meta name="twitter:description" content="${esc(article.summary)}">
    ${img ? `<meta name="twitter:image" content="${esc(img)}">` : ''}`;
    ldJson = `<script type="application/ld+json">
    {
      "@context": "https://schema.org",
      "@type": "NewsArticle",
      "headline": ${JSON.stringify(article.title)},
      "description": ${JSON.stringify(article.summary)},
      "datePublished": "${article.date}",
      "dateModified": "${article.date}",
      "mainEntityOfPage": {"@type":"WebPage","@id":"https://readthesignal.com/article/${article.slug}"},
      "author": {"@type":"Organization","name":"The Signal","url":"https://readthesignal.com"},
      "publisher": {"@type":"Organization","name":"The Signal","logo":{"@type":"ImageObject","url":"https://readthesignal.com/img/logo.png","width":600,"height":60}},
      "image": ${JSON.stringify(img || 'https://readthesignal.com/img/og-default.png')}
    }
    </script>`;
  }
  return `<!DOCTYPE html>\n<html lang="en">\n<head>\n  <meta charset="UTF-8">\n  <meta name="viewport" content="width=device-width, initial-scale=1.0">\n  <meta name="theme-color" content="#08080e">\n  <meta name="robots" content="max-image-preview:large">\n  <link rel="preconnect" href="https://fonts.googleapis.com">\n  <link href="https://fonts.googleapis.com/css2?family=Anton&family=Inter:wght@400;500;600;700;800;900&family=JetBrains+Mono:wght@500;700&display=swap" rel="stylesheet">\n  <link rel="stylesheet" href="/css/main.css">
  <link rel="stylesheet" href="/css/pulse-badge.css">\n  <script src="/js/prices.js" defer></script>\n  <script src="/js/search.js" defer></script>\n  <script src="/js/auth.js" defer></script>\n  <script src="/js/pulse.js" defer></script>\n  <title>${esc(title)}</title>\n  <meta name="description" content="${esc(desc)}">\n  <meta property="og:title" content="${esc(title)}">\n  <meta property="og:description" content="${esc(desc)}">\n  ${ogExtra}\n</head>\n<body>\n  <nav class="nav">\n    <div class="nav-inner">\n      <a href="/" class="logo"><img src="/img/logo-hex.jpg" alt="The Signal" class="logo-img"><span class="logo-text">THE <strong>SIGNAL</strong></span></a>\n      <div class="nav-links">\n        <a href="/sector/ai" class="nav-link">AI</a>\n        <a href="/sector/cyber" class="nav-link">Cyber</a>\n        <a href="/sector/defense" class="nav-link">Defense</a>\n        <a href="/sector/space" class="nav-link">Space</a>\n        <a href="/sector/mega-cap" class="nav-link">Mega-Cap</a>\n      </div>\n      <div class="nav-actions">\n        <button class="nav-btn search-btn" id="searchToggle" aria-label="Search">\n          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">\n            <circle cx="11" cy="11" r="8"></circle>\n            <line x1="21" y1="21" x2="16.65" y2="16.65"></line>\n          </svg>\n        </button>\n        <div class="auth-container" id="authContainer">\n          <button class="nav-btn auth-btn" id="authToggle" aria-label="Sign In">\n            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">\n              <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path>\n              <circle cx="12" cy="7" r="4"></circle>\n            </svg>\n            <span class="auth-label" id="authLabel">Sign In</span>\n          </button>\n          <div class="auth-dropdown" id="authDropdown">\n            <div class="auth-user-info" id="authUserInfo" style="display:none">\n              <img class="auth-avatar" id="authAvatar" src="" alt="">\n              <span class="auth-name" id="authName"></span>\n              <button class="auth-signout-btn" id="authSignOut">Sign Out</button>\n            </div>\n            <div class="auth-options" id="authOptions">\n              <button class="auth-option google" id="authGoogle"><span class="auth-icon">G</span> Sign in with Google</button>\n              <button class="auth-option github" id="authGithub"><span class="auth-icon">⌘</span> Sign in with GitHub</button>\n              <button class="auth-option email" id="authEmail"><span class="auth-icon">✉</span> Sign in with Email</button>\n            </div>\n          </div>\n        </div>\n      </div>\n    </div>\n  </nav>\n\n  <!-- Search Overlay -->\n  <div class="search-overlay" id="searchOverlay">\n    <div class="search-backdrop" id="searchBackdrop"></div>\n    <div class="search-modal">\n      <div class="search-header">\n        <input type="text" class="search-input" id="searchInput" placeholder="Search articles by title, ticker, sector, or tag…" autofocus>\n        <button class="search-close" id="searchClose" aria-label="Close search">\n          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">\n            <line x1="18" y1="6" x2="6" y2="18"></line>\n            <line x1="6" y1="6" x2="18" y2="18"></line>\n          </svg>\n        </button>\n      </div>\n      <div class="search-results" id="searchResults"></div>\n      <div class="search-empty" id="searchEmpty">Start typing to search articles…</div>\n    </div>\n  </div>\n\n  <script id="articles-data" type="application/json">${JSON.stringify(allArticles || [])}</script>\n  <main class="main">${ldJson ? ldJson : ''}`;
}

function renderFooter() {
  return `  </main>
  <footer class="footer">
    <div class="footer-inner">
      <div class="footer-brand"><img src="/img/logo-hex.jpg" alt="The Signal" class="footer-logo"> THE <strong>SIGNAL</strong></div>
      <div class="footer-tag">The Signal Editorial Team · readthesignal.com</div>
      <div class="footer-copy">© ${new Date().getFullYear()} The Signal — Market Intelligence. Data from public sources.</div>
    </div>
  <script src="/js/prices.js" defer></script>
  <script src="/js/search.js" defer></script>
  <script src="/js/auth.js" defer></script>
  <script src="/js/pulse.js" defer></script>
</html>`;
}

function renderCard(a, prices) {
  const sentLabel = a.sentiment === 'bullish' ? '▲ Bullish' : a.sentiment === 'bearish' ? '▼ Bearish' : '– Neutral';
  const img = typeof a.image === 'object' ? a.image : (a.image ? { src: a.image } : null);
  const imgHtml = img ? `<div class="card-image"><img src="${esc(img.src)}" alt="${esc(a.title)}" loading="lazy"></div>` : '';
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
  const imgHtml = img ? `<div class="featured-image"><img src="${esc(img.src)}" alt="${esc(a.title)}" loading="eager"></div>` : '';
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

function injectVideos(bodyHtml, videos) {
  if (!videos || !videos.length) return bodyHtml;
  let result = bodyHtml;
  for (let i = 0; i < videos.length; i++) {
    const marker = `<!-- VIDEO ${i} -->`;
    const card = renderVideoCard(videos[i]);
    if (card) result = result.replace(marker, card);
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
    ? `<section class="feed feed-continued"><div class="article-grid">${articles.slice(5).map(a => renderCard(a, prices)).join('\n      ')}</div></section>`
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
  </section>
  ${gridRest}`;

  const html = renderHeader('The Signal — Market Intelligence for AI, Defense, Space & Cyber',
    'The Signal delivers sharp analysis on AI, defense, space, and cybersecurity stocks. Earnings deep-dives, contract analysis, and market-moving insights.',
    null, articles)
    + ticker + hero + feed + renderFooter();
  fs.mkdirSync(DIST, { recursive: true });
  fs.writeFileSync(path.join(DIST, 'index.html'), html);
  console.log('  ✓ index.html');
}

function buildArticle(article, allArticles) {
  const sentLabel = article.sentiment === 'bullish' ? '▲ Bullish' : article.sentiment === 'bearish' ? '▼ Bearish' : '– Neutral';
  const img = typeof article.image === 'object' ? article.image : (article.image ? { src: article.image } : null);
  const info = COMPANY_INFO[article.ticker] || {};
  const linksHtml = article.links && article.links.length
    ? `<div class="article-links"><h4>🔗 Learn More</h4><ul>${article.links.map(l => `<li><a href="${esc(l.url)}" target="_blank" rel="noopener">${esc(l.label)}</a></li>`).join('\n          ')}</ul></div>`
    : '';
  const bodyHtml = injectVideos(article.bodyHtml || '', article.videos);

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
        ${relImg ? `<div class="related-card-image"><img src="${esc(relImg.src)}" alt="${esc(a.title)}" loading="lazy"></div>` : ''}
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
    ${img ? `<div class="article-image"><img src="${esc(img.src)}" alt="${esc(article.title)}" loading="eager"></div>` : ''}
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
    `Latest analysis for ${info.name || symbol} (${symbol}). Articles, earnings, and market intelligence.`)
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
    `Latest analysis of ${sec.name.toLowerCase()} stocks including ${sec.tickers.slice(0, 5).join(', ')}.`)
    + body + renderFooter();
  const dir = path.join(DIST, 'sector', key);
  fs.mkdirSync(dir, { recursive: true });
  fs.writeFileSync(path.join(dir, 'index.html'), html);
  console.log(`  ✓ sector/${key}/`);
}

function buildSitemap(articles) {
  let xml = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n';
  xml += '  <url><loc>https://readthesignal.com/</loc><priority>1.0</priority></url>\n';
  for (const a of articles) {
    xml += `  <url><loc>https://readthesignal.com/article/${a.slug}</loc><lastmod>${a.date.split('T')[0]}</lastmod><priority>0.9</priority></url>\n`;
  }
  for (const key of Object.keys(SECTORS)) {
    xml += `  <url><loc>https://readthesignal.com/sector/${key}</loc><priority>0.7</priority></url>\n`;
  }
  const tickers = new Set(articles.map(a => a.ticker));
  for (const t of tickers) {
    xml += `  <url><loc>https://readthesignal.com/ticker/${t}</loc><priority>0.6</priority></url>\n`;
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
  <link>https://readthesignal.com/</link>
  <description>AI, defense, space &amp; cyber stock analysis</description>
  <atom:link href="https://readthesignal.com/rss" rel="self" type="application/rss+xml"/>`;
  for (const a of articles.slice(0, 50)) {
    rss += `
  <item>
    <title><![CDATA[${a.title}]]></title>
    <link>https://readthesignal.com/article/${a.slug}</link>
    <description><![CDATA[${a.summary}]]></description>
    <pubDate>${new Date(a.date).toUTCString()}</pubDate>
    <guid>https://readthesignal.com/article/${a.slug}</guid>
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
