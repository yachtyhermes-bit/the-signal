#!/usr/bin/env node
// The Signal — Trader Holdings Page Builder (data-driven)
//
// Reads data/traders.json and:
//   1. Renders one full holdings page per investor → dist/<slug>/index.html
//      (replicates _backup_dist/buffett/index.html structure; shared
//      nav/drawer/search-overlay blocks are EXTRACTED from that page at
//      runtime via regex so they stay in sync with the frozen design).
//   2. Regenerates the `const investors = [...]` array in dist/insights/index.html
//      and injects/refreshes the /* TRADER-GEN-COLORS */ per-slug CSS block.
//
// Idempotent. Missing data/dist → warn + exit 0 (never crashes `npm run build`).
// Wired into build.js after the dist copy exists (after scripts/build-stocks-index.js).

const fs = require('fs');
const path = require('path');

const ROOT = path.join(__dirname, '..');
const DATA_PATH = path.join(ROOT, 'data', 'traders.json');
const DIST = path.join(ROOT, 'dist');
const BACKUP_PAGE = path.join(ROOT, '_backup_dist', 'buffett', 'index.html');
const TEMPLATE_CSS = path.join(ROOT, 'scripts', 'templates', 'trader-page.css');
const INSIGHTS_PATH = path.join(DIST, 'insights', 'index.html');

const SEC_DISCLAIMER =
  'Data shown is for informational purposes only and may be delayed. Holdings and weights are based on latest available SEC 13F filings. Past performance does not guarantee future results. This is not investment advice.';

// ─── Helpers ────────────────────────────────────────────────────────────────

function esc(s) {
  return String(s == null ? '' : s)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/•/g, '&bull;');
}

function fmtNum(n) {
  const v = Number(n);
  if (!isFinite(v)) return '0';
  const r = Math.round(v * 10) / 10;
  return Number.isInteger(r) ? String(r) : String(r);
}

function fmtRet(v) {
  const n = Number(v) || 0;
  return (n >= 0 ? '+' : '') + n.toFixed(2) + '%';
}

function fmtPrice(p) {
  if (p === null || p === undefined || p === '') return '—';
  const n = Number(p);
  if (!isFinite(n)) return '—';
  return '$' + n.toFixed(2);
}

function fmtWeight(w) {
  return fmtNum(w) + '%';
}

function changeHtml(c) {
  if (c === null || c === undefined || c === '') {
    return '<span class="holding-change">—</span>';
  }
  const n = Number(c);
  if (!isFinite(n)) return '<span class="holding-change">' + esc(c) + '</span>';
  if (n >= 0) {
    return '<span class="holding-change pos"><span class="change-arrow">&#9650;</span>+' + n.toFixed(1) + '%</span>';
  }
  return '<span class="holding-change neg"><span class="change-arrow">&#9660;</span>' + n.toFixed(1) + '%</span>';
}

// Deterministic smooth curve: 10 monotonic points, cubic-bezier (catmull-rom) path.
// `ret` may be negative — both curves share a normalized value range so the
// portfolio/S&P lines always render relative to each other (and to 0%).
function perfPoints(ret, i) {
  const t = i / 9;
  return ret * Math.pow(t, 1.7); // smooth, monotonic, starts slow
}

function smoothPath(pts) {
  let d = 'M' + pts[0][0].toFixed(1) + ',' + pts[0][1].toFixed(1);
  for (let i = 0; i < pts.length - 1; i++) {
    const p0 = pts[Math.max(0, i - 1)];
    const p1 = pts[i];
    const p2 = pts[i + 1];
    const p3 = pts[Math.min(pts.length - 1, i + 2)];
    const c1x = p1[0] + (p2[0] - p0[0]) / 6;
    const c1y = p1[1] + (p2[1] - p0[1]) / 6;
    const c2x = p2[0] - (p3[0] - p1[0]) / 6;
    const c2y = p2[1] - (p3[1] - p1[1]) / 6;
    d += ' C' + c1x.toFixed(1) + ',' + c1y.toFixed(1) + ' ' + c2x.toFixed(1) + ',' + c2y.toFixed(1) +
      ' ' + p2[0].toFixed(1) + ',' + p2[1].toFixed(1);
  }
  return d;
}

