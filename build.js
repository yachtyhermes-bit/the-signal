#!/usr/bin/env node
// Static site generator — reads article JSONs, outputs dist/ folder
const fs = require('fs');
const path = require('path');

const ROOT = __dirname;
const ARTICLES_DIR = path.join(ROOT, 'articles', 'posts');
const INDEX_FILE = path.join(ROOT, 'articles', 'index.json');
const DIST = path.join(ROOT, 'dist');
const PUBLIC = path.join(ROOT, 'public');
const TEMPLATES_DIR = path.join(ROOT, 'templates');

const SECTORS = {
  ai: { name: 'AI', tickers: ['NVDA','AMD','AVGO','MRVL','TSM','ASML','MU','CBRS'], color: '#3b82f6' },
  cyber: { name: 'Cybersecurity', tickers: ['CRWD','PANW','FTNT','ZS','S','CHKP','CYBR','TENB'], color: '#22c55e' },
  defense: { name: 'Defense', tickers: ['LMT','RTX','NOC','GD','LHX','KTOS','AVAV','PL'], color: '#fbbf24' },
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
  'PL': { name: 'Planet Labs', url: 'https://www.planet.com/' }
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

function esc(s) {
  return String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;').replace(/'/g, '&#39;');
}

// === HTML rendering ===
function renderHeader(title, desc, article) {
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
  return `<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="theme-color" content="#08080e">
  <meta name="robots" content="max-image-preview:large">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&family=JetBrains+Mono:wght@500;700&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="/css/main.css">
  <title>${esc(title)}</title>
  <meta name="description" content="${esc(desc)}">
  <meta property="og:title" content="${esc(title)}">
  <meta property="og:description" content="${esc(desc)}">
  ${ogExtra}
</head>
<body>
  <nav class="nav">
    <div class="nav-inner">
      <a href="/" class="logo"><span class="logo-icon">◈</span><span class="logo-text">THE <strong>SIGNAL</strong></span></a>
      <div class="nav-links">
        <a href="/" class="nav-link">Live</a>
        <a href="/sector/ai" class="nav-link">AI</a>
        <a href="/sector/cyber" class="nav-link">Cyber</a>
        <a href="/sector/defense" class="nav-link">Defense</a>
        <a href="/sector/space" class="nav-link">Space</a>
        <a href="/sector/mega-cap" class="nav-link">Mega-Cap</a>
      </div>
    </div>
  </nav>
  <main class="main">${ldJson ? ldJson : ''}`;
}

function renderFooter() {
  return `  </main>
  <footer class="footer">
    <div class="footer-inner">
      <div class="footer-brand"><span class="logo-icon">◈</span> THE <strong>SIGNAL</strong></div>
      <div class="footer-tag">Analysis by Hermes Agent Swarm · Data from public sources</div>
      <div class="footer-copy">© ${new Date().getFullYear()} The Signal — readthesignal.com</div>
    </div>
  </footer>
</body>
</html>`;
}

function renderCard(a) {
  const sentLabel = a.sentiment === 'bullish' ? '▲ Bullish' : a.sentiment === 'bearish' ? '▼ Bearish' : '– Neutral';
  return `<a href="/article/${a.slug}" class="article-card">
    <div class="card-top">
      <span class="ticker-badge ${a.sentiment || 'neutral'}">${a.ticker}</span>
      <span class="sentiment-label ${a.sentiment || 'neutral'}">${sentLabel}</span>
    </div>
    <h3 class="card-title">${esc(a.title)}</h3>
    <p class="card-summary">${esc(a.summary.length > 200 ? a.summary.slice(0, 200) + '…' : a.summary)}</p>
    <div class="card-meta">
      <span class="card-date">${formatDate(a.date)}</span>
      <span class="card-read">${readMin(a)} min read</span>
    </div>
  </a>`;
}

function renderSectorBadge(s) {
  const cssClass = s.toLowerCase().replace(/ /g, '-');
  return `<a href="/sector/${s.toLowerCase()}" class="sector-badge ${cssClass}">${s.toUpperCase()}</a>`;
}

// === Build pages ===
function buildHome(articles) {
  const hero = `<section class="hero">
    <div class="hero-content">
      <h1 class="hero-title">Read the <span class="accent-blue">signal</span> before the market moves</h1>
      <p class="hero-sub">AI · Defense · Space · Cybersecurity — analysis that connects the dots</p>
    </div>
  </section>`;
  const feed = `<section class="feed">
    <div class="feed-header">
      <h2 class="feed-title">● Live Feed</h2>
      <div class="feed-sectors">
        ${Object.keys(SECTORS).map(s => renderSectorBadge(SECTORS[s].name)).join('\n        ')}
      </div>
    </div>
    <div class="article-grid">
      ${articles.map(renderCard).join('\n      ')}
    </div>
  </section>`;
  const html = renderHeader('The Signal — Market Intelligence for AI, Defense, Space & Cyber',
    'The Signal delivers sharp analysis on AI, defense, space, and cybersecurity stocks. Earnings deep-dives, contract analysis, and market-moving insights.')
    + hero + feed + renderFooter();
  fs.mkdirSync(DIST, { recursive: true });
  fs.writeFileSync(path.join(DIST, 'index.html'), html);
  console.log('  ✓ index.html');
}

