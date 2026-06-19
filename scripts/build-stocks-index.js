#!/usr/bin/env node
// The Signal — Stocks Index Page Builder
// Generates /stocks/index.html with all tracked stocks and search

const fs = require('fs');
const path = require('path');

const ROOT = path.join(__dirname, '..');
const DATA = path.join(ROOT, 'data');
const DIST = path.join(ROOT, 'dist');

function esc(s) { return String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;'); }

// Load data
const financialsPath = path.join(DATA, 'financials.json');
const pricesPath = path.join(DATA, 'prices.json');

if (!fs.existsSync(financialsPath)) {
  console.error('ERROR: data/financials.json not found');
  process.exit(1);
}

const financials = JSON.parse(fs.readFileSync(financialsPath, 'utf8'));
const prices = fs.existsSync(pricesPath) ? JSON.parse(fs.readFileSync(pricesPath, 'utf8')) : {};
const symbols = Object.keys(financials);

console.log(`📊 Building stocks index for ${symbols.length} tickers...`);

// Build stock list data for JS
const stockListData = symbols.map(sym => {
  const fin = financials[sym];
  const name = (fin && fin.company && fin.company.name) || sym;
  const price = prices[sym];
  const isPrivate = (fin && fin.company && fin.company.isPrivate) || (price && price.isPrivate);

  // Moat data
  let moatRating = 'None';
  let moatClass = 'none';
  const moatPath = path.join(DATA, `moat-${sym}.json`);
  if (fs.existsSync(moatPath)) {
    try {
      const moatData = JSON.parse(fs.readFileSync(moatPath, 'utf8'));
      moatRating = moatData.rating || 'None';
      moatClass = moatRating === 'Wide' ? 'wide' : (moatRating === 'Narrow' ? 'narrow' : 'none');
    } catch (_) {}
  }

  const moatBadge = moatRating === 'Wide' ? '🛡️ Wide Moat' : (moatRating === 'Narrow' ? '🛡️ Narrow Moat' : '');

  if (isPrivate) {
    return { sym, name, price: 'Private', change: '—', changeClass: '', isPrivate: true, moatRating, moatClass, moatBadge };
  }

  const priceVal = price && price.price != null ? price.price : null;
  const changePct = price && price.changePercent != null ? price.changePercent : null;
  const priceStr = priceVal != null ? '$' + priceVal.toFixed(2) : '—';
  const changeStr = changePct != null ? (changePct >= 0 ? '+' : '') + changePct.toFixed(2) + '%' : '—';
  const changeClass = changePct != null ? (changePct >= 0 ? 'positive' : 'negative') : '';

  return { sym, name, price: priceStr, change: changeStr, changeClass, isPrivate: false, moatRating, moatClass, moatBadge };
});

// Build stock cards HTML — slim row layout
const cardsHtml = stockListData.map(s => {
  return `<a href="/stocks/${esc(s.sym)}/" class="stocks-card" data-ticker="${esc(s.sym)}">
    <div class="stocks-card-left">
      <span class="stocks-card-ticker">$${esc(s.sym)}</span>
      <span class="stocks-card-name">${esc(s.name)}</span>
    </div>
    <div class="stocks-card-right">
      <span class="stocks-card-price" data-price="${esc(s.sym)}">${esc(s.price)}</span>
      <span class="stocks-card-change ${s.changeClass}" data-change="${esc(s.sym)}">${esc(s.change)}</span>
    </div>
  </a>`;
}).join('\n');

// Build search data as JSON for client-side filtering
const stockListJson = JSON.stringify(stockListData);

const html = `<!DOCTYPE html>
<html lang="en" class="stock-page">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
  <title>Stocks — The Signal</title>
  <meta name="description" content="Track all stocks covered by The Signal. Real-time prices, moat ratings, and deep analysis on NVDA, TSLA, AMZN, PLTR, SPACEX, RKLB and more.">
  <link rel="stylesheet" href="/css/stock-card.css">
  <link rel="canonical" href="https://readthesignal.net/stocks/">
</head>
<body class="stock-page">

  <!-- ── NAV ── -->
  <nav class="stock-nav">
    <div class="stock-nav-inner">
      <a href="/" class="stock-nav-stocks">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="19" y1="12" x2="5" y2="12"></line><polyline points="12 19 5 12 12 5"></polyline></svg>
        The Signal
      </a>
      <a href="/" class="stock-nav-logo">
        <span class="logo-text"><span class="logo-the">THE</span> <strong>SIGNAL</strong></span>
      </a>
      <div class="stock-nav-right">
        <button class="theme-toggle" onclick="toggleTheme()" aria-label="Toggle theme">
          <span class="theme-icon">☀️</span>
        </button>
        <button class="hamburger-btn" aria-label="Menu">
          <span class="hamburger-line"></span>
          <span class="hamburger-line"></span>
          <span class="hamburger-line"></span>
        </button>
      </div>
    </div>
  </nav>

  <!-- ── DRAWER MENU ── -->
  <div class="drawer-overlay" id="drawerOverlay"></div>
  <div class="drawer" id="drawer">
    <div class="drawer-header">
      <button class="drawer-close" id="drawerClose" aria-label="Close menu">✕</button>
      <a href="/" class="drawer-logo">
        <span class="drawer-logo-text">SIGNAL</span>
      </a>
    </div>
    <div class="drawer-body">
      <div class="drawer-section-label">SECTORS</div>
      <a href="/sector/ai" class="drawer-link">AI</a>
      <a href="/sector/cyber" class="drawer-link">Cyber</a>
      <a href="/sector/defense" class="drawer-link">Defense</a>
      <a href="/sector/space" class="drawer-link">Space</a>
      <a href="/sector/mega-cap" class="drawer-link">Mega-Cap</a>
      <a href="/sector/quantum" class="drawer-link">Quantum</a>
      <hr class="drawer-divider">
      <div class="drawer-section-label">FEATURES</div>
      <a href="/hive" class="drawer-link">Hive</a>
      <a href="/signal-vs-the-street" class="drawer-link">Signal vs. Street</a>
      <a href="/stocks/" class="drawer-link">📈 Stock Pages</a>
      <a href="/#scorecard" class="drawer-link">📊 Signal Scorecard</a>
    </div>
  </div>

  <main class="stock-page-main stocks-index-main">
    <!-- ── HERO ── -->
    <section class="stocks-index-hero">
      <div class="stocks-index-hero-inner">
        <h1 class="stocks-index-title">Stocks</h1>
        <p class="stocks-index-subtitle">Tracked companies on The Signal — real-time prices, moat ratings, and deep analysis.</p>
      </div>
    </section>

    <!-- ── SEARCH ── -->
    <div class="stocks-search-wrapper">
      <div class="stocks-search-container">
        <svg class="stocks-search-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg>
        <input type="text" class="stocks-search-input" placeholder="Search by ticker or company..." id="stocksSearch" autocomplete="off">
      </div>
      <div class="stocks-count" id="stocksCount">${symbols.length} stocks</div>
    </div>

    <!-- ── STOCK CARDS GRID ── -->
    <div class="stocks-grid" id="stocksGrid">
      ${cardsHtml}
    </div>
  </main>

  <script>
    const stockList = ${stockListJson};

    (function() {
      const saved = localStorage.getItem('stock-theme');
      if (saved === 'light') {
        document.documentElement.classList.add('light');
        var icon = document.querySelector('.theme-icon');
        if (icon) icon.textContent = '🌙';
      }
    })();

    function toggleTheme() {
      const html = document.documentElement;
      html.classList.toggle('light');
      localStorage.setItem('stock-theme', html.classList.contains('light') ? 'light' : 'dark');
      var icon = document.querySelector('.theme-icon');
      if (icon) icon.textContent = html.classList.contains('light') ? '🌙' : '☀️';
    }

    // Search filtering
    const searchInput = document.getElementById('stocksSearch');
    const stocksGrid = document.getElementById('stocksGrid');
    const stocksCount = document.getElementById('stocksCount');
    const allCards = Array.from(stocksGrid.querySelectorAll('.stocks-card'));

    searchInput.addEventListener('input', function() {
      const query = this.value.toLowerCase().trim();
      let visible = 0;

      allCards.forEach((card, i) => {
        const stock = stockList[i];
        if (!stock) return;
        const ticker = stock.sym.toLowerCase();
        const name = stock.name.toLowerCase();
        const match = !query || ticker.includes(query) || name.includes(query);
        card.style.display = match ? '' : 'none';
        if (match) visible++;
      });

      stocksCount.textContent = visible === allCards.length
        ? '${symbols.length} stocks'
        : visible + ' of ${symbols.length} stocks';
    });
  </script>
  <script>
  document.addEventListener('DOMContentLoaded', function(){
    var btn = document.querySelector('.hamburger-btn');
    var drawer = document.getElementById('drawer');
    var overlay = document.getElementById('drawerOverlay');
    var closeBtn = document.getElementById('drawerClose');
    function openDrawer() {
      if(drawer){drawer.classList.add('open');}
      if(overlay){overlay.classList.add('open');}
      document.body.style.overflow = 'hidden';
    }
    function closeDrawer() {
      if(drawer){drawer.classList.remove('open');}
      if(overlay){overlay.classList.remove('open');}
      document.body.style.overflow = '';
    }
    if (btn && drawer && overlay) {
      btn.addEventListener('click', function(){ openDrawer(); });
      overlay.addEventListener('click', function(){ closeDrawer(); });
      if (closeBtn) closeBtn.addEventListener('click', function(){ closeDrawer(); });
      document.addEventListener('keydown', function(e){
        if (e.key === 'Escape' && drawer.classList.contains('open')) closeDrawer();
      });
      drawer.querySelectorAll('a').forEach(function(a){
        a.addEventListener('click', function(){ closeDrawer(); });
      });
    }
  });
  </script>
  <script>
  // Live price updater — fetches from Vercel proxy every 5 min
  (function() {
    var INTERVAL = 300000;
    function formatNum(n) {
      if (n == null || isNaN(n)) return '---';
      return n.toLocaleString('en-US', {minimumFractionDigits:2,maximumFractionDigits:2});
    }
    function updatePrices(prices) {
      document.querySelectorAll('[data-price]').forEach(function(el) {
        var sym = el.getAttribute('data-price');
        var p = prices[sym];
        if (p && p.price != null) el.textContent = '$' + formatNum(p.price);
      });
      document.querySelectorAll('[data-change]').forEach(function(el) {
        var sym = el.getAttribute('data-change');
        var p = prices[sym];
        if (p && p.changePercent != null) {
          var chg = (p.changePercent >= 0 ? '+' : '') + p.changePercent.toFixed(2) + '%';
          el.textContent = chg;
          el.className = el.className.replace(/positive|negative/g,'').trim() + ' ' + (p.changePercent >= 0 ? 'positive' : 'negative');
        }
      });
    }
    function fetchPrices() {
      fetch('/api/prices/').then(function(r){return r.json()}).then(updatePrices).catch(function(){});
    }
    fetchPrices();
    setInterval(fetchPrices, INTERVAL);
  })();
  </script>
</body>
</html>`;

// Write output
const outDir = path.join(DIST, 'stocks');
fs.mkdirSync(outDir, { recursive: true });
fs.writeFileSync(path.join(outDir, 'index.html'), html);
console.log(`  ✅ /stocks/index.html — ${symbols.length} stocks, ${Buffer.byteLength(html)} bytes`);
