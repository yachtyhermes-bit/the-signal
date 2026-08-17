(function() {
  'use strict';

  // ── DOM refs ──
  const overlay = document.getElementById('searchOverlay');
  const toggle = document.getElementById('searchToggle');
  const input = document.getElementById('searchInput');
  const resultsEl = document.getElementById('searchResults');
  const emptyEl = document.getElementById('searchEmpty');
  const closeBtn = document.getElementById('searchClose');
  const backdrop = document.getElementById('searchBackdrop');

  if (!overlay || !toggle) return;

  // ── State ──
  let articles = [];
  let stockPages = [];
  let premiumStatus = null; // null=unknown, true, false
  let userChecked = false;

  // ── Premium helpers ──
  function checkPremiumStatus(callback) {
    if (premiumStatus !== null) {
      callback(premiumStatus);
      return;
    }
    var token = null;
    try { token = localStorage.getItem('hive_token'); } catch(e) {}
    if (!token) {
      premiumStatus = false;
      userChecked = true;
      callback(false);
      return;
    }
    fetch('/api/hive?action=me&token=' + encodeURIComponent(token))
      .then(function(r) { return r.json(); })
      .then(function(data) {
        premiumStatus = !!(data.authenticated && data.isPremium);
        userChecked = true;
        callback(premiumStatus);
      })
      .catch(function() {
        premiumStatus = false;
        userChecked = true;
        callback(false);
      });
  }

  // ── Load stock pages (public — stock pages are free static pages) ──
  function loadStockPages(callback) {
    if (stockPages.length > 0) {
      callback(stockPages);
      return;
    }
    fetch('/stocks/index.json')
      .then(function(r) {
        if (!r.ok) throw new Error('No stock index');
        return r.json();
      })
      .then(function(data) {
        stockPages = data.stocks || data || [];
        callback(stockPages);
      })
      .catch(function() {
        // Stock index doesn't exist yet — try scraping /stocks/ page
        stockPages = [];
        callback([]);
      });
  }

  // ── Load articles ──
  function ensureArticles(callback) {
    if (articles.length > 0) {
      callback(articles);
      return;
    }
    fetch('/articles/index.json')
      .then(function(r) { return r.json(); })
      .then(function(data) {
        articles = data || [];
        callback(articles);
      })
      .catch(function() { callback([]); });
  }

  // ── Date helpers ──
  function daysAgo(days) {
    var d = new Date();
    d.setDate(d.getDate() - days);
    return d;
  }

  function parseArticleDate(a) {
    try { return new Date(a.date); } catch(e) { return null; }
  }

  // ── Search core ──
  function performSearch(query) {
    var q = query.toLowerCase().trim();
    if (!q) {
      resultsEl.innerHTML = '';
      emptyEl.textContent = 'Start typing to search articles…';
      return;
    }

    checkPremiumStatus(function(isPremium) {
      ensureArticles(function(allArticles) {
        // ── Filter articles ──
        var cutoff = isPremium ? null : daysAgo(30);
        var filtered = allArticles.filter(function(a) {
          // Free users: only articles from last 30 days
          if (cutoff) {
            var d = parseArticleDate(a);
            if (d && d < cutoff) return false;
          }

          var title = (a.title || '').toLowerCase();
          var summary = (a.summary || '').toLowerCase();
          var ticker = (a.ticker || '').toLowerCase();
          var sector = (a.sector || '').toLowerCase();
          var tags = (a.tags || []).join(' ').toLowerCase();

          return title.indexOf(q) !== -1 ||
                 summary.indexOf(q) !== -1 ||
                 ticker.indexOf(q) !== -1 ||
                 sector.indexOf(q) !== -1 ||
                 tags.indexOf(q) !== -1;
        });

        // ── Search stock pages (public — stock pages are free static pages) ──
        loadStockPages(function(stocks) {
          var stockResults = stocks.filter(function(s) {
            var ticker = s.ticker || s.sym || '';
            var name = ((s.name || ticker) + ' ' + ticker + ' ' + (s.sector || '')).toLowerCase();
            return name.indexOf(q) !== -1;
          });
          // Exact ticker match pinned first (case-insensitive); rest keep index order
          stockResults.sort(function(a, b) {
            var aExact = ((a.ticker || a.sym || '').toLowerCase() === q) ? 0 : 1;
            var bExact = ((b.ticker || b.sym || '').toLowerCase() === q) ? 0 : 1;
            return aExact - bExact;
          });
          renderResults(q, filtered, stockResults, isPremium);
        });
      });
    });
  }

  function renderResults(query, articleResults, stockResults, isPremium) {
    var totalArticles = articleResults.length;
    var totalStocks = stockResults.length;
    var MAX_FREE_RESULTS = 5;
    var showAll = isPremium || totalArticles <= MAX_FREE_RESULTS;
    var shownArticles = showAll ? articleResults : articleResults.slice(0, MAX_FREE_RESULTS);
    var hiddenCount = isPremium ? 0 : Math.max(0, totalArticles - MAX_FREE_RESULTS);

    if (totalArticles === 0 && totalStocks === 0) {
      resultsEl.innerHTML = '';
      emptyEl.textContent = 'No results found for "' + query + '"';
      emptyEl.style.display = 'block';
      return;
    }

    emptyEl.style.display = 'none';

    var html = '';

    // ── Stock page results (public) ──
    if (stockResults.length > 0) {
      html += '<div class="search-section-label" style="padding:0.5rem 1rem;font-size:0.6rem;letter-spacing:2px;text-transform:uppercase;color:var(--color-stealth-80);font-family:Roboto Mono,monospace;">Stock Pages</div>';
      stockResults.forEach(function(s) {
        var ticker = s.ticker || s.sym || '';
        var name = s.name || ticker;
        var sector = s.sector || '';
        var priceText = (s.price != null && !isNaN(s.price)) ? '$' + Number(s.price).toFixed(2) : '—';
        html += '<a href="/stocks/' + ticker.toUpperCase() + '" class="search-result-item" onclick="handleSearchClose()">' +
          '<div class="search-result-info">' +
            '<div class="search-result-title">' + escapeHtml(name) + '</div>' +
            '<div class="search-result-meta">' +
              '<span class="search-result-ticker">$' + escapeHtml(ticker) + '</span>' +
              (sector ? '<span class="search-result-sector">' + escapeHtml(sector) + '</span>' : '') +
              '<span data-price="' + escapeHtml(ticker.toUpperCase()) + '" style="margin-left:auto;color:var(--text-secondary);font-weight:600;">' + priceText + '</span>' +
            '</div>' +
          '</div>' +
        '</a>';
      });
    }

    // ── Article results ──
    if (shownArticles.length > 0) {
      html += '<div class="search-section-label" style="padding:0.5rem 1rem;font-size:0.6rem;letter-spacing:2px;text-transform:uppercase;color:var(--color-stealth-80);font-family:Roboto Mono,monospace;">Articles' + (isPremium ? ' <span style="font-size:0.5rem;border:1px solid rgba(6,128,255,0.3);border-radius:3px;padding:1px 6px;margin-left:6px;color:#0680ff;">⚡ Real-time</span>' : '') + '</div>';
      shownArticles.forEach(function(a) {
        var dateStr = '';
        try {
          dateStr = new Date(a.date).toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' });
        } catch(e) {}

        var sectorColors = {
          'ai': '#60a5fa',
          'cyber': '#4ade80',
          'defense': '#fbbf24',
          'space': '#a78bfa',
          'mega-cap': '#f87171'
        };
        var sectorColor = sectorColors[a.sector] || '#8888aa';

        html += '<a href="/article/' + a.slug + '" class="search-result-item" onclick="handleSearchClose()">' +
          '<div class="search-result-info">' +
            '<div class="search-result-title">' + escapeHtml(a.title) + (isPremium ? ' <span style="font-size:0.65rem;color:#0680ff;">⚡</span>' : '') + '</div>' +
            '<div class="search-result-meta">' +
              '<span class="search-result-ticker">$' + escapeHtml(a.ticker) + '</span>' +
              '<span class="search-result-sector" style="color:' + sectorColor + '">' + escapeHtml(a.sector) + '</span>' +
              (dateStr ? '<span class="search-result-date">' + dateStr + '</span>' : '') +
            '</div>' +
          '</div>' +
        '</a>';
      });
    }

    // ── Upgrade CTA for free users ──
    if (hiddenCount > 0) {
      html += '<div class="search-upgrade-cta" style="text-align:center;padding:1.25rem 1rem;border-top:1px solid rgba(69,69,70,0.3);margin-top:0.5rem;">' +
        '<p style="font-size:0.75rem;color:var(--color-grayscale-500);margin-bottom:0.75rem;line-height:1.6;">' +
          hiddenCount + ' more article' + (hiddenCount > 1 ? 's' : '') + ' hidden for free accounts. ' +
          '<a href="/pricing" style="color:#0680ff;font-weight:600;text-decoration:underline;text-underline-offset:2px;">Upgrade to Signal Premium</a> for unlimited search.' +
        '</p>' +
      '</div>';
    }

    resultsEl.innerHTML = html;
  }

  // ── Utilities ──
  function escapeHtml(str) {
    if (!str) return '';
    var div = document.createElement('div');
    div.appendChild(document.createTextNode(str));
    return div.innerHTML;
  }

  // ── Open / Close ──
  function openSearch() {
    overlay.classList.add('active');
    document.body.style.overflow = 'hidden';
    setTimeout(function() { if (input) input.focus(); }, 100);
  }

  function closeSearch() {
    overlay.classList.remove('active');
    document.body.style.overflow = '';
    if (input) input.value = '';
    if (resultsEl) resultsEl.innerHTML = '';
    if (emptyEl) emptyEl.textContent = 'Start typing to search articles…';
  }

  // Expose close helper for inline onclick
  window.handleSearchClose = closeSearch;

  // ── Event listeners ──
  toggle.addEventListener('click', function(e) {
    e.stopPropagation();
    ensureArticles(function() {
      openSearch();
      if (input.value.trim()) performSearch(input.value);
    });
  });

  if (closeBtn) closeBtn.addEventListener('click', closeSearch);
  if (backdrop) backdrop.addEventListener('click', closeSearch);

  document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape' && overlay.classList.contains('active')) {
      closeSearch();
    }
    // Ctrl+K or Cmd+K to open
    if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
      e.preventDefault();
      ensureArticles(function() {
        openSearch();
      });
    }
  });

  if (input) {
    input.addEventListener('input', function() {
      performSearch(this.value);
    });
    input.addEventListener('keydown', function(e) {
      if (e.key === 'Escape') closeSearch();
    });
  }

  // Prevent overlay from closing when clicking inside modal
  var modal = overlay.querySelector('.search-modal');
  if (modal) {
    modal.addEventListener('click', function(e) {
      e.stopPropagation();
    });
  }
})();