function dotsHtml(pts, color) {
  return pts
    .map((p, i) => {
      const r = i === pts.length - 1 ? 4 : 2.5;
      return '                <circle cx="' + p[0].toFixed(1) + '" cy="' + p[1].toFixed(1) + '" r="' + r + '" fill="' + color + '"/>';
    })
    .join('\n');
}

// ─── Per-investor page builders ─────────────────────────────────────────────

function buildHead(inv, styleCss) {
  const slug = inv.slug;
  const url = 'https://readthesignal.net/' + slug;
  const desc = esc(inv.description || '');
  return [
    '<!DOCTYPE html>',
    '<html lang="en">',
    '<head>',
    '  <meta charset="UTF-8">',
    '  <meta name="viewport" content="width=device-width, initial-scale=1.0">',
    '  <meta name="theme-color" content="#0b1226">',
    '  <link rel="canonical" href="' + url + '">',
    '  <link rel="icon" type="image/x-icon" href="/favicon.ico">',
    '  <link rel="apple-touch-icon" sizes="180x180" href="/img/apple-touch-icon.png">',
    '  <meta name="robots" content="max-image-preview:large">',
    '  <meta name="description" content="' + desc + '">',
    '  <meta property="og:title" content="' + esc(inv.name) + ' - Read The Signal">',
    '  <meta property="og:description" content="' + desc + '">',
    '  <meta property="og:url" content="' + url + '">',
    '  <meta property="og:type" content="website">',
    '  <link rel="preconnect" href="https://fonts.googleapis.com">',
    '  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap" rel="stylesheet">',
    '  <link rel="stylesheet" href="/css/main.css?v=27">',
    '  <link rel="stylesheet" href="/css/nav.css?v=1">',
    '  <script async src="https://www.googletagmanager.com/gtag/js?id=G-98KDVDFBCW"></script>',
    '  <script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments);}gtag(\'js\',new Date());gtag(\'config\',\'G-98KDVDFBCW\');</script>',
    '  <script src="/js/prices.js" defer></script>',
    '  <script src="/js/search.js" defer></script>',
    '  <script src="/js/auth.js?v=2" defer></script>',
    '  <script src="/js/theme.js?v=2" defer></script>',
    '  <script src="/js/nav.js?v=1" defer></script>',
    '  <title>' + esc(inv.name) + ' - Read The Signal</title>',
    '  <style>',
    styleCss,
    '  </style>',
    '</head>',
    '<body>'
  ].join('\n');
}

function buildBreadcrumbs(inv) {
  return [
    '      <!-- Breadcrumbs -->',
    '      <div class="breadcrumbs">',
    '        <a href="/insights">Insights</a>',
    '        <span class="sep">/</span>',
    '        <span class="current">' + esc(inv.name) + '</span>',
    '      </div>'
  ].join('\n');
}

function buildHero(inv) {
  const holdings = inv.holdings || [];
  return [
    '      <!-- Hero Grid -->',
    '      <div class="hero-grid">',
    '        <!-- Hero Card (left) -->',
    '        <div class="hero-card">',
    '          <div class="hero-card-header">',
    '            <div class="hero-avatar" style="background:' + inv.avatarGradient + '">',
    '              <span style="font-weight:800;font-size:1.5rem">' + esc(inv.avatarIcon) + '</span>',
    '            </div>',
    '            <span class="hero-handle">' + esc(inv.handle) + '</span>',
    '          </div>',
    '          <div class="hero-name">' + esc(inv.displayName || inv.name) + '</div>',
    '          <div class="hero-title">' + esc(inv.title || '') + '</div>',
    '          <div class="hero-desc">' + esc(inv.description || '') + '</div>',
    '          <div class="hero-bio">' + esc(inv.bio || '') + '</div>',
    '          <div class="hero-stats">',
    '            <div>',
    '              <div class="hero-stat-label">250D Return</div>',
    '              <div class="hero-stat-value ' + (inv.ret250 < 0 ? 'red' : 'green') + '">' + fmtRet(inv.ret250) + '</div>',
    '            </div>',
    '            <div>',
    '              <div class="hero-stat-label">Holdings</div>',
    '              <div class="hero-stat-value white">' + holdings.length + '</div>',
    '            </div>',
    '            <div>',
    '              <div class="hero-stat-label">Last Update</div>',
    '              <div class="hero-stat-date">' + esc(inv.lastUpdate || '') + '</div>',
    '            </div>',
    '          </div>',
    '        </div>'
  ].join('\n');
}

