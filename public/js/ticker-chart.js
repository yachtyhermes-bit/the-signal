// Ticker Chart — TradingView Lightweight Charts (script-tag approach)
// OHLC Bar Chart with multiple timeframes
// Loaded AFTER lightweight-charts CDN script

function initTickerChart(ticker) {
  if (typeof LightweightCharts === 'undefined') {
    console.error('LightweightCharts library not loaded');
    return;
  }
  const { createChart } = LightweightCharts;

  const scriptEl = document.getElementById('chartData-' + ticker);
  if (!scriptEl) {
    console.error('No chart data found for ' + ticker);
    return;
  }

  let fullChartData;
  try {
    fullChartData = JSON.parse(scriptEl.textContent);
  } catch (e) {
    console.error('Failed to parse chart data:', e);
    return;
  }

  if (!fullChartData || !fullChartData.length) {
    console.error('Empty chart data');
    return;
  }

  // Parse OHLC data
  const parsedData = fullChartData.map(function(d) {
    return {
      time: d.time,
      open: d.open,
      high: d.high,
      low: d.low,
      close: d.close,
      date: new Date(d.time + 'T00:00:00')
    };
  });

  var container = document.getElementById('tickerChart');
  if (!container) {
    console.error('No chart container found');
    return;
  }

  container.innerHTML = '';

  var chart = createChart(container, {
    layout: {
      background: { type: 'solid', color: '#0f0f20' },
      textColor: '#9ca3af',
      fontFamily: 'Inter, sans-serif',
    },
    grid: {
      vertLines: { color: '#1f2937', style: 1 },
      horzLines: { color: '#1f2937', style: 1 },
    },
    crosshair: {
      mode: 0,
      vertLine: { color: '#3b82f6', width: 1, style: 2, labelBackgroundColor: '#3b82f6' },
      horzLine: { color: '#3b82f6', width: 1, style: 2, labelBackgroundColor: '#3b82f6' },
    },
    rightPriceScale: {
      borderColor: '#1f2937',
      scaleMargins: { top: 0.1, bottom: 0.1 },
    },
    timeScale: {
      borderColor: '#1f2937',
      timeVisible: false,
      fixRightEdge: true,
      fixLeftEdge: true,
    },
    width: container.clientWidth,
    height: 400,
    handleScroll: false,
    handleScale: false,
  });

  // Bar (OHLC) series
  var barSeries = chart.addBarSeries({
    upColor: '#22c55e',
    downColor: '#ef4444',
    borderUpColor: '#22c55e',
    borderDownColor: '#ef4444',
    wickUpColor: '#22c55e',
    wickDownColor: '#ef4444',
    priceFormat: { type: 'price', precision: 2, minMove: 0.01 },
  });

  function filterData(months) {
    if (months === 'all') {
      return parsedData.map(function(d) {
        return { time: d.time, open: d.open, high: d.high, low: d.low, close: d.close };
      });
    }
    var cutoff = new Date();
    cutoff.setMonth(cutoff.getMonth() - months);
    return parsedData
      .filter(function(d) { return d.date >= cutoff; })
      .map(function(d) {
        return { time: d.time, open: d.open, high: d.high, low: d.low, close: d.close };
      });
  }

  // Default to 1Y
  var currentData = filterData(12);
  barSeries.setData(currentData);
  chart.timeScale().fitContent();

  var buttons = document.querySelectorAll('.tf-btn');
  buttons.forEach(function(btn) {
    btn.addEventListener('click', function() {
      buttons.forEach(function(b) { b.classList.remove('active'); });
      btn.classList.add('active');
      var months;
      switch (btn.dataset.tf) {
        case '1w': months = 0.25; break;   // ~1 week
        case '1m': months = 1; break;
        case '3m': months = 3; break;
        case '6m': months = 6; break;
        case '1y': months = 12; break;
        case '5y': months = 60; break;
        case 'all': months = 'all'; break;
        default: months = 12;
      }
      currentData = filterData(months);
      barSeries.setData(currentData);
      chart.timeScale().fitContent();
    });
  });

  function resizeChart() {
    var w = container.clientWidth;
    chart.applyOptions({ width: w, height: 400 });
    chart.timeScale().fitContent();
  }

  window.addEventListener('resize', resizeChart);
  setTimeout(resizeChart, 100);
}

// Auto-init
document.addEventListener('DOMContentLoaded', function() {
  var container = document.getElementById('tickerChart');
  if (container) {
    var tickerEl = document.querySelector('.ticker-badge');
    if (tickerEl) {
      var ticker = tickerEl.textContent.replace('$', '');
      initTickerChart(ticker);
    }
  }
});
