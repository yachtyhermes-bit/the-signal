// Live price updater for The Signal
// Fetches from Yahoo Finance v8 API every 60 seconds
(function() {
  'use strict';

  const TICKERS = [
    'NVDA', 'PLTR', 'AVGO', 'AMD', 'GOOGL', 'META', 'MSFT', 'AMZN', 'TSLA', 'CRWV'
  ];

  const INTERVAL = 1800000; // 30 minutes

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

  function updatePriceChips(prices) {
    const chips = document.querySelectorAll('.price-chip');
    for (const chip of chips) {
      // Price chips are inside article cards with format: $PRICE (+/-X.XX%)
      // The parent card has a .ticker-badge with the ticker symbol
      const card = chip.closest('.article-card');
      if (!card) continue;
      const badge = card.querySelector('.ticker-badge');
      if (!badge) continue;
      const sym = badge.textContent.trim();
      const p = prices[sym];
      if (!p || p.price == null) continue;

      const price = p.price;
      const changePercent = p.changePercent;

      const dir = changePercent >= 0 ? 'up' : 'down';
      chip.className = 'price-chip ' + dir;
      const chgStr = (changePercent >= 0 ? '+' : '') + changePercent.toFixed(2) + '%';
      chip.innerHTML = '$' + formatNum(price) + ' <span>' + chgStr + '</span>';
    }
  }

  async function fetchPrices() {
    try {
      // Batch fetch in groups of 5 to avoid rate limits
      const results = {};
      const batchSize = 5;
      for (let i = 0; i < TICKERS.length; i += batchSize) {
        const batch = TICKERS.slice(i, i + batchSize);
        const promises = batch.map(sym =>
          fetch('https://query1.finance.yahoo.com/v8/finance/chart/' + sym + '?interval=1d&range=2d', {
            headers: { 'User-Agent': 'Mozilla/5.0' }
          })
          .then(r => r.json())
          .then(d => {
            const result = d.chart?.result?.[0];
            if (!result) return null;
            const meta = result.meta;
            // Use actual quote close data for accuracy, not meta.chartPreviousClose
            const quotes = result.indicators?.quote?.[0];
            const closes = quotes?.close?.filter(c => c != null) || [];
            const price = closes.length ? closes[closes.length - 1] : meta.regularMarketPrice;
            const prevClose = closes.length >= 2 ? closes[closes.length - 2] : meta.chartPreviousClose;
            const changePercent = (price && prevClose) ? ((price - prevClose) / prevClose) * 100 : null;
            results[sym] = { price, prevClose, changePercent };
          })
          .catch(() => {})
        );
        await Promise.allSettled(promises);
        if (i + batchSize < TICKERS.length) {
          await new Promise(r => setTimeout(r, 300));
        }
      }
      return results;
    } catch (e) {
      console.warn('Price fetch failed:', e);
      return null;
    }
  }

  async function refresh() {
    const prices = await fetchPrices();
    if (!prices) return;
    updateTickerTape(prices);
    updatePriceChips(prices);
  }

  // Initial fetch after page loads
  if (document.readyState === 'complete') {
    refresh();
  } else {
    window.addEventListener('load', refresh);
  }

  // Then every 60 seconds
  setInterval(refresh, INTERVAL);
})();
