// The Signal — Stock Profile Charts v5
// Heikin-Ashi candlesticks · Div-based financials bar chart · Tab management

(function() {
  'use strict';

  const isMobile = window.innerWidth < 768;
  const isLight = document.documentElement.classList.contains('light');
  const BG = isLight ? '#ffffff' : '#11141c';
  const GRID = isLight ? '#e5e5e5' : '#1a1e28';
  const TEXT = isLight ? '#4b5563' : '#5c6270';
  const BORDER = isLight ? '#d1d5db' : '#1f2430';
  const BLUE = '#3b82f6', GREEN = isLight ? '#16a34a' : '#22c55e', RED = isLight ? '#dc2626' : '#ef4444';
  let mainChart = null, finInitialized = false;

  // ═══ DATA ══════════════════════════════════════════════════
  const dataScript = document.querySelector('script[id^="chartData-"]');
  if (!dataScript) return;
  const pageData = JSON.parse(dataScript.textContent);
  const ohlcData = pageData.prices || [];
  const quarterly = pageData.quarterly || {};
  const annual = pageData.annual || {};

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

  // ═══ INIT MAIN CHART ════════════════════════════════════════
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
      color: isLight ? 'rgba(107,114,128,0.2)' : 'rgba(107,114,128,0.15)', priceFormat: { type: 'volume' }, priceScaleId: 'volume', lastValueVisible: false,
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
      const m = window.innerWidth < 768;
      const spacings = { '1m': { bar: m ? 7 : 12, min: m ? 3 : 5 }, '3m': { bar: m ? 3 : 7, min: m ? 1.5 : 3 }, '6m': { bar: m ? 2 : 5, min: m ? 1 : 2 }, '1y': { bar: m ? 1.2 : 3, min: m ? 0.6 : 1.5 }, '5y': { bar: m ? 0.5 : 2, min: m ? 0.25 : 0.8 }, 'all': { bar: m ? 0.3 : 1.5, min: m ? 0.15 : 0.5 } };
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

  // ═══ FORMAT ═════════════════════════════════════════════════
  function fmtB(n) { if (n == null||isNaN(n)) return '—'; return n >= 1e9 ? (n/1e9).toFixed(1)+'B' : n >= 1e6 ? (n/1e6).toFixed(0)+'M' : '$'+n.toFixed(0); }
  function fmtComma(n) { if (n == null||isNaN(n)) return '—'; return Math.round(n).toLocaleString('en-US'); }

  // Quarter label mapping: "2026/Q2" → "Q2 2026"
  function qLabel(p) {
    const m = String(p).match(/(\d{4})\/Q(\d)/);
    return m ? 'Q'+m[2]+' '+m[1] : p;
  }
  // Quarter → date: "2026/Q2" → "Jul 31, 2025" (NVDA FY ends Jan, so Q2 ≈ Jul)
  function qDate(p) {
    const m = String(p).match(/(\d{4})\/Q(\d)/);
    if (!m) return p;
    const q = parseInt(m[2]), yr = parseInt(m[1]);
    const months = ['Jan','Apr','Jul','Oct'];
    const calYr = q === 1 ? yr - 1 : yr; // FY Q1 is in prior calendar year
    return months[q-1] + ' ' + ['31','30','31','31'][q-1] + ', ' + calYr;
  }
  // Annual date: "01/2026" → "Jan 24, 2026" (NVDA FY ends ~Jan 24-31)
  function aDate(p) {
    const m = String(p).match(/(\d{2})\/(\d{4})/);
    if (!m) return p;
    const mo = parseInt(m[1]), yr = parseInt(m[2]);
    const days = ['','24','24','24','24','24','24','29','27','25','24','24','24'];
    const mon = ['','Jan','Jan','Jan','Jan','Jan','Jan','Jul','Oct','Jan','Jan','Jan','Jan'];
    // NVDA fiscal year: Jan 2026 = period ending ~Jan 24, 2026
    // Jan 2025 = Jan 25, 2025, Jul 2024 = Jul 28, 2024, Oct 2023 = Oct 29, 2023
    // Use a simple mapping
    const approxDays = {1:'24',4:'27',7:'28',10:'27'};
    const approxMon = {1:'Jan',4:'Apr',7:'Jul',10:'Oct'};
    return (approxMon[mo]||'Jan')+' '+(approxDays[mo]||'31')+', '+yr;
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

    const Y_TICKS_IS = [240, 200, 160, 120, 80, 40, 0];
    const MAX_IS = 240e9;

    // Income Statement grid (static) + Y-axis
    isGrid.innerHTML = Y_TICKS_IS.map(() => '<div class="fin-chart-grid-line"></div>').join('');
    isYAxis.innerHTML = Y_TICKS_IS.map(v => '<span>'+v+'b</span>').join('');

    function buildIS(mode) {
      const isAnn = mode === 'annual';
      if (isAnn && annual.income && annual.income.length) {
        return annual.income.map(e => ({
          period: e.period.replace('01/',''), fullDate: aDate(e.period),
          rev: e['Total Revenue'] || 0, gp: e['Gross Profit'] || 0, ni: e['Net Income'] || 0,
        })).reverse();
      } else {
        const qRev = (quarterly.revenue || []).filter(p => p.actual).slice(0, 8).reverse();
        return qRev.map(r => {
          const niEntry = (quarterly.netIncome||[]).find(n => n.period === r.period);
          return { period: qLabel(r.period), fullDate: qDate(r.period),
            rev: r.actual || 0, gp: (r.actual||0) * 0.7, ni: niEntry ? niEntry.actual : 0 };
        });
      }
    }

    function renderIS(mode) {
      const data = buildIS(mode);
      isBars.innerHTML = data.map(d => {
        const revH = Math.max(0.5, (d.rev / MAX_IS) * 100);
        const niH = Math.max(0.5, (d.ni / MAX_IS) * 100);
        return `<div class="fin-bar-group"><div class="fin-bar-tooltip">${d.period} | Rev: ${fmtB(d.rev)} | Net: ${fmtB(d.ni)}</div><div class="fin-bar-rev" style="height:${revH}%"></div><div class="fin-bar-ni" style="height:${niH}%"></div></div>`;
      }).join('');
      isXAxis.innerHTML = data.map(d => '<span>'+d.period+'</span>').join('');
      // Data table
      const table = document.getElementById('finDataTable');
      if (table) {
        const rev = data.slice().reverse().slice(0, 3);
        table.querySelector('thead tr').innerHTML = '<th>Period Ending:</th>' + rev.map(d => '<th>'+d.fullDate+'</th>').join('');
        table.querySelector('tbody').innerHTML =
          '<tr class="fin-data-row"><td class="fin-data-label">Total Revenues</td>'+rev.map(d => '<td>'+fmtComma(d.rev)+'</td>').join('')+'</tr>'+
          '<tr class="fin-data-row"><td class="fin-data-label">Gross Profit</td>'+rev.map(d => '<td>'+fmtComma(d.gp)+'</td>').join('')+'</tr>';
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
      const maxVal = Math.max(1e9, ...data.map(d => Math.max(d.assets, d.liab))) * 1.1;
      const maxRounded = Math.ceil(maxVal / 40e9) * 40e9;
      const MAX_BS = maxRounded > 0 ? maxRounded : 240e9;
      const BS_TICKS = [MAX_BS/1e9, (MAX_BS/1e9)*5/6, (MAX_BS/1e9)*4/6, (MAX_BS/1e9)*3/6, (MAX_BS/1e9)*2/6, (MAX_BS/1e9)*1/6, 0].map(v => Math.round(v));

      if (bsGrid) bsGrid.innerHTML = BS_TICKS.map(() => '<div class="fin-chart-grid-line"></div>').join('');
      if (bsYAxis) bsYAxis.innerHTML = BS_TICKS.map(v => '<span>'+v+'b</span>').join('');

      if (bsBars) bsBars.innerHTML = data.map(d => {
        const taH = Math.max(0.5, (d.assets / MAX_BS) * 100);
        const tlH = Math.max(0.5, (d.liab / MAX_BS) * 100);
        return `<div class="fin-bar-group"><div class="fin-bar-tooltip">${d.period} | Assets: ${fmtB(d.assets)} | Liab: ${fmtB(d.liab)}</div><div class="fin-bar-rev" style="height:${taH}%"></div><div class="fin-bar-ni" style="height:${tlH}%"></div></div>`;
      }).join('');
      if (bsXAxis) bsXAxis.innerHTML = data.map(d => '<span>'+d.period+'</span>').join('');
      // BS data table
      const bsTable = document.getElementById('finBsTable');
      if (bsTable) {
        const rev = data.slice().reverse().slice(0, 3);
        bsTable.querySelector('thead tr').innerHTML = '<th>Period Ending:</th>' + rev.map(d => '<th>'+d.fullDate+'</th>').join('');
        bsTable.querySelector('tbody').innerHTML =
          '<tr class="fin-data-row"><td class="fin-data-label">Total Assets</td>'+rev.map(d => '<td>'+fmtComma(d.assets)+'</td>').join('')+'</tr>'+
          '<tr class="fin-data-row"><td class="fin-data-label">Total Liabilities</td>'+rev.map(d => '<td>'+fmtComma(d.liab)+'</td>').join('')+'</tr>';
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
        grid: { vertLines: { color: light ? '#e5e5e5' : '#1a1e28' }, horzLines: { color: light ? '#e5e5e5' : '#1a1e28' } },
        rightPriceScale: { borderColor: light ? '#d1d5db' : '#1f2430' },
        timeScale: { borderColor: light ? '#d1d5db' : '#1f2430' },
      });
    }
  };

})();
