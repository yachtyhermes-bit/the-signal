#!/usr/bin/env node
// The Signal — Stock Profile Page Builder v4
// Tabs: Chart · Financials · Earnings · Statistics
// Dark Signal theme · Mobile-optimized · Completely isolated from main site

const fs = require('fs');
const path = require('path');

const DIST = path.join(__dirname, '..', 'dist');
const PUBLIC = path.join(__dirname, '..', 'public');
const DATA = path.join(__dirname, '..', 'data');

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

  // Price from live data
  const pricesRaw = fs.existsSync(pricesPath) ? JSON.parse(fs.readFileSync(pricesPath, 'utf8')) : {};
  const price = pricesRaw[symbol];
  const priceNow = price?.price ?? null;
  const changePct = price?.changePercent ?? null;

  const recKey = (fin.analyst?.recommendationKey || 'neutral').toLowerCase().replace(/_/g, '-');
  const targetMean = val(stats, 'targetMeanPrice');
  const analystUpside = priceNow && fin.analyst?.targetMeanPrice
    ? ((fin.analyst.targetMeanPrice / priceNow - 1) * 100) : null;

  // Package ALL data for the client-side chart JS
  const embeddedData = JSON.stringify({
    prices: fin.chartData || [],
    quarterly: {
      revenue: qf.revenue || [],
      netIncome: qf.netIncome || [],
      eps: qf.eps || [],
      ebit: qf.ebit || [],
    },
    annual: fin.annualFinancials || {},
    earnings: earn,
  });

  const consensusTotal = (consensus.strongBuy||0) + (consensus.buy||0) + (consensus.hold||0) + (consensus.sell||0) + (consensus.strongSell||0);

  const html = `<!DOCTYPE html>
<html lang="en" class="stock-page">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
  <title>${esc(symbol)} — The Signal</title>
  <link rel="stylesheet" href="/css/stock-card.css">
  <script src="https://cdn.jsdelivr.net/npm/lightweight-charts@4.1.3/dist/lightweight-charts.standalone.production.js"></script>
</head>
<body class="stock-page">

  <!-- ── NAV ── -->
  <nav class="stock-nav">
    <div class="stock-nav-inner">
      <div class="stock-nav-left">
        <a href="/" class="stock-nav-back">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="19" y1="12" x2="5" y2="12"></line><polyline points="12 19 5 12 12 5"></polyline></svg>
          The Signal
        </a>
        <span class="stock-nav-ticker"><span>$${esc(symbol)}</span> · ${esc(company.sector || '')}</span>
      </div>
    </div>
  </nav>

  <main class="stock-page-main">

    <!-- ═══════════ HERO ═══════════ -->
    <section class="stock-hero">
      <div class="stock-hero-inner">
        <div class="stock-hero-left">
          <div class="stock-ticker-badge">$${esc(symbol)} · NASDAQ</div>
          <h1 class="stock-company-name">${esc(company.name || symbol)}</h1>
          <div class="stock-company-meta">
            <span class="flag">🇺🇸</span>
            <span>${esc(company.sector || '—')}</span>
            <span class="dot"></span>
            <span>${esc(company.industry || '—')}</span>
          </div>
        </div>
        <div class="stock-hero-right">
          <div class="stock-price-display">${priceNow ? '$' + priceNow.toFixed(2) : '—'}</div>
          ${changePct != null ? `<div class="stock-change-display ${changePct >= 0 ? 'positive' : 'negative'}">
            ${changePct >= 0 ? '▲' : '▼'} ${Math.abs(changePct).toFixed(2)}%
          </div>` : ''}
        </div>
      </div>
      <div class="stock-hero-stats">
        <div class="hero-stat"><span class="hero-stat-label">Market Cap</span><span class="hero-stat-value">${val(stats, 'marketCap')}</span></div>
        <div class="hero-stat"><span class="hero-stat-label">P/E (TTM)</span><span class="hero-stat-value">${val(stats, 'trailingPE')}</span></div>
        <div class="hero-stat"><span class="hero-stat-label">52W Range</span><span class="hero-stat-value">${val(stats, 'fiftyTwoWeekLow')} – ${val(stats, 'fiftyTwoWeekHigh')}</span></div>
        <div class="hero-stat"><span class="hero-stat-label">Volume</span><span class="hero-stat-value">${val(stats, 'avgVolume')}</span></div>
        <div class="hero-stat"><span class="hero-stat-label">Beta</span><span class="hero-stat-value">${val(stats, 'beta')}</span></div>
      </div>
    </section>

    <!-- ═══════════ TABS ═══════════ -->
    <nav class="stock-tabs">
      <button class="stock-tab active" data-tab="overview">Summary</button>
      <button class="stock-tab" data-tab="financials">Financials</button>
      <button class="stock-tab" data-tab="earnings">Earnings</button>
    </nav>

    <!-- ═══════════ OVERVIEW TAB (default) ═══════════ -->
    <div id="tab-overview" class="stock-tab-panel active">
      <!-- Chart -->
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

    <!-- ═══════════ STATISTICS TAB (removed — now on Overview) ═══════════ -->
  </main>

  <script id="chartData-${symbol}" type="application/json">${embeddedData}</script>
  <script src="/js/stock-chart.js"></script>
</body>
</html>`;

  const dir = path.join(DIST, 'stock', symbol);
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
fs.copyFileSync(path.join(PUBLIC,'js','stock-chart.js'), path.join(distJs,'stock-chart.js'));

console.log(`🏗  Building stock pages for ${symbols.length} ticker(s)...`);
let built = 0;
for (const symbol of symbols) {
  if (buildStockPage(symbol)) { console.log(`  ✅ /stock/${symbol}/`); built++; }
  else { console.log(`  ⚠️  Skipping ${symbol} — no data`); }
}
console.log(`✅ Built ${built} stock page(s)`);