function buildWeighting(inv) {
  const holdings = inv.holdings || [];
  const legend = holdings
    .map(
      h =>
        '            <div class="weighting-legend-item"><span class="weighting-legend-dot" style="background:' +
        h.color +
        '"></span>' + esc(h.company) +
        ' <span class="weighting-legend-pct">' + fmtWeight(h.weight) + '</span></div>'
    )
    .join('\n');
  return [
    '        <!-- Portfolio Weighting Card (right) -->',
    '        <div class="weighting-card">',
    '          <div class="weighting-title">Portfolio Weighting <span class="info-icon">i</span></div>',
    '          <div class="donut-large">',
    '            <img src="' + esc(inv.donutImage) + '" alt="' + esc(inv.displayName || inv.name) + ' portfolio holdings" class="donut-large-chart" style="width:100%;height:100%;border-radius:50%;object-fit:cover;display:block">',
    '          </div>',
    '          <div class="weighting-legend">',
    legend,
    '          </div>',
    '        </div>',
    '      </div>'
  ].join('\n');
}

function buildHoldings(inv) {
  const holdings = inv.holdings || [];
  const maxW = Math.max.apply(null, holdings.map(h => Number(h.weight) || 0).concat([1]));
  const rows = holdings
    .map(h => {
      const barW = fmtNum(Math.round((Number(h.weight) / maxW) * 1000) / 10);
      return (
        '              <tr>\n' +
        '                <td><span class="holding-ticker" style="background:' + h.color + '">' + esc(h.ticker) + '</span></td>\n' +
        '                <td>\n' +
        '                  <div class="holding-name-row">\n' +
        '                    <span class="holding-company">' + esc(h.company) + '</span>\n' +
        '                  </div>\n' +
        '                </td>\n' +
        '                <td><span class="holding-price">' + fmtPrice(h.price) + '</span></td>\n' +
        '                <td>\n' +
        '                  <div class="weight-bar-wrap">\n' +
        '                    <div class="weight-bar"><div class="weight-bar-fill" style="width:' + barW + '%;background:' + h.color + '"></div></div>\n' +
        '                    <span class="weight-pct">' + fmtWeight(h.weight) + '</span>\n' +
        '                  </div>\n' +
        '                </td>\n' +
        '                <td>' + changeHtml(h.change) + '</td>\n' +
        '              </tr>'
      );
    })
    .join('\n');
  return [
    '        <!-- Top ' + holdings.length + ' Holdings Table (left, wider) -->',
    '        <div class="holdings-card">',
    '          <div class="holdings-header">',
    '            <span class="holdings-title">Top Holdings by Weight</span>',
    '            <a href="' + esc(inv.wikiUrl) + '" target="_blank" rel="noopener" class="holdings-view-all">View all &rarr;</a>',
    '          </div>',
    '          <table class="holdings-table">',
    '            <thead>',
    '              <tr>',
    '                <th>Ticker</th>',
    '                <th>Company</th>',
    '                <th>Price</th>',
    '                <th>Weight</th>',
    '                <th>Change</th>',
    '              </tr>',
    '            </thead>',
    '            <tbody>',
    rows,
    '            </tbody>',
    '          </table>',
    '        </div>'
  ].join('\n');
}

