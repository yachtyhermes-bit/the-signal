// The Signal — Watchlist Manager
// Per-user saved watchlists with real-time prices via /api/prices
(function() {
  'use strict';

  var API_BASE = '/api/hive';

  function getToken() {
    try { return localStorage.getItem('hive_token'); } catch(e) { return null; }
  }

  function getUser() {
    try { return JSON.parse(localStorage.getItem('hive_user') || 'null'); } catch(e) { return null; }
  }

  // === API Calls ===

  function watchlistUrl() {
    var token = getToken();
    return API_BASE + '?action=watchlist&op=list&token=' + encodeURIComponent(token || '');
  }

  function addToWatchlist(ticker) {
    var token = getToken();
    return fetch(API_BASE + '?action=watchlist&op=add', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ ticker: ticker, token: token })
    }).then(function(r) { return r.json(); });
  }

  function removeFromWatchlist(ticker) {
    var token = getToken();
    return fetch(API_BASE + '?action=watchlist&op=remove', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ ticker: ticker, token: token })
    }).then(function(r) { return r.json(); });
  }

  function getWatchlist() {
    var token = getToken();
    return fetch(API_BASE + '?action=watchlist&op=list&token=' + encodeURIComponent(token || ''))
      .then(function(r) { return r.json(); });
  }

  // === Heart Toggle UI ===
  // Call this to put watchlist hearts on stock pages

  function createHeartIcon(ticker, isWatched, container) {
    var heart = document.createElement('span');
    heart.className = 'watchlist-heart' + (isWatched ? ' watched' : '');
    heart.setAttribute('data-ticker', ticker);
    heart.innerHTML = isWatched ? '❤️' : '🤍';
    heart.title = isWatched ? 'Remove from watchlist' : 'Add to watchlist';
    heart.style.cssText = 'cursor:pointer;font-size:1.3rem;display:inline-flex;align-items:center;justify-content:center;width:36px;height:36px;border-radius:50%;transition:all .2s;background:' + (isWatched ? 'rgba(239,68,68,.15)' : 'rgba(255,255,255,.05)') + ';';

    heart.addEventListener('click', function(e) {
      e.stopPropagation();
      e.preventDefault();
      var user = getUser();
      if (!user) {
        if (typeof showHiveJoinModal === 'function') {
          showHiveJoinModal('login');
        } else {
          window.location.href = '/hive';
        }
        return;
      }

      var currentlyWatched = heart.classList.contains('watched');
      if (currentlyWatched) {
        removeFromWatchlist(ticker).then(function(data) {
          if (data.status === 'ok') {
            heart.classList.remove('watched');
            heart.innerHTML = '🤍';
            heart.title = 'Add to watchlist';
            heart.style.background = 'rgba(255,255,255,.05)';
            // Dispatch event for page sync
            window.dispatchEvent(new CustomEvent('watchlist-changed', { detail: { ticker: ticker, action: 'removed' } }));
          }
        }).catch(function() {
          // Silent fail
        });
      } else {
        addToWatchlist(ticker).then(function(data) {
          if (data.status === 'ok') {
            heart.classList.add('watched');
            heart.innerHTML = '❤️';
            heart.title = 'Remove from watchlist';
            heart.style.background = 'rgba(239,68,68,.15)';
            window.dispatchEvent(new CustomEvent('watchlist-changed', { detail: { ticker: ticker, action: 'added' } }));
          }
        }).catch(function() {
          // Silent fail
        });
      }
    });

    if (container) container.appendChild(heart);
    return heart;
  }

  // === Initialize hearts on stock detail pages ===
  // Looks for elements with [data-watchlist-ticker] and stock-page ticker badges

  function initWatchlistHearts() {
    var user = getUser();
    if (!user) return;

    getWatchlist().then(function(data) {
      var watchlist = data.watchlist || [];
      var watchTickers = watchlist.map(function(item) { return item.ticker; });

      // Find all watchlist heart containers on the page
      var containers = document.querySelectorAll('[data-watchlist-ticker]');
      containers.forEach(function(container) {
        var ticker = container.getAttribute('data-watchlist-ticker');
        if (ticker) {
          var isWatched = watchTickers.indexOf(ticker) !== -1;
          createHeartIcon(ticker, isWatched, container);
        }
      });

      // Try to find stock ticker from common page elements
      var tickerFromBadge = document.querySelector('.stock-ticker-badge');
      if (tickerFromBadge && !tickerFromBadge.querySelector('.watchlist-heart')) {
        var text = tickerFromBadge.textContent.trim();
        var match = text.match(/\$?([A-Z]{1,5})/);
        if (match) {
          var tickerText = match[1];
          if (tickerText && tickerText.length <= 5) {
            // Insert heart after the ticker badge content
            var heartContainer = document.createElement('span');
            heartContainer.style.cssText = 'display:inline-flex;align-items:center;margin-left:8px;vertical-align:middle;';
            tickerFromBadge.parentNode.insertBefore(heartContainer, tickerFromBadge.nextSibling);
            var isWatched = watchTickers.indexOf(tickerText) !== -1;
            createHeartIcon(tickerText, isWatched, heartContainer);
          }
        }
      }

      // Also try page title
      var title = document.title;
      var titleMatch = title.match(/^([A-Z]{1,5})\s*(—|-)/);
      if (titleMatch) {
        var titleTicker = titleMatch[1];
        // Check if it's a stock page and heart not already added
        if (document.querySelector('.stock-page, .stock-hero') && !document.querySelector('[data-watchlist-ticker="' + titleTicker + '"]') && !document.querySelector('.watchlist-heart')) {
          var badge = document.querySelector('.stock-ticker-badge');
          if (!badge || !badge.querySelector('.watchlist-heart')) {
            // Find a good spot to insert
            var heroLeft = document.querySelector('.stock-hero-left');
            if (heroLeft) {
              var isWatched = watchTickers.indexOf(titleTicker) !== -1;
              createHeartIcon(titleTicker, isWatched, heroLeft);
            }
          }
        }
      }

      // Legacy selector support
      var tickerDisplay = document.querySelector('.stock-title h1, .stock-header .ticker, .stock-ticker-display');
      if (tickerDisplay && !tickerDisplay.querySelector('.watchlist-heart') && !document.querySelector('.watchlist-heart')) {
        var tickerText = tickerDisplay.textContent.trim();
        if (tickerText && tickerText.length <= 5) {
          var isWatched = watchTickers.indexOf(tickerText) !== -1;
          createHeartIcon(tickerText, isWatched, tickerDisplay);
          tickerDisplay.style.display = 'inline-flex';
          tickerDisplay.style.alignItems = 'center';
          tickerDisplay.style.gap = '8px';
        }
      }
    }).catch(function() {
      // Not authenticated or API error — skip hearts
    });
  }

  // === Watchlist Page Renderer ===

  function renderWatchlistPage(container) {
    if (!container) return;

    var user = getUser();
    if (!user) {
      container.innerHTML = '<div style="text-align:center;padding:4rem 2rem;">' +
        '<div style="font-size:3rem;margin-bottom:1rem;">📋</div>' +
        '<h2 style="font-family:\'Oxanium\',sans-serif;font-size:1.3rem;color:#fff;margin:0 0 .5rem;">Sign in to use Watchlists</h2>' +
        '<p style="color:#94a3b8;margin:0 0 2rem;">Track your favorite stocks and monitor their prices in real time.</p>' +
        '<button class="hive-cta-btn" onclick="showHiveJoinModal()">Sign In</button>' +
        '</div>';
      return;
    }

    container.innerHTML = '<div style="text-align:center;padding:3rem;"><div class="hive-spinner" style="margin:0 auto 1rem;"></div><span style="color:#94a3b8;">Loading your watchlist...</span></div>';

    getWatchlist().then(function(data) {
      var items = data.watchlist || [];
      renderWatchlistItems(items, container);
    }).catch(function() {
      container.innerHTML = '<div style="text-align:center;padding:3rem;color:#ef4444;">Failed to load watchlist. Please try again.</div>';
    });
  }

  function renderWatchlistItems(items, container) {
    if (items.length === 0) {
      container.innerHTML = '<div style="text-align:center;padding:4rem 2rem;">' +
        '<div style="font-size:3rem;margin-bottom:1rem;">📋</div>' +
        '<h2 style="font-family:\'Oxanium\',sans-serif;font-size:1.3rem;color:#fff;margin:0 0 .5rem;">Your Watchlist is Empty</h2>' +
        '<p style="color:#94a3b8;margin:0 0 .3rem;">Start adding stocks you want to track.</p>' +
        '<p style="color:#5e7092;font-size:.85rem;margin:0 0 2rem;">Click the 🤍 icon on any stock page to add it here.</p>' +
        '<a href="/stocks/" class="premium-cta-btn" style="display:inline-block;padding:12px 28px;background:linear-gradient(135deg,#6366f1,#818cf8);border:none;border-radius:10px;color:#fff;font-family:\'Oxanium\',sans-serif;font-size:.9rem;font-weight:700;cursor:pointer;text-decoration:none;">Browse Stocks</a>' +
        '</div>';
      return;
    }

    var html = '<div style="display:flex;flex-direction:column;gap:.6rem;">';

    items.forEach(function(item) {
      var price = item.price;
      var priceStr = price !== null && price !== undefined ? '$' + price.toFixed(2) : '---';
      var sectorColor = getSectorColor(item.sector);

      html += '<div class="watchlist-item" data-ticker="' + item.ticker + '" style="display:flex;align-items:center;gap:1rem;padding:.8rem 1rem;background:linear-gradient(145deg,#12121a,#1a1a2e);border:1px solid #2a2a3e;border-radius:12px;cursor:pointer;transition:border-color .2s,transform .2s;" onclick="window.location.href=\'/stocks/' + item.ticker + '/\'" onmouseover="this.style.borderColor=\'#6366f1\';this.style.transform=\'translateY(-2px)\'" onmouseout="this.style.borderColor=\'#2a2a3e\';this.style.transform=\'none\'">' +
        '<div style="width:4px;height:36px;border-radius:2px;background:' + sectorColor + ';flex-shrink:0;"></div>' +
        '<div style="flex-shrink:0;">' +
          '<span style="font-family:\'JetBrains Mono\',monospace;font-weight:700;font-size:1rem;color:#fff;">' + item.ticker + '</span>' +
          '<div style="font-size:.75rem;color:#5e7092;margin-top:2px;">' + item.sector + '</div>' +
        '</div>' +
        '<div style="flex:1;min-width:0;">' +
          '<div style="font-size:.85rem;color:#94a3b8;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;">' + item.name + '</div>' +
        '</div>' +
        '<div style="font-family:\'JetBrains Mono\',monospace;font-size:1rem;font-weight:600;color:#e0e0e0;">' + priceStr + '</div>' +
        '<button class="watchlist-remove-btn" data-ticker="' + item.ticker + '" style="background:none;border:none;cursor:pointer;font-size:1.1rem;padding:4px 8px;border-radius:6px;color:#5e7092;transition:color .2s,background .2s;" onclick="event.stopPropagation();removeWatchlistItem(\'' + item.ticker + '\', this)" onmouseover="this.style.color=\'#ef4444\';this.style.background=\'rgba(239,68,68,.1)\'" onmouseout="this.style.color=\'#5e7092\';this.style.background=\'none\'">✕</button>' +
      '</div>';
    });

    html += '</div>';
    container.innerHTML = html;
  }

  function getSectorColor(sector) {
    var colors = {
      'AI': '#3b82f6',
      'Cybersecurity': '#22c55e',
      'Defense': '#fbbf24',
      'Space': '#a78bfa',
      'Mega-Cap': '#f87171',
      'Quantum': '#06b6d4'
    };
    return colors[sector] || '#6366f1';
  }

  window.removeWatchlistItem = function(ticker, btn) {
    var item = btn.closest('.watchlist-item');
    if (item) item.style.opacity = '0.4';

    removeFromWatchlist(ticker).then(function(data) {
      if (data.status === 'ok') {
        // Re-render the watchlist
        var container = document.getElementById('watchlistContent');
        if (container) renderWatchlistPage(container);
      }
    }).catch(function() {
      if (item) item.style.opacity = '1';
    });
  };

  // === Auto-initialize on stock pages ===
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initWatchlistHearts);
  } else {
    initWatchlistHearts();
  }

  // Re-initialize when auth changes
  window.addEventListener('storage', function(e) {
    if (e.key === 'hive_user' || e.key === 'hive_token') {
      setTimeout(initWatchlistHearts, 500);
    }
  });

  // Expose public API
  window.watchlistAPI = {
    get: getWatchlist,
    add: addToWatchlist,
    remove: removeFromWatchlist,
    render: renderWatchlistPage,
    initHearts: initWatchlistHearts,
    createHeart: createHeartIcon
  };

  // Listen for watchlist-changed events
  window.addEventListener('watchlist-changed', function(e) {
    // Re-render watchlist page if visible
    var container = document.getElementById('watchlistContent');
    if (container) renderWatchlistPage(container);
  });

})();
