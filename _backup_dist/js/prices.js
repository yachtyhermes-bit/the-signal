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

  // Update stock cards + trending rows (data-price / data-change attributes)
  function updateCardPrices(prices) {
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
        var cls = el.className.replace(/positive|negative|up|down/g,'').trim();
        el.className = cls + ' ' + (p.changePercent >= 0 ? 'up' : 'down');
      }
    });
  }

  // Update "The Numbers That Matter" stats tables on article pages
  // (cells marked data-live-ticker + data-live-field, e.g. data-live-field="price")
  function updateStatsTables(prices) {
    document.querySelectorAll('.stats-table [data-live-ticker]').forEach(function(cell) {
      var sym = cell.getAttribute('data-live-ticker');
      var field = cell.getAttribute('data-live-field') || 'price';
      var p = prices[sym];
      if (!p) return;

      if (field === 'price' && p.price != null) {
        cell.textContent = '$' + formatNum(p.price);
        if (p.changePercent != null) {
          var chip = cell.querySelector('.stat-live-chip');
          if (!chip) {
            chip = document.createElement('span');
            cell.appendChild(chip);
          }
          chip.className = 'stat-live-chip ' + (p.changePercent >= 0 ? 'up' : 'down');
          chip.textContent = (p.changePercent >= 0 ? '+' : '') + p.changePercent.toFixed(2) + '%';
        }
      } else if (field === 'changePercent' && p.changePercent != null) {
        cell.textContent = (p.changePercent >= 0 ? '+' : '') + p.changePercent.toFixed(2) + '%';
        cell.classList.remove('positive', 'negative');
        cell.classList.add(p.changePercent >= 0 ? 'positive' : 'negative');
      }
    });
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
    updateCardPrices(data);
    updateStatsTables(data);
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