function buildPerf(inv) {
  // Timeframes come from the optional nested `perf` object — each entry is
  // { ret, sp } percents (may be negative). If `perf` is missing entirely,
  // fall back to the legacy inv.ret250 / inv.retSp500 as the 1y values.
  const TIMEFRAMES = ['1y', '3y', '5y'];
  const PERF_LABELS = {
    '1y': ['Jan', 'Mar', 'May', 'Jul', 'Sep', 'Nov', 'Jan'],
    '3y': ['2023', '2024', '2025', '2026'],
    '5y': ['2021', '2022', '2023', '2024', '2025', '2026']
  };
  const perf = inv.perf && typeof inv.perf === 'object' && !Array.isArray(inv.perf) ? inv.perf : null;
  const frames = [];
  TIMEFRAMES.forEach(tf => {
    const p = perf && perf[tf];
    if (p && typeof p === 'object' && (p.ret !== undefined || p.sp !== undefined)) {
      frames.push({ tf, ret: Number(p.ret) || 0, sp: Number(p.sp) || 0 });
    }
  });
  if (frames.length === 0) {
    frames.push({ tf: '1y', ret: Number(inv.ret250) || 0, sp: Number(inv.retSp500) || 0 });
  }

  // Moomoo-style labeled stat rows — one row per available perf frame.
  // Values come straight from inv.perf (embedded at build time, no fetching).
  const FRAME_LABELS = { '1y': 'Last 1 Year', '3y': 'Last 3 Years', '5y': 'Last 5 Years' };
  const statRows = frames
    .map(f => {
      const cls = f.ret >= 0 ? 'pos' : 'neg';
      return (
        '            <div class="perf-stat-row">\n' +
        '              <span class="perf-stat-label">' + FRAME_LABELS[f.tf] + '</span>\n' +
        '              <span class="perf-stat-metrics">\n' +
        '                <span class="perf-stat-val ' + cls + '">' + fmtRet(f.ret) + '</span>\n' +
        '                <span class="perf-stat-sp">S&amp;P 500 ' + fmtRet(f.sp) + '</span>\n' +
        '              </span>\n' +
        '            </div>'
      );
    })
    .join('\n');

  const chartGroup = (frame, isFirst) => {
    const ret250 = frame.ret;
    const retSp500 = frame.sp;
    const n = 10;
    const minVal = Math.min(0, ret250, retSp500);
    const maxVal = Math.max(0, ret250, retSp500);
    const range = maxVal - minVal || 1;
    const toXY = (v, i) => {
      const t = i / (n - 1);
      return [10 + t * 325, 180 - ((v - minVal) / range) * 150];
    };
    const portPts = Array.from({ length: n }, (_, i) => toXY(perfPoints(ret250, i), i));
    const spPts = Array.from({ length: n }, (_, i) => toXY(perfPoints(retSp500, i), i));
    const portLabelY = Math.min(190, Math.max(15, portPts[n - 1][1] - 10));
    const spLabelY = Math.min(190, Math.max(15, spPts[n - 1][1] + 15));
    return [
      '            <div class="perf-chart-group' + (isFirst ? ' active' : '') + '" data-perf="' + frame.tf + '">',
      '              <div class="perf-chart-wrap">',
      '                <svg viewBox="0 0 340 200" preserveAspectRatio="none">',
      '                  <!-- Grid lines -->',
      '                  <line x1="0" y1="20" x2="340" y2="20" stroke="#2c426f" stroke-width="1"/>',
      '                  <line x1="0" y1="70" x2="340" y2="70" stroke="#2c426f" stroke-width="1"/>',
      '                  <line x1="0" y1="120" x2="340" y2="120" stroke="#2c426f" stroke-width="1"/>',
      '                  <!-- Portfolio line (orange) -->',
      '                  <path fill="none" stroke="#f97316" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" d="' + smoothPath(portPts) + '"/>',
      '                  <!-- Portfolio data dots -->',
      dotsHtml(portPts, '#f97316'),
      '                  <!-- S&P 500 line (slate) -->',
      '                  <path fill="none" stroke="#5e7092" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" d="' + smoothPath(spPts) + '"/>',
      '                  <!-- S&P data dots -->',
      dotsHtml(spPts, '#5e7092'),
      '                  <!-- End point labels -->',
      '                  <text x="335" y="' + portLabelY + '" text-anchor="end" fill="#f97316" font-size="10" font-weight="700">' + fmtRet(ret250) + '</text>',
      '                  <text x="335" y="' + spLabelY + '" text-anchor="end" fill="#71717a" font-size="10" font-weight="600">' + fmtRet(retSp500) + '</text>',
      '                </svg>',
      '              </div>',
      '              <div class="perf-labels">',
      ...PERF_LABELS[frame.tf].map(l => '                <span>' + l + '</span>'),
      '              </div>',
      '              <div class="perf-legend">',
      '                <div class="perf-legend-item"><span class="perf-legend-dot" style="background:#f97316"></span>Portfolio <span class="perf-val">' + fmtRet(ret250) + '</span></div>',
      '                <div class="perf-legend-item"><span class="perf-legend-dot" style="background:#5e7092"></span>S&amp;P 500 <span class="perf-val">' + fmtRet(retSp500) + '</span></div>',
      '              </div>',
      '            </div>'
    ].join('\n');
  };

  return [
    '          <!-- Performance Card -->',
    '          <div class="perf-card">',
    '            <div class="perf-header">',
    '              <span class="perf-title">Performance</span>',
    '              <div class="perf-toggles">',
    ...frames.map((f, i) => '                <button class="perf-toggle' + (i === 0 ? ' active' : '') + '" data-perf="' + f.tf + '">' + f.tf.toUpperCase() + '</button>'),
    '              </div>',
    '            </div>',
    '            <div class="perf-stats">',
    '              <div class="perf-stats-title">Returns</div>',
    statRows,
    '            </div>',
    ...frames.map((f, i) => chartGroup(f, i === 0)),
    '          </div>'
  ].join('\n');
}

