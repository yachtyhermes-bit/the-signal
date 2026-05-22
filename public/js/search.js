(function() {
  'use strict';

  const overlay = document.getElementById('searchOverlay');
  const toggle = document.getElementById('searchToggle');
  const input = document.getElementById('searchInput');
  const resultsEl = document.getElementById('searchResults');
  const emptyEl = document.getElementById('searchEmpty');
  const closeBtn = document.getElementById('searchClose');
  const backdrop = document.getElementById('searchBackdrop');

  if (!overlay || !toggle) return;

  // Load articles data from the embedded JSON
  let articles = [];
  try {
    const script = document.getElementById('articles-data');
    if (script) {
      articles = JSON.parse(script.textContent) || [];
    }
  } catch (e) {
    console.warn('Search: Could not parse articles data');
  }

  // Also try fetching from /articles/index.json as fallback for article pages
  function ensureArticles(callback) {
    if (articles.length > 0) {
      callback(articles);
      return;
    }
    fetch('/articles/index.json')
      .then(r => r.json())
      .then(data => {
        articles = data || [];
        callback(articles);
      })
      .catch(() => callback([]));
  }

  function openSearch() {
    overlay.classList.add('active');
    document.body.style.overflow = 'hidden';
    setTimeout(() => input && input.focus(), 100);
  }

  function closeSearch() {
    overlay.classList.remove('active');
    document.body.style.overflow = '';
    if (input) input.value = '';
    if (resultsEl) resultsEl.innerHTML = '';
    if (emptyEl) emptyEl.textContent = 'Start typing to search articles…';
  }

  function performSearch(query) {
    const q = query.toLowerCase().trim();
    if (!q) {
      resultsEl.innerHTML = '';
      emptyEl.textContent = 'Start typing to search articles…';
      return;
    }

    const results = articles.filter(function(a) {
      const title = (a.title || '').toLowerCase();
      const summary = (a.summary || '').toLowerCase();
      const ticker = (a.ticker || '').toLowerCase();
      const sector = (a.sector || '').toLowerCase();
      const tags = (a.tags || []).join(' ').toLowerCase();

      return title.indexOf(q) !== -1 ||
             summary.indexOf(q) !== -1 ||
             ticker.indexOf(q) !== -1 ||
             sector.indexOf(q) !== -1 ||
             tags.indexOf(q) !== -1;
    });

    if (results.length === 0) {
      resultsEl.innerHTML = '';
      emptyEl.textContent = 'No articles found for "' + query + '"';
      emptyEl.style.display = 'block';
      return;
    }

    emptyEl.style.display = 'none';
    resultsEl.innerHTML = results.slice(0, 12).map(function(a) {
      var dateStr = '';
      try {
        dateStr = new Date(a.date).toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' });
      } catch (e) {}

      var sectorColors = {
        'ai': '#60a5fa',
        'cyber': '#4ade80',
        'defense': '#fbbf24',
        'space': '#a78bfa',
        'mega-cap': '#f87171'
      };
      var sectorColor = sectorColors[a.sector] || '#8888aa';

      return '<a href="/article/' + a.slug + '" class="search-result-item" onclick="handleSearchClose()">' +
        '<div class="search-result-info">' +
          '<div class="search-result-title">' + escapeHtml(a.title) + '</div>' +
          '<div class="search-result-meta">' +
            '<span class="search-result-ticker">$' + escapeHtml(a.ticker) + '</span>' +
            '<span class="search-result-sector" style="color:' + sectorColor + '">' + escapeHtml(a.sector) + '</span>' +
            (dateStr ? '<span class="search-result-date">' + dateStr + '</span>' : '') +
          '</div>' +
        '</div>' +
      '</a>';
    }).join('');
  }

  function escapeHtml(str) {
    if (!str) return '';
    var div = document.createElement('div');
    div.appendChild(document.createTextNode(str));
    return div.innerHTML;
  }

  // Expose close helper for inline onclick
  window.handleSearchClose = closeSearch;

  // Event listeners
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
