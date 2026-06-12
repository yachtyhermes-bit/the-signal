// The Signal — Stock Profile Charts v4
// Heikin-Ashi candlesticks · Financials bar chart · Tab management

(function() {
  'use strict';

  const isMobile = window.innerWidth < 768;
  const BG = '#11141c', GRID = '#1a1e28', TEXT = '#5c6270', BORDER = '#1f2430';
  const BLUE = '#3b82f6', GREEN = '#22c55e', RED = '#ef4444';
  let mainChart = null, finChart = null;
  let finInitialized = false;

  // ═══ DATA ══════════════════════════════════════════════════
  const dataScript = document.querySelector('script[id^="chartData-"]');
  if (!dataScript) return;
  const pageData = JSON.parse(dataScript.textContent);
  const ohlcData = pageData.prices || [];
  const quarterly = pageData.quarterly || {};

  // ═══ HEIKIN-ASHI ═══════════════════════════════════════════
  function computeHeikinAshi(data) {
    const ha = [];
    for (let i = 0; i < data.length; i++) {
      const hc = (data[i].open + data[i].high + data[i].low + data[i].close) / 4;
      const ho = i === 0 ? (data[i].open + data[i].close) / 2 : (ha[i-1].open + ha[i-1].close) / 2;
      ha.push({ time: data[i].time, open: ho, high: Math.max(data[i].high, ho, hc), low: Math.min(data[i].low, ho, hc), close: hc });
    }
    return ha;
  }

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

  // ═══ INIT MAIN CHART (always visible) ════════════════════════
  function initMainChart() {
    const chartEl = document.getElementById('stockChart');
    if (!chartEl || !ohlcData.length) return;

    const rawOHLC = ohlcData.map(d => ({ time: d.time, open: d.open, high: d.high, low: d.low, close: d.close }));
    const heikinAshi = computeHeikinAshi(rawOHLC);

    mainChart = window.LightweightCharts.createChart(chartEl, {
      layout: { background: { type: 'solid', color: BG }, textColor: TEXT },
      grid: { vertLines: { color: GRID, style: 1 }, horzLines: { color: GRID, style: 1 } },
      crosshair: { mode: 0 },
      rightPriceScale: { borderColor: BORDER, scaleMargins: { top: 0.12, bottom: 0.05 } },
      timeScale: { borderColor: BORDER, timeVisible: true },
      width: chartEl.clientWidth,
      height: isMobile ? 340 : 480,
      handleScroll: { vertTouchDrag: false },
      handleScale: { axisPressedMouseMove: true },
    });

    const candleSeries = mainChart.addCandlestickSeries({
      upColor: GREEN, downColor: RED, borderUpColor: GREEN, borderDownColor: RED, wickUpColor: GREEN, wickDownColor: RED,
    });

    const volumeSeries = mainChart.addHistogramSeries({
      color: 'rgba(107,114,128,0.15)', priceFormat: { type: 'volume' }, priceScaleId: 'volume', lastValueVisible: false,
    });
    mainChart.priceScale('volume').applyOptions({ scaleMargins: { top: 0.82, bottom: 0 } });

    function setChartData(tf) {
      const haFiltered = filterByTF(heikinAshi, tf);
      const rawFiltered = filterByTF(ohlcData, tf);
      candleSeries.setData(haFiltered);
      volumeSeries.setData(rawFiltered.map(d => ({
        time: d.time, value: d.volume || 0,
        color: d.close >= d.open ? 'rgba(34,197,94,0.12)' : 'rgba(239,68,68,0.1)',
      })));
      // Adaptive bar spacing: compress bars for longer timeframes
      const m = window.innerWidth < 768;
      const spacings = { '1m': { bar: m ? 7 : 12, min: m ? 3 : 5 }, '3m': { bar: m ? 3 : 7, min: m ? 1.5 : 3 }, '6m': { bar: m ? 2 : 5, min: m ? 1 : 2 }, '1y': { bar: m ? 1.2 : 3, min: m ? 0.6 : 1.5 }, '5y': { bar: m ? 0.5 : 2, min: m ? 0.25 : 0.8 }, 'all': { bar: m ? 0.3 : 1.5, min: m ? 0.15 : 0.5 } };
      const s = spacings[tf] || spacings['1y'];
      mainChart.timeScale().applyOptions({ barSpacing: s.bar, minBarSpacing: s.min, fixLeftEdge: true });
      mainChart.timeScale().fitContent();
    }

    setChartData('1m');

    // Timeframe buttons
    document.querySelectorAll('.tf-btn').forEach(btn => {
      btn.addEventListener('click', () => {
        document.querySelectorAll('.tf-btn').forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        setChartData(btn.dataset.tf);
      });
    });

    // Tooltip
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

  // ═══ INIT FINANCIALS CHART (lazy — only when tab activated) ═══
  function initFinChart() {
    if (finInitialized) return;
    const finEl = document.getElementById('finChart');
    if (!finEl) return;
    // Force explicit height so chart renders properly inside hidden tab
    const isMob = window.innerWidth < 768;
    finEl.style.height = (isMob ? '320px' : '400px');

    const revData = quarterly.revenue || [];
    const niData = quarterly.netIncome || [];

    function buildData(mode) {
      const isQ = mode !== 'annual';
      const rev = [], ni = [];
      const revSrc = isQ ? revData.slice(0, 20).reverse() : aggregateAnnual(revData);
      const niSrc = isQ ? niData.slice(0, 20).reverse() : aggregateAnnual(niData);
      // Convert period to valid Lightweight Charts time format
      function toTime(period) {
        if (period.includes('/')) {
          // "2026/Q2" → "2026-04-01"
          const [yr, qt] = period.split('/');
          const m = { Q1: '01', Q2: '04', Q3: '07', Q4: '10' }[qt] || '01';
          return yr + '-' + m + '-01';
        }
        // Annual: "2026" → "2026-01-01"
        return period + '-01-01';
      }
      for (const p of revSrc) rev.push({ time: toTime(p.period), value: p.actual || 0 });
      for (const p of niSrc) ni.push({ time: toTime(p.period), value: p.actual || 0 });
      return { rev, ni };
    }

    function aggregateAnnual(data) {
      const a = {};
      for (const d of data) {
        if (!d.actual) continue;
        const yr = d.period.split('/')[0];
        a[yr] = (a[yr] || 0) + d.actual;
      }
      return Object.entries(a).sort(([a],[b]) => a.localeCompare(b)).map(([p, v]) => ({ period: p, actual: v }));
    }

    const { rev, ni } = buildData('quarterly');

    finChart = window.LightweightCharts.createChart(finEl, {
      layout: { background: { type: 'solid', color: BG }, textColor: TEXT },
      grid: { vertLines: { color: GRID, style: 1 }, horzLines: { color: GRID, style: 1 } },
      rightPriceScale: { borderColor: BORDER },
      timeScale: { borderColor: BORDER, timeVisible: true, fixLeftEdge: true, barSpacing: isMob ? 18 : 28, minBarSpacing: isMob ? 8 : 12 },
      width: finEl.clientWidth,
      height: parseInt(finEl.style.height) || 380,
    });

    const revSeries = finChart.addHistogramSeries({ color: BLUE });
    const niSeries = finChart.addHistogramSeries({ color: 'rgba(156,163,175,0.6)' });

    revSeries.setData(rev);
    niSeries.setData(ni);
    finChart.timeScale().fitContent();

    document.querySelectorAll('.fin-toggle-btn').forEach(btn => {
      btn.addEventListener('click', () => {
        document.querySelectorAll('.fin-toggle-btn').forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        const { rev: rp, ni: np } = buildData(btn.dataset.mode);
        revSeries.setData(rp);
        niSeries.setData(np);
        finChart.timeScale().fitContent();
      });
    });

    window.addEventListener('resize', () => {
      if (finChart) {
        const m = window.innerWidth < 768;
        finEl.style.height = (m ? '320px' : '400px');
        finChart.applyOptions({ width: finEl.clientWidth, height: parseInt(finEl.style.height) });
      }
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

      // Lazy-init financials chart when tab is first opened
      if (tab.dataset.tab === 'financials') {
        setTimeout(initFinChart, 50);
      }

      // Resize main chart if switching to chart tab
      if (tab.dataset.tab === 'overview' && chartEl) {
        setTimeout(() => {
          const el = document.getElementById('stockChart');
          if (el) mainChart.applyOptions({ width: el.clientWidth });
        }, 50);
      }
    });
  });

  // ═══ STARTUP ════════════════════════════════════════════════
  initMainChart();

  // If financials tab is somehow active at load, init it
  if (document.getElementById('tab-financials')?.classList.contains('active')) {
    setTimeout(initFinChart, 100);
  }

})();
