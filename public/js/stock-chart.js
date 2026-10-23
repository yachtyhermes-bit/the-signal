// The Signal — Stock Profile Charts v6

(function() {
  'use strict';

  const isMobile = window.innerWidth < 768;
  const isLight = document.documentElement.classList.contains('light');
  const BG = isLight ? '#ffffff' : '#11141c';
  const GRID = isLight ? '#f0f0f0' : '#18202e';
  const TEXT = isLight ? '#4b5563' : '#5c6270';
  const BORDER = isLight ? '#d1d5db' : '#1f2430';
  const BLUE = '#3b82f6', GREEN = '#089981', RED = '#f23645';
  let mainChart = null, candleSeries = null, finInitialized = false, livePriceLine = null;

  // ═══ DATA ══════════════════════════════════════════════════
  const dataScript = document.querySelector('script[id^="chartData-"]');
  if (!dataScript) return;
  const pageData = JSON.parse(dataScript.textContent);
  const ohlcData = (pageData.prices || []).filter(d => d.open != null && d.high != null && d.low != null && d.close != null);
  const quarterly = pageData.quarterly || {};
  const annual = pageData.annual || {};

  function filterByTF(data, tf) {
    const now = new Date();
    let cutoff;
    switch (tf) {
      case '1m': cutoff = new Date(now.getFullYear(), now.getMonth()-1, now.getDate()); break;
      case '3m': cutoff = new Date(now.getFullYear(), now.getMonth()-3, now.getDate()); break;
      case '6m': cutoff = new Date(now.getFullYear(), now.getMonth()-6, now.getDate()); break;
      case '1y': cutoff = new Date(now.getFullYear()-1, now.getMonth(), now.getDate()); break;
      case '5y': cutoff = new Date(now.getFullYear()-5, now.getMonth(), now.getDate()); break;
      default: return data;
    }
    return data.filter(d => new Date(d.time) >= cutoff);
  }

  // ═══ INIT MAIN CHART ════════════════════════════════════════
  function initMainChart() {
    const chartEl = document.getElementById('stockChart');
    if (!chartEl || !ohlcData.length) return;

    const rawOHLC = ohlcData.map(d => ({ time: d.time, open: d.open, high: d.high, low: d.low, close: d.close }));

    mainChart = window.LightweightCharts.createChart(chartEl, {
      layout: { background: { type: 'solid', color: BG }, textColor: TEXT },
      grid: { vertLines: { color: GRID, style: 1 }, horzLines: { color: GRID, style: 1 } },
      crosshair: { mode: 0 },
      rightPriceScale: { borderColor: BORDER, scaleMargins: { top: 0.12, bottom: 0.05 }, visible: true, entireTextOnly: false, minimumWidth: 60 },
      timeScale: { borderColor: BORDER, timeVisible: true },
      width: chartEl.clientWidth,
      height: isMobile ? 340 : 480,
      handleScroll: { vertTouchDrag: false },
      handleScale: { axisPressedMouseMove: true },
    });

    candleSeries = mainChart.addCandlestickSeries({
      upColor: GREEN, downColor: RED, wickUpColor: GREEN, wickDownColor: RED,
      lastValueVisible: true,
      priceLineVisible: false,
      priceFormat: { type: 'price', minMove: 0.01 },
    });

    const volumeSeries = mainChart.addHistogramSeries({
      color: isLight ? 'rgba(107,114,128,0.2)' : 'rgba(107,114,128,0.15)', priceFormat: { type: 'volume' }, priceScaleId: 'volume', lastValueVisible: false,
    });
    mainChart.priceScale('volume').applyOptions({ scaleMargins: { top: 0.82, bottom: 0 } });

    function setChartData(tf) {
      const rawFiltered = filterByTF(ohlcData, tf);
      candleSeries.setData(rawFiltered);
      volumeSeries.setData(rawFiltered.map(d => ({
        time: d.time, value: d.volume || 0,
        color: d.close >= d.open ? 'rgba(34,197,94,0.12)' : 'rgba(239,68,68,0.1)',
      })));

      const m = window.innerWidth < 768;
      const spacings = { '1m': { bar: m ? 5 : 10, min: m ? 2 : 4 }, '3m': { bar: m ? 2.5 : 6, min: m ? 1 : 2.5 }, '6m': { bar: m ? 1.5 : 4, min: m ? 0.7 : 1.5 }, '1y': { bar: m ? 0.9 : 2.5, min: m ? 0.4 : 1 }, '5y': { bar: m ? 0.4 : 1.5, min: m ? 0.2 : 0.6 }, 'all': { bar: m ? 0.25 : 1, min: m ? 0.1 : 0.4 } };
      const s = spacings[tf] || spacings['1y'];
      mainChart.timeScale().applyOptions({ barSpacing: s.bar, minBarSpacing: s.min, fixLeftEdge: true });
      mainChart.timeScale().fitContent();
    }

    setChartData('1m');

    document.querySelectorAll('.tf-btn').forEach(btn => {
      btn.addEventListener('click', () => {
        document.querySelectorAll('.tf-btn').forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        setChartData(btn.dataset.tf);
      });
    });

    const tooltip = document.createElement('div');
    tooltip.className = 'chart-tooltip';
    chartEl.style.position = 'relative';
    chartEl.appendChild(tooltip);

    mainChart.subscribeCrosshairMove(param => {
      if (!param.point || !param.time || !param.seriesData) { tooltip.style.display = 'none'; return; }
      const d = param.seriesData.get(candleSeries);
      if (!d) { tooltip.style.display = 'none'; return; }
      tooltip.style.display = 'block';
      tooltip.style.left = Math.min(param.point.x + 12, chartEl.clientWidth - 120) + 'px';
      tooltip.style.top = Math.max(param.point.y - 65, 5) + 'px';
      tooltip.innerHTML = `<div style="color:#9ca3af;margin-bottom:2px">${d.time}</div>
        <div style="display:grid;grid-template-columns:14px 1fr;gap:2px 8px">
        <span style="color:#9ca3af">O</span><span style="color:#e5e7eb;font-weight:600">${d.open.toFixed(2)}</span>
        <span style="color:#9ca3af">H</span><span style="color:#e5e7eb;font-weight:600">${d.high.toFixed(2)}</span>
        <span style="color:#9ca3af">L</span><span style="color:#e5e7eb;font-weight:600">${d.low.toFixed(2)}</span>
        <span style="color:#9ca3af">C</span><span style="color:${d.close>=d.open?GREEN:RED};font-weight:600">${d.close.toFixed(2)}</span></div>`;
    });

    window.addEventListener('resize', () => {
      if (!mainChart) return;
      const m = window.innerWidth < 768;
      mainChart.applyOptions({ width: chartEl.clientWidth, height: m ? 340 : 480 });
    });
  }

  // ═══ LIVE PRICE LINE ═══════════════════════════════════════
  window._updateLivePriceLine = function(price) {
    if (!candleSeries) return;
    if (livePriceLine) candleSeries.removePriceLine(livePriceLine);
    livePriceLine = candleSeries.createPriceLine({
      price: price,
      color: RED + '80',
      lineWidth: 1,
      lineStyle: 2,
      axisLabelVisible: true,
      title: 'Live',
    });
  };
  if (pageData.currentPrice != null) {
    window._updateLivePriceLine(pageData.currentPrice);
  }

  // ═══ FORMAT ═════════════════════════════════════════════════
  function fmtB(n) { if (n == null||isNaN(n)) return '—'; const sign = n < 0 ? '-' : ''; const abs = Math.abs(n); return sign + (abs >= 1e9 ? (abs/1e9).toFixed(1)+'B' : abs >= 1e6 ? (abs/1e6).toFixed(0)+'M' : '$'+abs.toFixed(0)); }
  function fmtComma(n) { if (n == null||isNaN(n)) return '—'; return Math.round(n).toLocaleString('en-US'); }
  function getSnapUnit(val) { if (val >= 100e9) return 20e9; if (val >= 10e9) return 5e9; if (val >= 1e9) return 1e9; if (val >= 100e6) return 100e6; if (val >= 10e6) return 10e6; return 1e6; }
  function fmtTick(n) { if (n === 0) return '0'; if (n >= 1e12) return parseFloat((n/1e12).toFixed(1))+'T'; if (n >= 1e9) return parseFloat((n/1e9).toFixed(1))+'B'; if (n >= 1e6) return parseFloat((n/1e6).toFixed(0))+'M'; return parseFloat((n/1e3).toFixed(0))+'K'; }

  // ── Shared grouped-bar renderer: paired bars anchored on a zero baseline ──
  function niceTicks(min, max) {
    const span = (max - min) || 1;
    const raw = span / 4;
    const mag = Math.pow(10, Math.floor(Math.log10(raw)));
    const norm = raw / mag;
    const step = (norm <= 1 ? 1 : norm <= 2 ? 2 : norm <= 2.5 ? 2.5 : norm <= 5 ? 5 : 10) * mag;
    const start = Math.floor(min / step) * step;
    const end = Math.ceil(max / step) * step;
    const out = [];
    for (let v = start; v <= end + step * 0.001; v += step) out.push(Math.round(v));
    return out.length > 1 ? out : [min, max];
  }
  function axisMoney(v) { return (v < 0 ? '-$' : '$') + fmtTick(Math.abs(v)); }

  function drawFinChart(areaEl, rows, opts) {
    if (!areaEl || !rows.length) return;
    areaEl.querySelectorAll('svg.fin-chart-svg').forEach(n => n.remove());
    const W = Math.max(240, areaEl.clientWidth || 320);
    const H = Math.max(150, areaEl.clientHeight || 260);
    const rotate = rows.length > 4;
    const m = { t: 12, r: 10, b: rotate ? 46 : 26, l: 52 };
    const plotW = W - m.l - m.r;
    const plotH = H - m.t - m.b;
    const all = [];
    rows.forEach(r => { all.push(r.a, r.b); });
    const ticks = niceTicks(Math.min(0, Math.min.apply(null, all)), Math.max(0, Math.max.apply(null, all)));
    const min = Math.min(ticks[0], 0);
    const max = Math.max(ticks[ticks.length - 1], 0);
    const y = v => m.t + (1 - (v - min) / ((max - min) || 1)) * plotH;
    const NS = 'http://www.w3.org/2000/svg';

    const svg = document.createElementNS(NS, 'svg');
    svg.setAttribute('class', 'fin-chart-svg');
    svg.setAttribute('viewBox', '0 0 ' + W + ' ' + H);
    svg.setAttribute('role', 'img');
    svg.setAttribute('aria-label', (opts.aLabel || 'Series A') + ' and ' + (opts.bLabel || 'Series B') + ' by period');
    areaEl.appendChild(svg);

    ticks.forEach(v => {
      if (v !== 0) {
        const g = document.createElementNS(NS, 'line');
        g.setAttribute('class', 'fc-grid');
        g.setAttribute('x1', m.l); g.setAttribute('x2', W - m.r);
        g.setAttribute('y1', y(v)); g.setAttribute('y2', y(v));
        svg.appendChild(g);
      }
      const t = document.createElementNS(NS, 'text');
      t.setAttribute('class', v === 0 ? 'fc-tick fc-zero' : 'fc-tick');
      t.setAttribute('x', m.l - 8); t.setAttribute('y', y(v) + 4);
      t.setAttribute('text-anchor', 'end');
      t.textContent = v === 0 ? '$0' : axisMoney(v);
      svg.appendChild(t);
    });

    const zero = document.createElementNS(NS, 'line');
    zero.setAttribute('class', 'fc-zero-line');
    zero.setAttribute('x1', m.l); zero.setAttribute('x2', W - m.r);
    zero.setAttribute('y1', y(0)); zero.setAttribute('y2', y(0));
    svg.appendChild(zero);

    const groupW = plotW / rows.length;
    const pairW = Math.min(groupW * 0.62, 60);
    const barW = pairW / 2;

    rows.forEach((r, i) => {
      const x0 = m.l + i * groupW + (groupW - pairW) / 2;
      [[r.a, 'fc-bar-a', opts.aLabel], [r.b, 'fc-bar-b', opts.bLabel]].forEach((sp, j) => {
        const val = sp[0];
        if (val === null || val === undefined || isNaN(val)) return;
        const top = Math.min(y(val), y(0));
        const h = Math.max(2, Math.abs(y(val) - y(0)));
        const rect = document.createElementNS(NS, 'rect');
        rect.setAttribute('class', sp[1]);
        rect.setAttribute('x', x0 + j * barW - (j ? 0.6 : 0));
        rect.setAttribute('y', top);
        rect.setAttribute('width', barW + (j ? 0.6 : 0));
        rect.setAttribute('height', h);
        const title = document.createElementNS(NS, 'title');
        title.textContent = r.label + ' · ' + sp[2] + ' ' + fmtB(val);
        rect.appendChild(title);
        svg.appendChild(rect);
      });
      const lab = document.createElementNS(NS, 'text');
      lab.setAttribute('class', 'fc-tick');
      const lx = x0 + pairW / 2;
      const ly = H - m.b + 14;
      lab.setAttribute('x', lx); lab.setAttribute('y', ly);
      lab.setAttribute('text-anchor', rotate ? 'end' : 'middle');
      if (rotate) lab.setAttribute('transform', 'rotate(-40 ' + lx + ' ' + ly + ')');
      lab.textContent = r.label;
      svg.appendChild(lab);
    });
  }

  // Quarter label mapping: "2026/Q2" → "Q2 2026"
  function qLabel(p) {
    const m = String(p).match(/(\d{4})\/Q(\d)/);
    return m ? 'Q'+m[2]+' '+m[1] : p;
  }
  // Period labels: never invent a calendar date. A fiscal period is shown as
  // the fiscal quarter / month it actually is, so MU (Aug FY) is not stamped "Jan".
  function qDate(p) { return qLabel(p); }
  function aDate(p) {
    const m = String(p).match(/(\d{2})\/(\d{4})/);
    if (!m) return p;
    const mon = ['', 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
    return (mon[parseInt(m[1], 10)] || '') + ' ' + m[2];
  }

  // ═══ INIT FINANCIALS CHARTS ════════════════════════════════
  function initFinChart() {
    if (finInitialized) return;

    // ── Income Statement ──
    const isGrid = document.getElementById('finChartGrid');
    const isBars = document.getElementById('finChartBars');
    const isYAxis = document.getElementById('finChartYAxis');
    const isXAxis = document.getElementById('finChartXAxis');

    // ── Balance Sheet ──
    const bsGrid = document.getElementById('finBsGrid');
    const bsBars = document.getElementById('finBsBars');
    const bsYAxis = document.getElementById('finBsYAxis');
    const bsXAxis = document.getElementById('finBsXAxis');

    if (!isGrid || !isBars) return;

    // ── Income Statement ──
    function buildIS(mode) {
      const isAnn = mode === 'annual';
      if (isAnn && annual.income && annual.income.length) {
        return annual.income.map(e => ({
          period: e.period.replace(/^\d{2}\//,''), fullDate: aDate(e.period),
          rev: e['Total Revenue'] || 0, gp: e['Gross Profit'] || 0, ni: e['Net Income'] || 0,
        })).reverse();
      } else {
        const qRev = (quarterly.revenue || []).filter(p => p.actual).slice(0, 8).reverse();
        return qRev.map(r => {
          const niEntry = (quarterly.netIncome||[]).find(n => n.period === r.period);
          return { period: qLabel(r.period), fullDate: qDate(r.period),
            rev: r.actual || 0, gp: null, ni: niEntry ? niEntry.actual : 0 };
        });
      }
    }

    function renderIS(mode) {
      const data = buildIS(mode);
      if (!data.length) return;
      isGrid.innerHTML = ''; isYAxis.innerHTML = ''; isXAxis.innerHTML = ''; isBars.innerHTML = '';
      drawFinChart(isBars.parentElement, data.map(d => ({ label: d.period, a: d.rev, b: d.ni })),
        { aLabel: 'Total Revenues', bLabel: 'Net Income' });

      const table = document.getElementById('finDataTable');
      if (table) {
        const rows = data.slice().reverse().slice(0, 3);
        const showGp = rows.some(d => d.gp !== null && d.gp !== undefined);
        table.querySelector('thead tr').innerHTML = '<th>Period:</th>' + rows.map(d => '<th>'+d.fullDate+'</th>').join('');
        let html = '<tr class="fin-data-row"><td class="fin-data-label">Total Revenues</td>' +
          rows.map(d => '<td>'+fmtComma(d.rev)+'</td>').join('') + '</tr>';
        if (showGp) {
          html += '<tr class="fin-data-row"><td class="fin-data-label">Gross Profit</td>' +
            rows.map(d => '<td>'+(d.gp == null ? '—' : fmtComma(d.gp))+'</td>').join('') + '</tr>';
        }
        html += '<tr class="fin-data-row"><td class="fin-data-label">Net Income</td>' +
          rows.map(d => '<td'+(d.ni < 0 ? ' class="neg"' : '')+'>'+fmtComma(d.ni)+'</td>').join('') + '</tr>';
        table.querySelector('tbody').innerHTML = html;
      }
    }

    // ── Balance Sheet ──
    function buildBS(mode) {
      const isAnn = mode === 'annual';
      if (isAnn && annual.balance && annual.balance.length) {
        return annual.balance.map(e => ({
          period: e.period.replace(/^\d{2}\//,''), fullDate: aDate(e.period),
          assets: e['Total Assets'] || 0, liab: e['Total Liabilities'] || 0,
        })).reverse();
      } else {
        const qAssets = (quarterly.totalAssets || []).filter(p => p.actual).slice(0, 8).reverse();
        return qAssets.map(a => {
          const lEntry = (quarterly.totalLiabilities||[]).find(l => l.period === a.period);
          return { period: qLabel(a.period), fullDate: qDate(a.period),
            assets: a.actual || 0, liab: lEntry ? lEntry.actual : 0 };
        });
      }
    }

    function renderBS(mode) {
      const data = buildBS(mode);
      if (!data.length) return;
      if (bsGrid) bsGrid.innerHTML = '';
      if (bsYAxis) bsYAxis.innerHTML = '';
      if (bsXAxis) bsXAxis.innerHTML = '';
      if (bsBars) {
        bsBars.innerHTML = '';
        drawFinChart(bsBars.parentElement, data.map(d => ({ label: d.period, a: d.assets, b: d.liab })),
          { aLabel: 'Total Assets', bLabel: 'Total Liabilities' });
      }

      const bsTable = document.getElementById('finBsTable');
      if (bsTable) {
        const rows = data.slice().reverse().slice(0, 3);
        bsTable.querySelector('thead tr').innerHTML = '<th>Period:</th>' + rows.map(d => '<th>'+d.fullDate+'</th>').join('');
        bsTable.querySelector('tbody').innerHTML =
          '<tr class="fin-data-row"><td class="fin-data-label">Total Assets</td>'+rows.map(d => '<td>'+fmtComma(d.assets)+'</td>').join('')+'</tr>'+
          '<tr class="fin-data-row"><td class="fin-data-label">Total Liabilities</td>'+rows.map(d => '<td>'+fmtComma(d.liab)+'</td>').join('')+'</tr>';
      }
    }

    // Initial renders
    renderIS('annual');
    renderBS('annual');

    // Toggle buttons — Income Statement
    document.querySelectorAll('.fin-toggle-btn').forEach(btn => {
      btn.addEventListener('click', () => {
        document.querySelectorAll('.fin-toggle-btn').forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        renderIS(btn.dataset.mode);
      });
    });

    // Toggle buttons — Balance Sheet
    document.querySelectorAll('.fin-toggle-btn-bs').forEach(btn => {
      btn.addEventListener('click', () => {
        document.querySelectorAll('.fin-toggle-btn-bs').forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        renderBS(btn.dataset.mode);
      });
    });

    finInitialized = true;
  }

  // ═══ TAB SWITCHING ══════════════════════════════════════════
  document.querySelectorAll('.stock-tab').forEach(tab => {
    tab.addEventListener('click', () => {
      document.querySelectorAll('.stock-tab').forEach(t => t.classList.remove('active'));
      document.querySelectorAll('.stock-tab-panel').forEach(p => p.classList.remove('active'));
      tab.classList.add('active');
      const target = document.getElementById('tab-' + tab.dataset.tab);
      if (target) target.classList.add('active');

      if (tab.dataset.tab === 'financials') {
        setTimeout(initFinChart, 100);
      }

      if (tab.dataset.tab === 'overview') {
        setTimeout(() => {
          const el = document.getElementById('stockChart');
          if (el && mainChart) mainChart.applyOptions({ width: el.clientWidth });
        }, 50);
      }
    });
  });

  // ═══ STARTUP ════════════════════════════════════════════════
  initMainChart();

  if (document.getElementById('tab-financials')?.classList.contains('active')) {
    setTimeout(initFinChart, 150);
  }

  // ═══ THEME UPDATE ═══════════════════════════════════════════
  window._updateChartTheme = function() {
    if (mainChart) {
      const light = document.documentElement.classList.contains('light');
      mainChart.applyOptions({
        layout: { background: { type: 'solid', color: light ? '#ffffff' : '#11141c' }, textColor: light ? '#4b5563' : '#5c6270' },
        grid: { vertLines: { color: light ? '#f0f0f0' : '#18202e' }, horzLines: { color: light ? '#f0f0f0' : '#18202e' } },
        rightPriceScale: { borderColor: light ? '#d1d5db' : '#1f2430' },
        timeScale: { borderColor: light ? '#d1d5db' : '#1f2430' },
      });
    }
  };

  // ═══ LIVE PRICE UPDATER ════════════════════════════════════
  (function() {
    var INTERVAL = 300000;
    function fmt(n) {
      if (n == null || isNaN(n)) return '---';
      return n.toLocaleString('en-US', {minimumFractionDigits:2, maximumFractionDigits:2});
    }
    function update(prices) {
      document.querySelectorAll('[data-price]').forEach(function(el) {
        var sym = el.getAttribute('data-price');
        var d = prices[sym];
        if (d && d.price != null) el.textContent = '$' + fmt(d.price);
      });
      document.querySelectorAll('[data-change]').forEach(function(el) {
        var sym = el.getAttribute('data-change');
        var d = prices[sym];
        if (d && d.changePercent != null) {
          var pct = d.changePercent;
          el.textContent = (pct >= 0 ? '▲ ' : '▼ ') + Math.abs(pct).toFixed(2) + '%';
          el.className = el.className.replace(/positive|negative/g,'').trim() + ' ' + (pct >= 0 ? 'positive' : 'negative');
        }
      });
    }
    function refresh() {
      fetch('/api/prices/')
        .then(function(r) { return r.json(); })
        .then(function(data) {
          var px = data.prices || data;
          update(px);
          // Sync chart live price line
          var symEl = document.querySelector('[data-price]');
          if (symEl && window._updateLivePriceLine) {
            var sym = symEl.getAttribute('data-price');
            if (px[sym] && px[sym].price != null) {
              window._updateLivePriceLine(px[sym].price);
            }
          }
        })
        .catch(function(){});
    }
    refresh();
    setInterval(refresh, INTERVAL);
  })();

})();