function buildChanges(inv) {
  const changes = inv.changes || [];
  if (changes.length === 0) return '';
  const ICONS = { add: ['+', 'add'], increase: ['+', 'increase'], reduce: ['&minus;', 'reduce'], exit: ['&times;', 'exit'] };
  const items = changes
    .map(c => {
      const pair = ICONS[c.type] || ['+', 'add'];
      const amount = String(c.amount || '');
      const amountClass = amount.indexOf('+') === 0 ? 'pos' : 'neg';
      const amountHtml = amount.replace(/^-/, '&minus;');
      return (
        '            <div class="change-item">\n' +
        '              <div class="change-icon-wrap ' + pair[1] + '">' + pair[0] + '</div>\n' +
        '              <div class="change-info">\n' +
        '                <div class="change-action">' + esc(c.action) + ' &bull; ' + esc(c.company) + '</div>\n' +
        '                <div class="change-detail-row">\n' +
        '                  <span>' + esc(c.date) + '</span>\n' +
        '                  <span class="change-ticker">(' + esc(c.ticker) + ')</span>\n' +
        '                </div>\n' +
        '              </div>\n' +
        '              <div class="change-amount ' + amountClass + '">' + esc(amountHtml) + '</div>\n' +
        '            </div>'
      );
    })
    .join('\n');
  return [
    '          <!-- Recent Portfolio Changes Card -->',
    '          <div class="changes-card">',
    '            <div class="changes-title">',
    '              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>',
    '              Recent Portfolio Changes',
    '            </div>',
    items,
    '          </div>'
  ].join('\n');
}

function buildMain(inv) {
  const changes = buildChanges(inv);
  return [
    '  <!-- Main Content -->',
    '  <main>',
    '    <div class="detail-container">',
    buildBreadcrumbs(inv),
    '',
    buildHero(inv),
    '',
    buildWeighting(inv),
    '',
    '      <!-- Content Grid: Holdings + Sidebar -->',
    '      <div class="content-grid">',
    buildHoldings(inv),
    '',
    '        <!-- Sidebar (right, narrower) -->',
    '        <div>',
    buildPerf(inv),
    changes ? '\n' + changes : '',
    '        </div>',
    '      </div>',
    '',
    '      <!-- Disclaimer -->',
    '      <div class="disclaimer">',
    '        <strong>Disclaimer:</strong> ' + esc(inv.disclaimer || SEC_DISCLAIMER),
    '      </div>',
    '    </div>',
    '  </main>'
  ].join('\n');
}

const FOOTER_SCRIPT = [
  '  <script>',
  '    // Nav drawer functions',
  "    window.openSubDrawer = function() {",
  "      var main = document.getElementById('drawerMain');",
  "      var sub = document.getElementById('drawerSub');",
  "      if (main) main.style.transform = 'translateX(-100%)';",
  "      if (sub) sub.style.transform = 'translateX(0)';",
  "    };",
  "    window.closeSubDrawer = function() {",
  "      var main = document.getElementById('drawerMain');",
  "      var sub = document.getElementById('drawerSub');",
  "      if (main) main.style.transform = 'translateX(0)';",
  "      if (sub) sub.style.transform = 'translateX(-100%)';",
  "    };",
  '',
  '    // Performance toggle interactivity: swap .active between buttons and chart groups',
  "    document.querySelectorAll('.perf-toggle').forEach(function(btn) {",
  "      btn.addEventListener('click', function() {",
  "        var tf = this.getAttribute('data-perf');",
  "        document.querySelectorAll('.perf-toggle').forEach(function(b) { b.classList.remove('active'); });",
  "        document.querySelectorAll('.perf-chart-group').forEach(function(g) { g.classList.remove('active'); });",
  "        this.classList.add('active');",
  "        document.querySelectorAll('.perf-chart-group[data-perf=\"' + tf + '\"]').forEach(function(g) { g.classList.add('active'); });",
  '      });',
  '    });',
  '  </script>',
  '</body>',
  '</html>'
].join('\n');