function buildArticle(article) {
  const sentLabel = article.sentiment === 'bullish' ? '▲ Bullish' : article.sentiment === 'bearish' ? '▼ Bearish' : '– Neutral';
  const img = typeof article.image === 'object' ? article.image : (article.image ? { src: article.image } : null);
  const info = COMPANY_INFO[article.ticker] || {};
  const linksHtml = article.links && article.links.length
    ? `<div class="article-links"><h4>🔗 Learn More</h4><ul>${article.links.map(l => `<li><a href="${esc(l.url)}" target="_blank" rel="noopener">${esc(l.label)}</a></li>`).join('\n          ')}</ul></div>`
    : '';

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
      ${article.bodyHtml || ''}
    </div>
    <div class="article-footer">
      <div class="article-tags">
        <span class="tag">$${article.ticker}</span>
        <span class="tag">${SECTORS[article.sector]?.name || article.sector}</span>
        ${(article.tags || []).map(t => `<span class="tag">${esc(t)}</span>`).join('\n        ')}
      </div>
      ${linksHtml}
    </div>
  </article>`;

  const html = renderHeader(article.title + ' — The Signal', article.summary, article) + body + renderFooter();
  const dir = path.join(DIST, 'article', article.slug);
  fs.mkdirSync(dir, { recursive: true });
  fs.writeFileSync(path.join(dir, 'index.html'), html);
  console.log(`  ✓ article/${article.slug}/`);
}

function buildTicker(symbol, articles) {
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
      ${articles.length ? articles.map(renderCard).join('\n      ') : '<div class="empty-state">No articles yet for $' + symbol + '. Check back soon.</div>'}
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

function buildSector(key, sec, articles, allArticles) {
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
      ${articles.length ? articles.map(renderCard).join('\n      ') : '<div class="empty-state">No articles yet in this sector.</div>'}
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
  // Add ticker pages
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

// === Entry point ===
console.log('🏗️  Building The Signal...');
const articles = loadArticles();
console.log(`   Loaded ${articles.length} articles`);

// Clean dist
if (fs.existsSync(DIST)) fs.rmSync(DIST, { recursive: true });

// Copy static assets
fs.cpSync(PUBLIC, path.join(DIST, 'public'), { recursive: true, dereference: true });
// Copy public to root for direct CSS access
fs.cpSync(PUBLIC, path.join(DIST, 'public'), { recursive: true, dereference: true });
console.log('  ✓ static assets copied');

// Build pages
buildHome(articles);

for (const a of articles) buildArticle(a);

// Build ticker pages
const tickerArticles = {};
for (const a of articles) {
  if (!tickerArticles[a.ticker]) tickerArticles[a.ticker] = [];
  tickerArticles[a.ticker].push(a);
}
for (const [symbol, arts] of Object.entries(tickerArticles)) {
  buildTicker(symbol, arts);
}

// Build sector pages
for (const [key, sec] of Object.entries(SECTORS)) {
  const sectorArticles = articles.filter(a => sec.tickers.includes(a.ticker));
  buildSector(key, sec, sectorArticles, articles);
}

// Build sitemap & RSS
buildSitemap(articles);
buildRSS(articles);

// Write articles index
fs.writeFileSync(path.join(DIST, 'articles.json'), JSON.stringify(articles.map(a => ({
  slug: a.slug, title: a.title, summary: a.summary, ticker: a.ticker,
  sector: a.sector, sentiment: a.sentiment, date: a.date
})), null, 2));
console.log('  ✓ articles.json (for price fetcher)');

// Write vercel.json
const vercelJson = {
  "rewrites": [
    { "source": "/css/:path*", "destination": "/public/css/:path*" },
    { "source": "/img/:path*", "destination": "/public/img/:path*" },
    { "source": "/js/:path*", "destination": "/public/js/:path*" }
  ],
  "trailingSlash": true,
  "headers": [
    { "source": "/(.*)", "headers": [
      { "key": "X-Content-Type-Options", "value": "nosniff" },
      { "key": "Referrer-Policy", "value": "strict-origin-when-cross-origin" }
    ]}
  ],
  "cleanUrls": false
};
fs.writeFileSync(path.join(DIST, 'vercel.json'), JSON.stringify(vercelJson, null, 2));
console.log('  ✓ vercel.json');

console.log('✅ Build complete! Output in dist/');
