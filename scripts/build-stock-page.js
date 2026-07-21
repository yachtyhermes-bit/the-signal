#!/usr/bin/env node
// The Signal — Stock Profile Page Builder v4
// Tabs: Chart · Financials · Earnings · Statistics
// Dark Signal theme · Mobile-optimized · Completely isolated from main site

const fs = require('fs');
const path = require('path');

const DIST = path.join(__dirname, '..', 'dist');
const PUBLIC = path.join(__dirname, '..', 'public');
const DATA = path.join(__dirname, '..', 'data');
const ARTICLES = path.join(__dirname, '..', 'articles', 'posts');

// ── Date formatter ────────────────────────────────────────
function fmtDate(dateStr) {
  if (!dateStr) return '';
  const d = new Date(dateStr);
  if (isNaN(d.getTime())) return dateStr;
  return d.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' });
}

const financialsPath = path.join(DATA, 'financials.json');
const pricesPath = path.join(DATA, 'prices.json');
const financials = fs.existsSync(financialsPath) ? JSON.parse(fs.readFileSync(financialsPath, 'utf8')) : {};

function esc(s) { return String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;'); }
function val(d, key) { const v = d?.[key]; return v?.fmt ?? '—'; }
function fmtB(n) {
  if (n == null) return '—';
  const abs = Math.abs(n);
  if (abs >= 1e12) return '$' + (n/1e12).toFixed(2) + 'T';
  if (abs >= 1e9) return '$' + (n/1e9).toFixed(2) + 'B';
  if (abs >= 1e6) return '$' + (n/1e6).toFixed(1) + 'M';
  if (abs >= 1e3) return '$' + (n/1e3).toFixed(1) + 'K';
  return '$' + n.toFixed(2);
}

// ── Build one stock page ───────────────────────────────────
function buildStockPage(symbol) {
  const fin = financials[symbol];
  if (!fin) return null;

  const company = fin.company || {};
  const stats = fin.stats || {};
  const returns = fin.returns || {};
  const analyst = fin.analystTarget || {};
  const consensus = fin.consensus || {};
  const qf = fin.quarterlyFinancials || {};
  const earn = fin.earnings || [];

  // Build annualFinancials from FMP data if not already present
  if ((!fin.annualFinancials || !fin.annualFinancials.income) && fin.fmpIncome && fin.fmpIncome.length) {
    fin.annualFinancials = fin.annualFinancials || {};
    fin.annualFinancials.income = fin.fmpIncome.map(e => ({
      period: (e.date || '').slice(5,7) + '/' + (e.date || '').slice(0,4),
      'Total Revenue': e.revenue || 0,
      'Gross Profit': e.grossProfit || 0,
      'Net Income': e.netIncome || 0
    }));
  }
  if ((!fin.annualFinancials || !fin.annualFinancials.balance) && fin.fmpBalance && fin.fmpBalance.length) {
    fin.annualFinancials = fin.annualFinancials || {};
    fin.annualFinancials.balance = fin.fmpBalance.map(e => ({
      period: (e.date || '').slice(5,7) + '/' + (e.date || '').slice(0,4),
      'Total Assets': e.totalAssets || 0,
      'Total Liabilities': e.totalLiabilities || 0
    }));
  }

  // Price from live data
  const pricesRaw = fs.existsSync(pricesPath) ? JSON.parse(fs.readFileSync(pricesPath, 'utf8')) : {};
  const price = pricesRaw[symbol];
  const priceNow = price?.price ?? null;
  const changePct = price?.changePercent ?? null;
  const isPrivate = company.isPrivate || (price && price.isPrivate);

  const recKey = (fin.analyst?.recommendationKey || 'neutral').toLowerCase().replace(/_/g, '-');
  const targetMean = val(stats, 'targetMeanPrice');
  const analystUpside = priceNow && fin.analyst?.targetMeanPrice?.raw
    ? ((fin.analyst.targetMeanPrice.raw / priceNow - 1) * 100) : null;

  // Scan articles for this ticker
  let relatedArticles = [];
  if (fs.existsSync(ARTICLES)) {
    const articleFiles = fs.readdirSync(ARTICLES).filter(f => f.endsWith('.json'));
    for (const file of articleFiles) {
      try {
        const a = JSON.parse(fs.readFileSync(path.join(ARTICLES, file), 'utf8'));
        const tickerMatch = (a.ticker && a.ticker.toUpperCase() === symbol.toUpperCase()) ||
                            (a.slug && a.slug.toLowerCase().includes(symbol.toLowerCase()));
        if (tickerMatch) {
          relatedArticles.push({
            slug: a.slug,
            title: a.title,
            date: a.date,
            image: a.image?.src || '',
            caption: a.image?.caption || '',
            summary: a.summary || '',
            readTime: a.meta?.estimatedReadTime || '',
          });
        }
      } catch (_) { /* skip malformed */ }
    }
  }
  // Sort by date descending, keep max 12
  relatedArticles.sort((a, b) => (b.date || '').localeCompare(a.date || ''));
  relatedArticles = relatedArticles.slice(0, 12);

  // Package ALL data for the client-side chart JS
  // ── Sync chart to live price: extend data to today with synthetic bridging candles ──
  const chartData = fin.chartData || [];
  if (chartData.length > 0 && priceNow != null) {
    const lastCandle = chartData[chartData.length - 1];
    const lastDate = new Date(lastCandle.time + 'T00:00:00');
    const today = new Date();
    today.setHours(0, 0, 0, 0);

    // Count genuinely missing trading days (Mon-Fri, excluding weekends)
    const missingDays = [];
    const cursor = new Date(lastDate);
    cursor.setDate(cursor.getDate() + 1);
    while (cursor < today) {
      const dow = cursor.getDay();
      if (dow !== 0 && dow !== 6) missingDays.push(new Date(cursor));
      cursor.setDate(cursor.getDate() + 1);
    }

    const lastClose = lastCandle.close;

    if (missingDays.length > 0) {
      // Extend high/low of the last real candle to encompass the bridge range
      lastCandle.high = Math.max(lastCandle.high, priceNow, lastCandle.open);
      lastCandle.low  = Math.min(lastCandle.low,  priceNow, lastCandle.open);

      // Generate synthetic daily candles for each missing trading day
      const steps = missingDays.length;
      missingDays.forEach((date, i) => {
        const progress = (i + 1) / steps;
        const estClose = lastClose + (priceNow - lastClose) * progress;
        const dailyVol = Math.abs(lastClose) * 0.015; // ~1.5% daily volatility buffer
        chartData.push({
          time: date.toISOString().split('T')[0],
          open:  i === 0 ? lastClose : lastClose + (priceNow - lastClose) * (i / steps),
          high:  Math.max(estClose, estClose + dailyVol * 0.6),
          low:   Math.min(estClose, estClose - dailyVol * 0.6),
          close: i === steps - 1 ? priceNow : estClose,
          volume: Math.round((lastCandle.volume || 1000000) * (0.8 + Math.random() * 0.4)),
        });
      });
    } else {
      // Same day — just sync close and extend range
      lastCandle.close = priceNow;
      lastCandle.high = Math.max(lastCandle.high, priceNow, lastCandle.open);
      lastCandle.low  = Math.min(lastCandle.low,  priceNow, lastCandle.open);
    }
  }
  const embeddedData = JSON.stringify({
    currentPrice: priceNow,
    prices: chartData,
    quarterly: {
      revenue: qf.revenue || [],
      netIncome: qf.netIncome || [],
      eps: qf.eps || [],
      ebit: qf.ebit || [],
      totalAssets: qf.totalAssets || [],
      totalLiabilities: qf.totalLiabilities || [],
    },
    annual: fin.annualFinancials || {},
    earnings: earn,
  });

  const consensusTotal = (consensus.strongBuy||0) + (consensus.buy||0) + (consensus.hold||0) + (consensus.sell||0) + (consensus.strongSell||0);

  // Moat rating — read from Morningstar assessment (generated by generate-moat.py)
  const moatPath = path.join(DATA, `moat-${symbol}.json`);
  let moatData = null;
  if (fs.existsSync(moatPath)) {
    try { moatData = JSON.parse(fs.readFileSync(moatPath, 'utf8')); } catch (_) {}
  }
  // Fallback if moat data is missing
  if (!moatData || !moatData.rating) {
    moatData = { rating: 'None', stars: 1, confidence: 'Low', sources: [], analysis: 'Assessment unavailable.' };
  }
  const moatBadgeClass = moatData.rating === 'Wide' ? 'wide' : (moatData.rating === 'Narrow' ? 'narrow' : 'none');
  const moatStars = '★'.repeat(moatData.stars || 1) + '☆'.repeat(5 - (moatData.stars || 1));
  const moatLabel = moatData.rating === 'Wide' ? '🛡️ Wide Moat' : (moatData.rating === 'Narrow' ? '🛡️ Narrow Moat' : '⚠️ No Moat');
  // Build moat source rows with score dots
  const moatSourceRows = (moatData.sources || []).map(s => {
    const dots = '●'.repeat(s.score) + '○'.repeat(5 - s.score);
    return `<div class="moat-source-row">
      <span class="moat-source-name">${esc(s.name)}</span>
      <span class="moat-source-dots">${dots}</span>
    </div>`;
  }).join('');
  const moatSourceTooltip = (moatData.sources || []).map(s =>
    `<div class="moat-tooltip-item"><strong>${esc(s.name)}:</strong> ${esc(s.rationale)}</div>`
  ).join('');

  const html = `<!DOCTYPE html>
<html lang="en" class="stock-page">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
  <title>${esc(symbol)} — The Signal</title>
  <link rel="stylesheet" href="/css/stock-card.css">
  <link rel="stylesheet" href="/css/nav.css">
  <script src="https://cdn.jsdelivr.net/npm/lightweight-charts@4.1.3/dist/lightweight-charts.standalone.production.js"></script>
</head>
<body class="stock-page">

  <!-- ── NAV ── -->
  <nav class="stock-nav">
    <div class="stock-nav-inner">
      <a href="/stocks/" class="stock-nav-stocks">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="19" y1="12" x2="5" y2="12"></line><polyline points="12 19 5 12 12 5"></polyline></svg>
        Stocks
      </a>
      <a href="/" class="stock-nav-logo">
        <span class="logo-text"><span class="logo-the">THE</span> <strong>SIGNAL</strong></span>
      </a>
      <div class="stock-nav-right">
        <button class="theme-toggle" onclick="toggleTheme()" aria-label="Toggle theme">
          <span class="theme-icon">☀️</span>
        </button>
        <button class="nav-btn hamburger-btn" id="hamburgerToggle" aria-label="Menu">
          <span class="hamburger-line"></span>
          <span class="hamburger-line"></span>
          <span class="hamburger-line"></span>
        </button>
      </div>
    </div>
  </nav>

  <!-- Rocket Lab-Style Drawer -->
  <div class="drawer-overlay" id="drawerOverlay"></div>
  <div class="drawer" id="drawer">
    <div class="drawer-header">
      <a href="/" class="drawer-logo">
        <span class="the">THE</span>
        <span class="signal">SIGNAL</span>
      </a>
      <button class="drawer-close" id="drawerClose" aria-label="Close menu">&#10005;</button>
    </div>
    <div class="drawer-body" id="drawerBody">
      <div class="drawer-main" id="drawerMain">
        <div class="drawer-section-label">SECTORS</div>
        <a href="javascript:void(0)" class="drawer-link" onclick="openSubDrawer()">SECTORS</a>
        <a href="/stocks/" class="drawer-link">STOCK PAGES</a>
        <a href="/#scorecard" class="drawer-link">SIGNAL SCORECARD</a>
        <a href="/hive" class="drawer-link">HIVE</a>
        <a href="/signal-vs-the-street" class="drawer-link">SIGNAL VS. STREET</a>
        <a href="/pricing" class="drawer-link">SIGNAL PREMIUM</a>
        <a href="/pricing" class="drawer-cta">GET PREMIUM ACCESS</a>
      </div>
      <div class="drawer-sub" id="drawerSub">
        <div class="sub-header" onclick="closeSubDrawer()">
          <span class="sub-back">&#8249;</span>
          <span class="sub-title">SECTORS</span>
        </div>
        <a href="/sector/ai" class="drawer-link">AI</a>
        <a href="/sector/cyber" class="drawer-link">CYBER</a>
        <a href="/sector/defense" class="drawer-link">DEFENSE</a>
        <a href="/sector/space" class="drawer-link">SPACE</a>
        <a href="/sector/mega-cap" class="drawer-link">MEGA-CAP</a>
        <a href="/sector/quantum" class="drawer-link">QUANTUM</a>
        <a href="/sector/ai-power" class="drawer-link">AI POWER</a>
        <a href="/sector/etfs" class="drawer-link">ETFS</a>
      </div>
    </div>
  </div>

  <main class="stock-page-main">

    <!-- ═══════════ HERO ═══════════ -->
    <section class="stock-hero">
      <div class="stock-hero-inner">
        <div class="stock-hero-left">
          <div class="stock-ticker-badge">$${esc(symbol)}${isPrivate ? ' · Private Company' : ' · NASDAQ'}</div>
          <h1 class="stock-company-name">${esc(company.name || symbol)}</h1>
          ${isPrivate ? '<div class="stock-private-badge">Private Company</div>' : ''}
          <div class="stock-company-meta">
            <span class="flag">🇺🇸</span>
            <span>${esc(company.sector || '—')}</span>
            <span class="dot"></span>
            <span>${esc(company.industry || '—')}</span>
          </div>
        </div>
        <div class="stock-hero-right">
          <div class="stock-price-display" data-price="${symbol}">${isPrivate ? 'Private' : (priceNow ? '$' + priceNow.toFixed(2) : '—')}</div>
          ${!isPrivate && changePct != null ? `<div class="stock-change-display ${changePct >= 0 ? 'positive' : 'negative'}" data-change="${symbol}">
            ${changePct >= 0 ? '▲' : '▼'} ${Math.abs(changePct).toFixed(2)}%
          </div>` : ''}
          ${isPrivate ? '<div class="stock-change-display" style="color:var(--signal-gold)" data-change="${symbol}">Not Publicly Traded</div>' : ''}
        </div>
      </div>
      <div class="stock-hero-stats">
        <div class="hero-stat"><span class="hero-stat-label">Market Cap</span><span class="hero-stat-value">${isPrivate ? '—' : val(stats, 'marketCap')}</span></div>
        <div class="hero-stat"><span class="hero-stat-label">P/E (TTM)</span><span class="hero-stat-value">${isPrivate ? '—' : val(stats, 'trailingPE')}</span></div>
        <div class="hero-stat"><span class="hero-stat-label">52W Range</span><span class="hero-stat-value">${isPrivate ? '—' : val(stats, 'fiftyTwoWeekLow') + ' – ' + val(stats, 'fiftyTwoWeekHigh')}</span></div>
        <div class="hero-stat"><span class="hero-stat-label">Volume</span><span class="hero-stat-value">${isPrivate ? '—' : val(stats, 'avgVolume')}</span></div>
        <div class="hero-stat"><span class="hero-stat-label">Beta</span><span class="hero-stat-value">${isPrivate ? '—' : val(stats, 'beta')}</span></div>
      </div>
    </section>

    <!-- ═══════════ TABS ═══════════ -->
    <nav class="stock-tabs">
      <button class="stock-tab active" data-tab="overview">Summary</button>
      <button class="stock-tab" data-tab="financials">Financials</button>
      <button class="stock-tab" data-tab="earnings">Earnings</button>
      <button class="stock-tab" data-tab="news">News</button>
    </nav>

    <!-- ═══════════ OVERVIEW TAB (default) ═══════════ -->
    <div id="tab-overview" class="stock-tab-panel active">
      <!-- Chart -->
      ${!isPrivate ? `
      <section class="stock-chart-section">
        <div class="chart-header">
          <div class="chart-timeframe-bar">
            <button class="tf-btn active" data-tf="1m">1M</button>
            <button class="tf-btn" data-tf="3m">3M</button>
            <button class="tf-btn" data-tf="6m">6M</button>
            <button class="tf-btn" data-tf="1y">1Y</button>
            <button class="tf-btn" data-tf="5y">5Y</button>
            <button class="tf-btn" data-tf="all">ALL</button>
          </div>
        </div>
        <div id="stockChart" class="stock-chart"></div>
      </section>
      ` : `
      <section class="stock-section">
        <div class="stock-section-header"><h2 class="stock-section-title">📊 Private Company</h2></div>
        <p class="stock-profile-text">SpaceX is a privately held company. Live price data and stock charts are not available. Financial data shown is based on publicly reported estimates and funding round disclosures.</p>
      </section>
      `}

      <!-- Key Statistics -->
      <section class="stock-section">
        <div class="stock-section-header"><h2 class="stock-section-title">Key Statistics</h2></div>
        <div class="stock-stats-grid">
          ${sc('Revenue', val(stats,'totalRevenue'), val(stats,'revenueGrowth'))}
          ${sc('Net Income', val(stats,'netIncome'), val(stats,'epsGrowth'))}
          ${sc('Gross Margin', val(stats,'grossMargins'))}
          ${sc('Net Margin', val(stats,'profitMargins'))}
          ${sc('P/E Ratio', val(stats,'trailingPE'))}
          ${sc('Forward P/E', val(stats,'forwardPE'))}
          ${sc('PEG Ratio', val(stats,'pegRatio'))}
          ${sc('P/S Ratio', val(stats,'priceToSales'))}
        </div>
      </section>

      <!-- Financial Performance -->
      <section class="stock-section">
        <div class="stock-section-header"><h2 class="stock-section-title">Financial Performance</h2></div>
        <div class="stock-stats-grid">
          ${sc('EBITDA', val(stats,'ebitda'), val(stats,'ebitdaGrowth'))}
          ${sc('Free Cash Flow', val(stats,'freeCashflow'), val(stats,'freeCashflowGrowth'))}
          ${sc('Operating Margin', val(stats,'operatingMargins'))}
          ${sc('ROE', val(stats,'returnOnEquity'))}
          ${sc('Total Debt', val(stats,'totalDebt'))}
          ${sc('Total Cash', val(stats,'totalCash'))}
          ${sc('Dividend Yield', val(stats,'dividendYield'))}
          ${sc('EPS (TTM)', val(stats,'epsTrailing'))}
        </div>
      </section>

      <!-- The Signal Report -->
      <section class="stock-section signal-report-section">
        <div class="signal-report-header">
          <div class="signal-report-title-row">
            <img src="https://readthesignal.net/img/logo-original.png" alt="The Signal" class="signal-report-logo" />
            <h2 class="stock-section-title">The Signal Report</h2>
            <span class="signal-report-badge">PREMIUM</span>
          </div>
        </div>

        <div class="signal-report-grid">
          <!-- Column 1: Rating -->
          <div class="signal-rating-col">
            <div class="signal-rating-label">Moat Rating</div>
            <div class="signal-moat-badge ${moatBadgeClass}">${moatLabel}</div>
            <div class="signal-stars">${moatStars}</div>
            <div class="signal-moat-reasons">
              ${moatSourceRows || '<div class="moat-source-row"><span class="moat-source-name">No data available</span></div>'}
            </div>
            <div class="signal-moat-confidence">Confidence: ${esc(moatData.confidence || 'Low')}</div>
          </div>

          <!-- Column 2: Fair Value -->
          <div class="signal-fair-value-col">
            <div class="signal-fair-value-label">Fair Value</div>
            <div class="signal-fair-value-price">${fin.analyst?.targetMeanPrice?.fmt || '—'}</div>
            <div class="signal-fair-value-change ${analystUpside != null && analystUpside >= 0 ? 'positive' : 'negative'}">${analystUpside != null ? (analystUpside >= 0 ? '+' : '') + analystUpside.toFixed(1) + '% upside' : '—'}</div>
            <div class="signal-fair-value-context">Based on ${fin.analyst?.numberOfAnalystOpinions || 0} analyst targets</div>
          </div>
        </div>

        <!-- AI Analysis -->
        <div class="signal-ai-analysis">
          <div class="signal-ai-header">
            <span class="signal-ai-icon">🤖</span>
            <span>Pulse AI Analysis</span>
          </div>
          <p class="signal-ai-text">${esc((fin.aiAnalysis || '').slice(0, 300))}${(fin.aiAnalysis || '').length > 300 ? '...' : ''}</p>
          <div class="signal-premium-cta">
            <span class="premium-lock">🔒</span>
            <span>Members Only</span>
            <span class="premium-arrow">→</span>
          </div>
        </div>

        <!-- Valuation Quick Stats -->
        <div class="signal-valuation-stats">
          <div class="signal-val-stat">
            <div class="signal-val-label">P/E (TTM)</div>
            <div class="signal-val-value">${val(stats, 'trailingPE')}</div>
          </div>
          <div class="signal-val-stat">
            <div class="signal-val-label">Forward P/E</div>
            <div class="signal-val-value">${val(stats, 'forwardPE')}</div>
          </div>
          <div class="signal-val-stat">
            <div class="signal-val-label">PEG Ratio</div>
            <div class="signal-val-value">${val(stats, 'pegRatio')}</div>
          </div>
          <div class="signal-val-stat">
            <div class="signal-val-label">Analyst Consensus</div>
            <div class="signal-val-value ${recKey}">${recKey.replace(/-/g, ' ')}</div>
          </div>
        </div>
      </section>

      <!-- Analyst Consensus -->
      <section class="stock-section">
        <div class="stock-section-header"><h2 class="stock-section-title">Wall Street Consensus</h2></div>
        <span class="analyst-rating-badge ${recKey}">${recKey.replace(/-/g, ' ')}</span>
        ${targetMean !== '—' ? `
        <div class="analyst-target-row">
          <div class="analyst-target-item"><span class="target-label">Mean Target</span><span class="target-value">${targetMean}</span>${analystUpside != null ? `<span class="target-upside">+${analystUpside.toFixed(1)}%</span>` : ''}</div>
          <div class="analyst-target-divider"></div>
          <div class="analyst-target-item"><span class="target-label">High</span><span class="target-value">${analyst.high?.fmt || '—'}</span></div>
          <div class="analyst-target-divider"></div>
          <div class="analyst-target-item"><span class="target-label">Low</span><span class="target-value">${analyst.low?.fmt || '—'}</span></div>
        </div>` : ''}
        ${consensusTotal > 0 ? `
        <div class="consensus-list">
          ${bar('Strong Buy', consensus.strongBuy||0, consensusTotal, '#22c55e')}
          ${bar('Buy', consensus.buy||0, consensusTotal, '#86efac')}
          ${bar('Hold', consensus.hold||0, consensusTotal, '#f59e0b')}
          ${bar('Sell', consensus.sell||0, consensusTotal, '#ef4444')}
          ${bar('Strong Sell', consensus.strongSell||0, consensusTotal, '#dc2626')}
        </div>` : ''}
      </section>

      <!-- Total Returns -->
      <section class="stock-section">
        <div class="stock-section-header"><h2 class="stock-section-title">Total Returns</h2></div>
        <div class="stock-returns-grid">
          ${rc('1 Year', returns.oneYear)}
          ${rc('5 Year', returns.fiveYear)}
          ${rc('10 Year', returns.tenYear)}
          ${rc('Year to Date', returns.ytd)}
        </div>
      </section>

      <!-- Company Profile -->
      <section class="stock-section">
        <div class="stock-section-header"><h2 class="stock-section-title">Company Profile</h2></div>
        <p class="stock-profile-text">${esc((company.description || '').slice(0, 700))}</p>
        <div class="stock-profile-grid">
          <div class="profile-item"><span class="profile-label">Sector</span><span class="profile-value">${esc(company.sector||'—')}</span></div>
          <div class="profile-item"><span class="profile-label">Industry</span><span class="profile-value">${esc(company.industry||'—')}</span></div>
          <div class="profile-item"><span class="profile-label">Employees</span><span class="profile-value">${company.employees ? Number(company.employees).toLocaleString() : '—'}</span></div>
          <div class="profile-item"><span class="profile-label">Headquarters</span><span class="profile-value">${esc([company.city,company.state].filter(Boolean).join(', ')||'—')}</span></div>
          <div class="profile-item"><span class="profile-label">Exchange</span><span class="profile-value">${esc(company.exchange||'NasdaqGS')}</span></div>
          <div class="profile-item"><span class="profile-label">Website</span><span class="profile-value"><a href="${esc(company.website||'#')}" target="_blank" rel="noopener">${esc(company.website||'—')}</a></span></div>
        </div>
      </section>
    </div>

    <!-- ═══════════ FINANCIALS TAB ═══════════ -->
    <div id="tab-financials" class="stock-tab-panel">
      <!-- ══ INCOME STATEMENT ══ -->
      <section class="fin-section">
        <div class="fin-header">
          <span class="fin-title">Income Statement</span>
          <div class="fin-toggle-group">
            <button class="fin-toggle-btn" data-mode="quarterly">Quarterly</button>
            <button class="fin-toggle-btn active" data-mode="annual">Annual</button>
          </div>
        </div>
        <div class="fin-chart-container">
          <div class="fin-chart-area">
            <div class="fin-chart-grid" id="finChartGrid"></div>
            <div class="fin-chart-bars" id="finChartBars"></div>
          </div>
          <div class="fin-chart-yaxis" id="finChartYAxis"></div>
        </div>
        <div class="fin-chart-xaxis" id="finChartXAxis"></div>
        <div class="fin-legend">
          <div class="fin-legend-item"><span class="fin-legend-dot" style="background:#4b8ae5"></span> Total Revenues</div>
          <div class="fin-legend-item"><span class="fin-legend-dot" style="background:#8d939c"></span> Net Income</div>
        </div>
      </section>
      <section class="fin-section">
        <div class="fin-table-wrap">
          <table class="fin-data-table" id="finDataTable">
            <thead><tr><th>Period Ending:</th></tr></thead>
            <tbody>
              <tr class="fin-data-row"><td class="fin-data-label">Total Revenues</td></tr>
              <tr class="fin-data-row"><td class="fin-data-label">Gross Profit</td></tr>
            </tbody>
          </table>
        </div>
      </section>
      <!-- ══ BALANCE SHEET ══ -->
      <section class="fin-section">
        <div class="fin-header">
          <span class="fin-title">Balance Sheet</span>
          <div class="fin-toggle-group">
            <button class="fin-toggle-btn-bs" data-mode="quarterly">Quarterly</button>
            <button class="fin-toggle-btn-bs active" data-mode="annual">Annual</button>
          </div>
        </div>
        <div class="fin-chart-container">
          <div class="fin-chart-area">
            <div class="fin-chart-grid" id="finBsGrid"></div>
            <div class="fin-chart-bars" id="finBsBars"></div>
          </div>
          <div class="fin-chart-yaxis" id="finBsYAxis"></div>
        </div>
        <div class="fin-chart-xaxis" id="finBsXAxis"></div>
        <div class="fin-legend">
          <div class="fin-legend-item"><span class="fin-legend-dot" style="background:#4b8ae5"></span> Total Assets</div>
          <div class="fin-legend-item"><span class="fin-legend-dot" style="background:#8d939c"></span> Total Liabilities</div>
        </div>
      </section>
      <section class="fin-section">
        <div class="fin-table-wrap">
          <table class="fin-data-table" id="finBsTable">
            <thead><tr><th>Period Ending:</th></tr></thead>
            <tbody>
              <tr class="fin-data-row"><td class="fin-data-label">Total Assets</td></tr>
              <tr class="fin-data-row"><td class="fin-data-label">Total Liabilities</td></tr>
            </tbody>
          </table>
        </div>
      </section>
    </div>

    <!-- ═══════════ EARNINGS TAB ═══════════ -->
    <div id="tab-earnings" class="stock-tab-panel">
      ${earn.length ? `
      <div class="earn-summary">
        <div class="earn-summary-title">Earnings & Revenue Forecast</div>
        <p class="earn-summary-text">${esc(company.name || symbol)} reported earnings results for the periods shown below. ${earn.filter(e => e.epsActual && e.epsEstimate).length} of the last ${earn.length} quarters have reported results.</p>
      </div>
      <div class="earn-cards">
        ${(() => {
          // Revenue forecast cards from quarterly estimates
          const revQ = (qf.revenue || []).filter(r => r.estimated && !r.actual).slice(0, 2).reverse();
          const epsQ = (qf.eps || []).filter(r => r.estimated && !r.actual).slice(0, 2).reverse();
          return revQ.map((r, i) => {
            const epsEst = epsQ.find(e => e.period === r.period);
            return `<div class="earn-card earn-card-forecast">
              <div class="earn-card-header">
                <span class="earn-card-period">${r.period} (Est)</span>
                <span class="earn-card-badge forecast">Forecast</span>
              </div>
              <div class="earn-card-row">
                <span class="earn-card-label">Revenue Est</span>
                <span class="earn-card-value">${fmtB(r.estimated)}</span>
              </div>
              ${epsEst ? `<div class="earn-card-row">
                <span class="earn-card-label">EPS Est</span>
                <span class="earn-card-value">$${epsEst.estimated?.toFixed(2) || '—'}</span>
              </div>` : ''}
            </div>`;
          }).join('');
        })()}
        ${earn.filter(e => e.epsActual != null).slice(0, 6).map(e => {
          const beat = e.epsActual > (e.epsEstimate || 0) ? 'beat' : (e.epsActual < (e.epsEstimate || 0) ? 'miss' : '');
          const surprise = e.epsEstimate ? ((e.epsActual - e.epsEstimate) / Math.abs(e.epsEstimate) * 100) : null;
          const revBeat = (e.revenueActual && e.revenueEstimate) ? (e.revenueActual > e.revenueEstimate ? 'beat' : 'miss') : '';
          const revSurprise = (e.revenueActual && e.revenueEstimate) ? ((e.revenueActual - e.revenueEstimate) / Math.abs(e.revenueEstimate) * 100) : null;
          return `<div class="earn-card">
            <div class="earn-card-header">
              <span class="earn-card-period">${e.date?.slice(0,7) || '—'}</span>
              ${beat ? `<span class="earn-card-badge ${beat}">${beat === 'beat' ? '✓ Beat' : '✗ Miss'}</span>` : ''}
            </div>
            <div class="earn-card-row">
              <span class="earn-card-label">Revenue Actual</span>
              <span class="earn-card-value">${e.revenueActual ? fmtB(e.revenueActual) : '—'}</span>
            </div>
            ${e.revenueEstimate ? `<div class="earn-card-row">
              <span class="earn-card-label">Revenue Forecast</span>
              <span class="earn-card-value">${fmtB(e.revenueEstimate)}</span>
            </div>
            ${revSurprise != null ? `<div class="earn-card-row">
              <span class="earn-card-label">Rev Surprise</span>
              <span class="earn-card-value earn-card-surprise ${revSurprise >= 0 ? 'positive' : 'negative'}">${revSurprise >= 0 ? '+' : ''}${revSurprise.toFixed(1)}%</span>
            </div>` : ''}` : ''}
            <div class="earn-card-row">
              <span class="earn-card-label">EPS Actual</span>
              <span class="earn-card-value">$${e.epsActual?.toFixed(2) || '—'}</span>
            </div>
            <div class="earn-card-row">
              <span class="earn-card-label">EPS Forecast</span>
              <span class="earn-card-value">$${e.epsEstimate?.toFixed(2) || '—'}</span>
            </div>
            ${surprise != null ? `<div class="earn-card-row">
              <span class="earn-card-label">EPS Surprise</span>
              <span class="earn-card-value earn-card-surprise ${surprise >= 0 ? 'positive' : 'negative'}">${surprise >= 0 ? '+' : ''}${surprise.toFixed(1)}%</span>
            </div>` : ''}
          </div>`;
        }).join('')}
      </div>` : '<div class="earn-summary"><p class="earn-summary-text">Earnings data will be available after the next report.</p></div>'}
    </div>

    <!-- ═══════════ NEWS TAB ═══════════ -->
    <div id="tab-news" class="stock-tab-panel">
      ${relatedArticles.length ? `
      <div class="news-grid">
        ${relatedArticles.map(a => {
          const imgRel = a.image?.src || a.image || '';
          const imgSrc = imgRel ? 'https://readthesignal.net' + (imgRel.startsWith('/') ? '' : '/') + imgRel : '';
          const title = esc(a.title || '');
          const summary = esc((a.summary || '').slice(0, 120));
          const dateStr = fmtDate(a.date);
          const readTime = a.readTime || '';
          const articleUrl = 'https://readthesignal.net/article/' + a.slug + '/';
          return '<a href="' + articleUrl + '" class="news-card" target="_blank" rel="noopener">' +
            (imgSrc ? '<div class="news-card-img-wrap"><img class="news-card-img" src="' + esc(imgSrc) + '" alt="' + title + '" loading="lazy"></div>' : '') +
            '<div class="news-card-body">' +
              '<h3 class="news-card-title">' + title + '</h3>' +
              '<div class="news-card-meta">' +
                (dateStr ? '<span class="news-card-date">' + dateStr + '</span>' : '') +
                (readTime ? '<span class="news-card-readtime">' + esc(readTime) + '</span>' : '') +
              '</div>' +
              (summary ? '<p class="news-card-summary">' + summary + '…</p>' : '') +
            '</div>' +
          '</a>';
        }).join('')}
      </div>` : '<div class="earn-summary"><p class="earn-summary-text">No related articles yet.</p></div>'}
    </div>

    <!-- ═══════════ STATISTICS TAB (removed — now on Overview) ═══════════ -->
  </main>

  <script id="chartData-${symbol}" type="application/json">${embeddedData}</script>
  <script src="/js/stock-chart.js?v=13"></script>
  <script>
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
  if (window._updateChartTheme) window._updateChartTheme();
}
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
      var main = document.getElementById('drawerMain');
      var sub = document.getElementById('drawerSub');
      if (main) main.classList.remove('hidden');
      if (sub) sub.classList.remove('active');
    }
    window.openSubDrawer = function() {
      var main = document.getElementById('drawerMain');
      var sub = document.getElementById('drawerSub');
      if (main) main.classList.add('hidden');
      if (sub) sub.classList.add('active');
    };
    window.closeSubDrawer = function() {
      var main = document.getElementById('drawerMain');
      var sub = document.getElementById('drawerSub');
      if (main) main.classList.remove('hidden');
      if (sub) sub.classList.remove('active');
    };
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
  // Live price updater for stock header
  (function(){var I=300000;function f(n){if(n==null||isNaN(n))return'---';return n.toLocaleString('en-US',{minimumFractionDigits:2,maximumFractionDigits:2})}function u(p){document.querySelectorAll('[data-price]').forEach(function(e){var s=e.getAttribute('data-price');var d=p[s];if(d&&d.price!=null)e.textContent='$'+f(d.price)});document.querySelectorAll('[data-change]').forEach(function(e){var s=e.getAttribute('data-change');var d=p[s];if(d&&d.changePercent!=null){var c=(d.changePercent>=0?'+':'')+d.changePercent.toFixed(2)+'%';e.textContent=(d.changePercent>=0?'▲ ':'▼ ')+Math.abs(d.changePercent).toFixed(2)+'%';var cl=e.className.replace(/positive|negative/g,'').trim();e.className=cl+' '+(d.changePercent>=0?'positive':'negative')}})})function r(){fetch(location.origin+'/api/prices/').then(function(r){return r.json()}).then(function(d){u((d.prices||d))}).catch(function(e){console.warn('price update:',e.message)})}r();setInterval(r,I)})();
  </script>
</body>
</html>`;

  const dir = path.join(DIST, 'stocks', symbol.toLowerCase());
  fs.mkdirSync(dir, { recursive: true });
  fs.writeFileSync(path.join(dir, 'index.html'), html);
  return true;
}

// ── Helpers ────────────────────────────────────────────────
function sc(label, value, changeVal) {
  const accent = (changeVal && changeVal !== '—') ? ' accent' : '';
  let ch = '';
  if (changeVal && changeVal !== '—') {
    const neg = String(changeVal).startsWith('-');
    ch = `<span class="stat-change ${neg ? 'negative' : 'positive'}">${changeVal}</span>`;
  }
  return `<div class="stat-card${accent}"><span class="stat-label">${label}</span><span class="stat-value">${value||'—'}</span>${ch}</div>`;
}
function rc(label, data) {
  const v = data?.fmt || '—';
  const cls = data?.raw != null ? (data.raw >= 0 ? 'positive' : 'negative') : '';
  return `<div class="return-card"><span class="return-label">${label}</span><span class="return-value ${cls}">${v}</span></div>`;
}
function bar(label, count, total, color) {
  if (!count) return '';
  const pct = total ? Math.round((count/total)*100) : 0;
  return `<div class="consensus-row"><span class="consensus-label">${label}</span><div class="consensus-bar-track"><div class="consensus-bar-fill" style="width:${pct}%;background:${color}"></div></div><span class="consensus-count">${count}</span></div>`;
}

// ── MAIN ────────────────────────────────────────────────────
const symbols = Object.keys(financials);
const distCss = path.join(DIST, 'css'), distJs = path.join(DIST, 'js');
fs.mkdirSync(distCss, { recursive: true });
fs.mkdirSync(distJs, { recursive: true });
fs.copyFileSync(path.join(PUBLIC,'css','stock-card.css'), path.join(distCss,'stock-card.css'));
fs.copyFileSync(path.join(PUBLIC,'css','nav.css'), path.join(distCss,'nav.css'));
fs.copyFileSync(path.join(PUBLIC,'js','stock-chart.js'), path.join(distJs,'stock-chart.js'));

// Also copy to stock project deploy root (signal-stock-pi Vercel project)
const stockDistCss = path.join(DIST, 'stock', 'css');
const stockDistJs = path.join(DIST, 'stock', 'js');
fs.mkdirSync(stockDistCss, { recursive: true });
fs.mkdirSync(stockDistJs, { recursive: true });
fs.copyFileSync(path.join(PUBLIC,'css','stock-card.css'), path.join(stockDistCss,'stock-card.css'));
fs.copyFileSync(path.join(PUBLIC,'css','nav.css'), path.join(stockDistCss,'nav.css'));
fs.copyFileSync(path.join(PUBLIC,'js','stock-chart.js'), path.join(stockDistJs,'stock-chart.js'));

console.log(`🏗  Building stock pages for ${symbols.length} ticker(s)...`);
let built = 0;
for (const symbol of symbols) {
  if (buildStockPage(symbol)) { console.log(`  ✅ /stock/${symbol}/`); built++; }
  else { console.log(`  ⚠️  Skipping ${symbol} — no data`); }
}
console.log(`✅ Built ${built} stock page(s)`);