// ─── Insights page sync ─────────────────────────────────────────────────────

function buildInvestorsArray(investors) {
  const lines = ['    const investors = ['];
  investors.forEach((inv, idx) => {
    const holdings = inv.holdings || [];
    const top3 = holdings.slice(0, 3);
    const top4 = holdings.slice(0, 4);
    const top8 = holdings.slice(0, 8);
    const extra = Math.max(0, holdings.length - 3);
    const pills = top3.map(h => JSON.stringify(h.ticker));
    if (extra > 0) pills.push(JSON.stringify('+' + extra + ' more'));
    lines.push('      {');
    lines.push('        name: ' + JSON.stringify(inv.name) + ',');
    lines.push('        pageUrl: ' + JSON.stringify('/' + inv.slug) + ',');
    lines.push('        handle: ' + JSON.stringify(inv.handle || '') + ',');
    lines.push('        category: ' + JSON.stringify(inv.category || '') + ',');
    lines.push('        categoryClass: ' + JSON.stringify(inv.slug) + ',');
    lines.push('        avatarClass: ' + JSON.stringify(inv.slug) + ',');
    lines.push('        avatarIcon: ' + JSON.stringify(inv.avatarIcon || '') + ',');
    lines.push('        donutImage: ' + JSON.stringify(inv.donutImage || '') + ',');
    lines.push('        ret: ' + JSON.stringify(fmtRet(inv.ret250)) + ',');
    lines.push('        bars: [');
    top4.forEach(h => lines.push('          { ticker: ' + JSON.stringify(h.ticker) + ', pct: ' + fmtNum(h.weight) + ', color: ' + JSON.stringify(h.color) + ' },'));
    lines.push('        ],');
    lines.push('        donutColors: [' + top8.map(h => JSON.stringify(h.color)).join(',') + '],');
    lines.push('        donutPcts: [' + top8.map(h => fmtNum(h.weight)).join(',') + '],');
    lines.push('        donutLabels: [' + top8.map(h => JSON.stringify(h.short || h.ticker)).join(',') + '],');
    lines.push('        pills: [' + pills.join(',') + '],');
    lines.push('        pillColors: [' + top3.map(h => JSON.stringify(h.color)).concat(JSON.stringify('#71717a')).join(',') + '],');
    lines.push('        donutCenter: ""');
    lines.push('      }' + (idx < investors.length - 1 ? ',' : ''));
  });
  lines.push('    ];');
  return lines.join('\n');
}

function buildColorsBlock(investors) {
  const lines = ['    /* TRADER-GEN-COLORS-START */'];
  investors.forEach(inv => {
    lines.push('    .card-avatar.' + inv.slug + ' { background: ' + inv.avatarGradient + '; color: #fff; }');
    lines.push('    .card-category.' + inv.slug + ' { color: ' + inv.categoryColor + '; }');
  });
  lines.push('    /* TRADER-GEN-COLORS-END */');
  return lines.join('\n');
}

function syncInsights(insightsHtml, investors) {
  // 1) Regenerate `const investors = [...]`
  const ARRAY_RE = /const investors = (\[[\s\S]*?\]);/;
  if (!ARRAY_RE.test(insightsHtml)) {
    console.warn('  ⚠️  build-traders: could not find `const investors = [...]` in dist/insights/index.html — array NOT regenerated');
    return insightsHtml;
  }
  const arrayBody = buildInvestorsArray(investors).replace(/^    const investors = /, '').replace(/;\s*$/, '');
  insightsHtml = insightsHtml.replace(ARRAY_RE, 'const investors = ' + arrayBody + ';');

  // 2) Refresh /* TRADER-GEN-COLORS */ block
  const START_MARK = '/* TRADER-GEN-COLORS-START */';
  const END_MARK = '/* TRADER-GEN-COLORS-END */';
  const colorsBlock = buildColorsBlock(investors);
  const startIdx = insightsHtml.indexOf(START_MARK);
  const endIdx = insightsHtml.indexOf(END_MARK);
  if (startIdx !== -1 && endIdx !== -1 && endIdx > startIdx) {
    // Markers present → replace content between them (drop the old line's leading whitespace)
    const lineStart = insightsHtml.lastIndexOf('\n', startIdx) + 1;
    insightsHtml = insightsHtml.slice(0, lineStart) + colorsBlock + insightsHtml.slice(endIdx + END_MARK.length);
  } else {
    // First run: drop stale hardcoded per-slug rules, then inject the marked block
    insightsHtml = insightsHtml.replace(/\s*\.card-(?:avatar|category)\.[A-Za-z0-9_-]+\s*\{[^}]*\}\s*/g, '\n');
    if (insightsHtml.indexOf('</style>') !== -1) {
      insightsHtml = insightsHtml.replace(/\n\s*<\/style>/, '\n' + colorsBlock + '\n  </style>');
    } else {
      insightsHtml = insightsHtml.replace('</head>', colorsBlock + '\n</head>');
    }
  }
  return insightsHtml;
}

