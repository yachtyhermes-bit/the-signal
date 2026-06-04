// Live price updater for The Signal
// Fetches from our proxy API (no CORS issues)
(function() {
  'use strict';

  const INTERVAL = 300000; // 5 minutes

  function formatNum(n) {
    if (n == null || isNaN(n)) return '---';
    return n.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
  }

  function updateTickerTape(prices) {
    const items = document.querySelectorAll('.ticker-item');
    if (!items.length) return;

    for (const el of items) {
      const symEl = el.querySelector('.ticker-sym');
      const prcEl = el.querySelector('.ticker-prc');
      const chgEl = el.querySelector('.ticker-chg');
      if (!symEl || !prcEl || !chgEl) continue;

      const sym = symEl.textContent.trim();
      const p = prices[sym];
      if (!p || p.price == null) continue;

      const price = p.price;
      const changePercent = p.changePercent;

      prcEl.textContent = '$' + formatNum(price);
      if (changePercent != null) {
        const chgStr = (changePercent >= 0 ? '+' : '') + changePercent.toFixed(2) + '%';
        chgEl.textContent = chgStr;
        chgEl.className = 'ticker-chg ' + (changePercent >= 0 ? 'up' : 'down');
      }
    }
  }

  async function fetchPrices() {
    try {
      const res = await fetch('/api/prices/');
      if (!res.ok) return null;
      const data = await res.json();
      return data.prices || null;
    } catch (e) {
      console.warn('Price fetch failed:', e);
      return null;
    }
  }

  async function refresh() {
    const data = await fetchPrices();
    if (!data) return;
    updateTickerTape(data);
  }

  // Initial fetch after page loads
  if (document.readyState === 'complete') {
    refresh();
  } else {
    window.addEventListener('load', refresh);
  }

  // Then every 5 minutes
  setInterval(refresh, INTERVAL);
})();