// ─── Main ───────────────────────────────────────────────────────────────────

function main() {
  if (!fs.existsSync(DATA_PATH)) {
    console.warn('⚠️  build-traders: data/traders.json not found — skipping trader pages (exit 0)');
    return;
  }
  if (!fs.existsSync(INSIGHTS_PATH)) {
    console.warn('⚠️  build-traders: dist/insights/index.html not found — skipping trader pages (exit 0)');
    return;
  }
  if (!fs.existsSync(BACKUP_PAGE)) {
    console.warn('⚠️  build-traders: _backup_dist/buffett/index.html not found — cannot extract shared nav (exit 0)');
    return;
  }

  const traders = JSON.parse(fs.readFileSync(DATA_PATH, 'utf8'));
  const investors = (traders && traders.investors) || [];
  if (investors.length === 0) {
    console.warn('⚠️  build-traders: data/traders.json has no investors — skipping (exit 0)');
    return;
  }
  console.log('📊 Building trader pages for ' + investors.length + ' investors...');

  // Extract shared nav/drawer/search-overlay from the frozen Buffett page
  const backupHtml = fs.readFileSync(BACKUP_PAGE, 'utf8');
  const navBlock = (backupHtml.match(/<!-- Nav -->[\s\S]*?<\/nav>/) || [''])[0];
  const drawerBlock = (backupHtml.match(/<!-- Drawer -->[\s\S]*?(?=<!-- Search Overlay -->)/) || [''])[0];
  const searchBlock = (backupHtml.match(/<!-- Search Overlay -->[\s\S]*?(?=<!-- Main Content -->)/) || [''])[0];
  if (!navBlock || !drawerBlock || !searchBlock) {
    console.warn('⚠️  build-traders: could not extract nav/drawer/search blocks from _backup_dist/buffett/index.html (exit 0)');
    return;
  }

  // Stylesheet: teammate's trader-page.css if present, else the buffett page's style block
  let styleCss = null;
  if (fs.existsSync(TEMPLATE_CSS)) {
    try {
      styleCss = fs.readFileSync(TEMPLATE_CSS, 'utf8');
    } catch (e) {
      styleCss = null;
    }
  }
  if (styleCss === null) {
    const styleMatch = backupHtml.match(/<style>([\s\S]*?)<\/style>/);
    if (styleMatch) styleCss = styleMatch[1];
    console.log('  ℹ️  scripts/templates/trader-page.css not found — embedding style block extracted from _backup_dist/buffett/index.html');
  }

  // Render one page per investor
  for (const inv of investors) {
    if (!inv || !inv.slug) continue;
    const parts = [
      buildHead(inv, styleCss || ''),
      navBlock,
      drawerBlock,
      searchBlock,
      buildMain(inv),
      FOOTER_SCRIPT
    ];
    const page = parts.join('\n');
    const outDir = path.join(DIST, inv.slug);
    fs.mkdirSync(outDir, { recursive: true });
    fs.writeFileSync(path.join(outDir, 'index.html'), page);
    const lines = page.split('\n').length;
    console.log('  ✅ dist/' + inv.slug + '/index.html (' + lines + ' lines)');
  }

  // Sync insights page
  const insightsHtml = fs.readFileSync(INSIGHTS_PATH, 'utf8');
  const updated = syncInsights(insightsHtml, investors);
  if (updated !== insightsHtml) {
    fs.writeFileSync(INSIGHTS_PATH, updated);
    console.log('  ✅ dist/insights/index.html — investors array regenerated (' + investors.length + ' entries) + TRADER-GEN-COLORS block refreshed');
  } else {
    console.log('  ℹ️  dist/insights/index.html unchanged');
  }
  console.log('✅ Trader pages build complete');
}

main();
