// The Hive — Client-side JavaScript for simulated trading & leaderboard
(function() {
  'use strict';

  const API_BASE = '/api/hive';

  // === Coverage Universe with company info ===
  var STOCKS = [
    { ticker: 'NVDA', name: 'NVIDIA Corporation', sector: 'AI' },
    { ticker: 'AMD', name: 'Advanced Micro Devices', sector: 'AI' },
    { ticker: 'AVGO', name: 'Broadcom Inc.', sector: 'AI' },
    { ticker: 'MRVL', name: 'Marvell Technology', sector: 'AI' },
    { ticker: 'TSM', name: 'Taiwan Semiconductor', sector: 'AI' },
    { ticker: 'ASML', name: 'ASML Holding', sector: 'AI' },
    { ticker: 'MU', name: 'Micron Technology', sector: 'AI' },
    { ticker: 'CBRS', name: 'Cerebras Systems', sector: 'AI' },
    { ticker: 'CRWV', name: 'CoreWeave Inc.', sector: 'AI' },
    { ticker: 'NBIS', name: 'Nebius Group', sector: 'AI' },
    { ticker: 'INTC', name: 'Intel Corporation', sector: 'AI' },
    { ticker: 'IREN', name: 'Iris Energy', sector: 'AI' },
    { ticker: 'LRCX', name: 'Lam Research Corp.', sector: 'AI' },
    { ticker: 'AMAT', name: 'Applied Materials Inc.', sector: 'AI' },
    { ticker: 'QCOM', name: 'Qualcomm Inc.', sector: 'AI' },
    { ticker: 'SMCI', name: 'Super Micro Computer Inc.', sector: 'AI' },
    { ticker: 'CRWD', name: 'CrowdStrike Holdings', sector: 'Cybersecurity' },
    { ticker: 'PANW', name: 'Palo Alto Networks', sector: 'Cybersecurity' },
    { ticker: 'FTNT', name: 'Fortinet Inc.', sector: 'Cybersecurity' },
    { ticker: 'ZS', name: 'Zscaler Inc.', sector: 'Cybersecurity' },
    { ticker: 'S', name: 'SentinelOne Inc.', sector: 'Cybersecurity' },
    { ticker: 'CHKP', name: 'Check Point Software', sector: 'Cybersecurity' },
    { ticker: 'CYBR', name: 'CyberArk Software', sector: 'Cybersecurity' },
    { ticker: 'TENB', name: 'Tenable Holdings', sector: 'Cybersecurity' },
    { ticker: 'RBRK', name: 'Rubrik Inc.', sector: 'Cybersecurity' },
    { ticker: 'LMT', name: 'Lockheed Martin', sector: 'Defense' },
    { ticker: 'RTX', name: 'RTX Corporation', sector: 'Defense' },
    { ticker: 'NOC', name: 'Northrop Grumman', sector: 'Defense' },
    { ticker: 'GD', name: 'General Dynamics', sector: 'Defense' },
    { ticker: 'LHX', name: 'L3Harris Technologies', sector: 'Defense' },
    { ticker: 'KTOS', name: 'Kratos Defense & Security', sector: 'Defense' },
    { ticker: 'AVAV', name: 'AeroVironment Inc.', sector: 'Defense' },
    { ticker: 'PL', name: 'Planet Labs', sector: 'Defense' },
    { ticker: 'AXON', name: 'Axon Enterprise', sector: 'Defense' },
    { ticker: 'GE', name: 'GE Aerospace', sector: 'Defense' },
    { ticker: 'PLTR', name: 'Palantir Technologies', sector: 'Defense' },
    { ticker: 'RKLB', name: 'Rocket Lab USA', sector: 'Space' },
    { ticker: 'RDW', name: 'Redwire Corporation', sector: 'Space' },
    { ticker: 'LUNR', name: 'Intuitive Machines', sector: 'Space' },
    { ticker: 'ASTS', name: 'AST SpaceMobile', sector: 'Space' },
    { ticker: 'AAPL', name: 'Apple Inc.', sector: 'Mega-Cap' },
    { ticker: 'MSFT', name: 'Microsoft Corporation', sector: 'Mega-Cap' },
    { ticker: 'GOOGL', name: 'Alphabet Inc.', sector: 'Mega-Cap' },
    { ticker: 'AMZN', name: 'Amazon.com Inc.', sector: 'Mega-Cap' },
    { ticker: 'META', name: 'Meta Platforms', sector: 'Mega-Cap' },
    { ticker: 'TSLA', name: 'Tesla Inc.', sector: 'Mega-Cap' },
    { ticker: 'NFLX', name: 'Netflix Inc.', sector: 'Mega-Cap' },
    { ticker: 'IONQ', name: 'IonQ Inc.', sector: 'Quantum' },
    { ticker: 'QBTS', name: 'D-Wave Quantum Inc.', sector: 'Quantum' },
    { ticker: 'QUBT', name: 'Quantum Computing Inc.', sector: 'Quantum' },
    { ticker: 'RGTI', name: 'Rigetti Computing Inc.', sector: 'Quantum' }
  ];

  // Keep old COVERAGE_UNIVERSE as array of ticker strings for backward compatibility
  var COVERAGE_UNIVERSE = STOCKS.map(function(s) { return s.ticker; });

  var SECTOR_COLORS = {
    'AI': '#3b82f6',
    'Cybersecurity': '#22c55e',
    'Defense': '#fbbf24',
    'Space': '#a78bfa',
    'Mega-Cap': '#f87171',
    'Quantum': '#06b6d4'
  };

  var SECTOR_ORDER = ['AI', 'Cybersecurity', 'Defense', 'Space', 'Mega-Cap', 'Quantum'];

  // Helper: stock lookup by ticker
  function getStockInfo(ticker) {
    for (var i = 0; i < STOCKS.length; i++) {
      if (STOCKS[i].ticker === ticker) return STOCKS[i];
    }
    return { ticker: ticker, name: ticker, sector: 'Other' };
  }

  // === Auth helpers ===
  function getToken() {
    try { return localStorage.getItem('hive_token'); } catch(e) { return null; }
  }

  function setToken(token) {
    try { localStorage.setItem('hive_token', token); } catch(e) {}
  }

  function clearToken() {
    try { localStorage.removeItem('hive_token'); } catch(e) {}
  }

  function getCurrentUser() {
    try {
      var data = localStorage.getItem('hive_user');
      if (data) return JSON.parse(data);
    } catch(e) {}
    return null;
  }

  function setCurrentUser(user) {
    try {
      localStorage.setItem('hive_user', JSON.stringify(user));
    } catch(e) {}
  }

  function clearCurrentUser() {
    try { localStorage.removeItem('hive_user'); } catch(e) {}
  }

  // Remove old thesignal_user so we don't have conflicts
  function migrateOldUser() {
    try {
      var old = localStorage.getItem('thesignal_user');
      if (old) {
        var parsed = JSON.parse(old);
        // If there's no hive_token, we'll treat as logged out
        localStorage.removeItem('thesignal_user');
      }
    } catch(e) {}
  }

  // === API calls with token ===
  function apiUrl(path) {
    var token = getToken();
    if (token) {
      if (path.indexOf('?') === -1) return path + '?token=' + encodeURIComponent(token);
      return path + '&token=' + encodeURIComponent(token);
    }
    return path;
  }

  function apiCall(url, options) {
    var token = getToken();
    if (token && options && options.body) {
      try {
        var body = JSON.parse(options.body);
        body.token = token;
        options.body = JSON.stringify(body);
      } catch(e) {}
    }
    return fetch(url, options);
  }

  // === Portfolio Page ===
  function loadPortfolio() {
    var user = getCurrentUser();
    var container = document.getElementById('hivePortfolioContent');
    if (!container) return;

    if (!user) {
      container.innerHTML = '<div class="hive-empty-state">' +
        '<div class="hive-empty-icon">🐝</div>' +
        '<h3>Sign in to manage your portfolio</h3>' +
        '<p>Join The Hive and get a $100,000 simulated portfolio to trade our coverage universe.</p>' +
        '<button class="hive-cta-btn" onclick="showHiveJoinModal()">Sign In</button>' +
        '</div>';
      return;
    }

    container.innerHTML = '<div class="hive-loading"><div class="hive-spinner"></div><span>Loading portfolio...</span></div>';

    fetch(apiUrl(API_BASE + '?uid=' + encodeURIComponent(user.uid) +
      '&displayName=' + encodeURIComponent(user.displayName || '') +
      '&photoURL=' + encodeURIComponent(user.photoURL || '')))
      .then(function(r) { return r.json(); })
      .then(function(data) {
        renderPortfolio(data, container);
      })
      .catch(function(err) {
        container.innerHTML = '<div class="hive-error">Failed to load portfolio: ' + err.message + '</div>';
      });
  }

  function renderPortfolio(data, container) {
    if (data.error) {
      container.innerHTML = '<div class=\"hive-error\">' + data.error + '</div>';
      return;
    }
    var holdings = data.holdings || {};
    var cash = (typeof data.cash === 'number') ? data.cash : 0;
    var totalHoldingsValue = (typeof data.totalHoldingsValue === 'number') ? data.totalHoldingsValue : 0;
    var totalValue = (typeof data.totalValue === 'number') ? data.totalValue : 0;
    var ret = (typeof data.return === 'number') ? data.return : 0;
    var holdingKeys = Object.keys(holdings);
    var hasHoldings = holdingKeys.length > 0;

    var html = '<div class="hive-portfolio-summary">' +
      '<div class="hive-summary-card">' +
      '<div class="hive-summary-label">Cash Balance</div>' +
      '<div class="hive-summary-value">$' + cash.toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2}) + '</div>' +
      '</div>' +
      '<div class="hive-summary-card">' +
      '<div class="hive-summary-label">Holdings Value</div>' +
      '<div class="hive-summary-value">$' + totalHoldingsValue.toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2}) + '</div>' +
      '</div>' +
      '<div class="hive-summary-card hive-summary-total">' +
      '<div class="hive-summary-label">Total Portfolio</div>' +
      '<div class="hive-summary-value">$' + totalValue.toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2}) + '</div>' +
      '</div>' +
      '<div class="hive-summary-card ' + (ret >= 0 ? 'hive-positive' : 'hive-negative') + '">' +
      '<div class="hive-summary-label">Return</div>' +
      '<div class="hive-summary-value">' + (ret >= 0 ? '+' : '') + ret + '%</div>' +
      '</div>' +
      '</div>';

    if (!hasHoldings) {
      html += '<div class="hive-empty-holdings">' +
        '<p>Your portfolio is empty. Start trading stocks from our coverage universe.</p>' +
        '<button class="hive-cta-btn" onclick="openTradeModal()">Make Your First Trade</button>' +
        '</div>';
    } else {
      html += '<div class="hive-holdings-section">';
      html += '<div class="hive-section-header"><h3>Holdings</h3><button class="hive-cta-btn hive-cta-sm" onclick="openTradeModal()">+ Trade</button></div>';
      html += '<div class="hive-holdings-table-wrap"><table class="hive-holdings-table">' +
        '<thead><tr><th>Ticker</th><th>Shares</th><th>Price</th><th>Value</th><th>% of PF</th></tr></thead><tbody>';

      var keys = Object.keys(holdings).sort(function(a, b) {
        return (holdings[b].value || 0) - (holdings[a].value || 0);
      });
      for (var i = 0; i < keys.length; i++) {
        var ticker = keys[i];
        var h = holdings[ticker];
        var pct = data.totalValue > 0 ? ((h.value / data.totalValue) * 100).toFixed(1) : '0.0';
        var info = getStockInfo(ticker);
        html += '<tr class="hive-holding-row" onclick="openTradeModal(\'' + ticker + '\')" style="cursor:pointer">' +
          '<td class="hive-ticker-cell"><span class="hive-ticker">' + ticker + '</span><div class="hive-holding-name">' + info.name + '</div></td>' +
          '<td>' + h.shares + '</td>' +
          '<td class="hive-mono">$' + h.price.toFixed(2) + '</td>' +
          '<td class="hive-mono">$' + h.value.toFixed(2) + '</td>' +
          '<td>' + pct + '%</td>' +
          '</tr>';
      }

      html += '</tbody></table></div></div>';
    }

    // Trade history
    if (data.trades && data.trades.length > 0) {
      html += '<div class="hive-trade-history">';
      html += '<div class="hive-section-header"><h3>Recent Trades</h3></div>';
      html += '<div class="hive-trade-list">';
      for (var i = 0; i < Math.min(data.trades.length, 20); i++) {
        var t = data.trades[i];
        var cls = t.action === 'buy' ? 'hive-trade-buy' : 'hive-trade-sell';
        var date = new Date(t.date);
        var dateStr = date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' });
        html += '<div class="hive-trade-row ' + cls + '">' +
          '<span class="hive-trade-action">' + t.action.toUpperCase() + '</span>' +
          '<span class="hive-trade-ticker">' + t.ticker + '</span>' +
          '<span class="hive-trade-shares">' + t.shares + ' shares @ $' + t.price.toFixed(2) + '</span>' +
          '<span class="hive-trade-date">' + dateStr + '</span>' +
          '</div>';
      }
      html += '</div></div>';
    }

    container.innerHTML = html;
  }

  // === Trade Modal ===
  window.openTradeModal = function(prefillTicker) {
    var existing = document.getElementById('hiveTradeModal');
    if (existing) existing.remove();

    var user = getCurrentUser();
    if (!user) {
      showHiveJoinModal();
      return;
    }

    var modal = document.createElement('div');
    modal.id = 'hiveTradeModal';
    modal.className = 'hive-modal-overlay';
    modal.innerHTML = '<div class="hive-modal">' +
      '<div class="hive-modal-header">' +
      '<h3>Execute Trade</h3>' +
      '<button class="hive-modal-close" onclick="closeTradeModal()">&times;</button>' +
      '</div>' +
      '<div class="hive-modal-body">' +
      '<div class="hive-form-group">' +
      '<label>Ticker</label>' +
      '<input type="text" class="hive-input" id="hiveTradeTicker" placeholder="e.g. NVDA" value="' + (prefillTicker || '') + '" maxlength="5" style="text-transform:uppercase" autocomplete="off">' +
      '<div class="hive-ticker-suggestions" id="hiveTickerSuggestions"></div>' +
      '</div>' +
      '<div class="hive-form-group">' +
      '<label>Action</label>' +
      '<div class="hive-toggle-group">' +
      '<button class="hive-toggle-btn hive-toggle-active" data-action="buy" onclick="setTradeAction(\'buy\')">Buy</button>' +
      '<button class="hive-toggle-btn" data-action="sell" onclick="setTradeAction(\'sell\')">Sell</button>' +
      '</div>' +
      '</div>' +
      '<div class="hive-form-group">' +
      '<label>Shares</label>' +
      '<input type="number" class="hive-input" id="hiveTradeShares" placeholder="Number of shares" min="1" step="1">' +
      '</div>' +
      '<div class="hive-trade-preview" id="hiveTradePreview">Enter a ticker and shares to see preview</div>' +
      '<div class="hive-trade-error" id="hiveTradeError" style="display:none"></div>' +
      '</div>' +
      '<div class="hive-modal-footer">' +
      '<button class="hive-btn hive-btn-secondary" onclick="closeTradeModal()">Cancel</button>' +
      '<button class="hive-btn hive-btn-primary" id="hiveTradeSubmit" onclick="submitTrade()">Submit Trade</button>' +
      '</div>' +
      '</div>';

    document.querySelector('.hive-app').appendChild(modal);
    setTimeout(function() { modal.classList.add('hive-modal-open'); }, 10);

    // Setup ticker input
    var tickerInput = document.getElementById('hiveTradeTicker');
    var suggestions = document.getElementById('hiveTickerSuggestions');

    tickerInput.addEventListener('input', function() {
      var val = this.value.toUpperCase();
      this.value = val;
      updateTradePreview();
      if (val.length < 1) { suggestions.innerHTML = ''; suggestions.style.display = 'none'; return; }
      // Search both ticker AND company name
      var valLower = val.toLowerCase();
      var matches = STOCKS.filter(function(s) {
        return s.ticker.indexOf(val) === 0 || s.name.toLowerCase().indexOf(valLower) !== -1;
      }).slice(0, 8);
      if (matches.length > 0) {
        suggestions.innerHTML = matches.map(function(s) {
          return '<div class="hive-suggestion-item" onclick="selectTicker(\'' + s.ticker + '\')"><span class="hive-sug-ticker">' + s.ticker + '</span> <span class="hive-sug-name">— ' + s.name + '</span></div>';
        }).join('');
        suggestions.style.display = 'block';
      } else {
        suggestions.innerHTML = '';
        suggestions.style.display = 'none';
      }
    });

    tickerInput.addEventListener('blur', function() {
      setTimeout(function() { suggestions.style.display = 'none'; }, 200);
    });

    var sharesInput = document.getElementById('hiveTradeShares');
    sharesInput.addEventListener('input', updateTradePreview);
  };

  window.closeTradeModal = function() {
    var modal = document.getElementById('hiveTradeModal');
    if (modal) {
      modal.classList.remove('hive-modal-open');
      setTimeout(function() { modal.remove(); }, 300);
    }
  };

  window.selectTicker = function(ticker) {
    document.getElementById('hiveTradeTicker').value = ticker;
    document.getElementById('hiveTickerSuggestions').style.display = 'none';
    updateTradePreview();
  };

  window.setTradeAction = function(action) {
    document.querySelectorAll('.hive-toggle-btn').forEach(function(b) {
      b.classList.remove('hive-toggle-active');
    });
    document.querySelector('.hive-toggle-btn[data-action="' + action + '"]').classList.add('hive-toggle-active');
    updateTradePreview();
  };

  function getTradeAction() {
    var active = document.querySelector('.hive-toggle-btn.hive-toggle-active');
    return active ? active.getAttribute('data-action') : 'buy';
  }

  function updateTradePreview() {
    var preview = document.getElementById('hiveTradePreview');
    var error = document.getElementById('hiveTradeError');
    error.style.display = 'none';
    var ticker = document.getElementById('hiveTradeTicker').value.toUpperCase();
    var shares = parseInt(document.getElementById('hiveTradeShares').value, 10);
    if (!ticker || !shares || shares < 1) {
      preview.textContent = 'Enter a ticker and shares to see preview';
      return;
    }
    if (COVERAGE_UNIVERSE.indexOf(ticker) === -1) {
      preview.innerHTML = '<span style="color:var(--red)">⚠ ' + ticker + ' is not in our coverage universe</span>';
      return;
    }
    var action = getTradeAction();
    fetch('/api/prices?ticker=' + ticker)
      .then(function(r) { return r.json(); })
      .then(function(data) {
        var price = data.price || 0;
        var total = price * shares;
        preview.innerHTML = '<div class="hive-preview-row"><span>Action</span><span class="hive-preview-' + action + '">' + action.toUpperCase() + '</span></div>' +
          '<div class="hive-preview-row"><span>Ticker</span><span class="hive-ticker">' + ticker + '</span></div>' +
          '<div class="hive-preview-row"><span>Shares</span><span>' + shares + '</span></div>' +
          '<div class="hive-preview-row"><span>Price</span><span class="hive-mono">$' + price.toFixed(2) + '</span></div>' +
          '<div class="hive-preview-row hive-preview-total"><span>Total</span><span class="hive-mono">$' + total.toFixed(2) + '</span></div>';
      })
      .catch(function() {
        preview.textContent = 'Ticker price unavailable — try again';
      });
  }

  window.submitTrade = function() {
    var user = getCurrentUser();
    if (!user) { closeTradeModal(); return; }

    var btn = document.getElementById('hiveTradeSubmit');
    var error = document.getElementById('hiveTradeError');
    btn.disabled = true;
    btn.textContent = 'Processing...';
    error.style.display = 'none';

    var ticker = document.getElementById('hiveTradeTicker').value.toUpperCase();
    var action = getTradeAction();
    var shares = parseInt(document.getElementById('hiveTradeShares').value, 10);

    if (!ticker || COVERAGE_UNIVERSE.indexOf(ticker) === -1) {
      error.textContent = 'Please enter a valid ticker from our coverage universe';
      error.style.display = 'block';
      btn.disabled = false;
      btn.textContent = 'Submit Trade';
      return;
    }
    if (!shares || shares < 1) {
      error.textContent = 'Please enter a valid number of shares';
      error.style.display = 'block';
      btn.disabled = false;
      btn.textContent = 'Submit Trade';
      return;
    }

    fetch(API_BASE, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        uid: user.uid,
        token: getToken(),
        displayName: user.displayName,
        photoURL: user.photoURL,
        ticker: ticker,
        action: action,
        shares: shares
      })
    })
    .then(function(r) { return r.json(); })
    .then(function(data) {
      if (data.error) {
        error.textContent = data.error;
        error.style.display = 'block';
        btn.disabled = false;
        btn.textContent = 'Submit Trade';
        return;
      }
      closeTradeModal();
      loadPortfolio();
      showToast(action === 'buy' ? 'Bought' : 'Sold' + ' ' + shares + ' shares of ' + ticker + ' @ $' + data.trade.price.toFixed(2));
    })
    .catch(function(err) {
      error.textContent = 'Network error: ' + err.message;
      error.style.display = 'block';
      btn.disabled = false;
      btn.textContent = 'Submit Trade';
    });
  };

  // === Leaderboard ===
  function loadLeaderboard(period) {
    period = period || 'monthly';
    var container = document.getElementById('hiveLeaderboardContent');
    if (!container) return;

    container.innerHTML = '<div class="hive-loading"><div class="hive-spinner"></div><span>Loading leaderboard...</span></div>';

    var periodParam = period === 'monthly' ? 'monthly' : period === 'weekly' ? 'weekly' : 'alltime';

    var url = API_BASE + '?leaderboard=' + periodParam;
    var user = getCurrentUser();
    if (user && user.uid) url += '&uid=' + encodeURIComponent(user.uid);

    fetch(url)
      .then(function(r) { return r.json(); })
      .then(function(data) {
        renderLeaderboard(data, container, period);
      })
      .catch(function(err) {
        container.innerHTML = '<div class="hive-error">Failed to load leaderboard: ' + err.message + '</div>';
      });
  }

  function renderLeaderboard(data, container, period) {
    var entries = data.leaderboard || [];
    var top10 = entries.slice(0, 10);
    var user = getCurrentUser();
    var currentUid = user ? user.uid : null;

    if (entries.length === 0) {
      container.innerHTML = '<div class="hive-empty-state"><p>No traders yet. Be the first to join The Hive!</p></div>';
      return;
    }

    var html = '<div class="hive-lb-header">' +
      '<span class="hive-lb-count">' + (data.totalParticipants || 0) + ' participants</span>' +
      '</div>';

    // Your Rank section
    var yourRank = data.yourRank;
    if (yourRank) {
      var isInTop10 = yourRank.rank <= 10;
      var inTop10Badge = isInTop10 ? ' <span class="hive-rank-badge">Top 10</span>' : '';
      var rankEmoji = yourRank.rank === 1 ? '🥇' : yourRank.rank === 2 ? '🥈' : yourRank.rank === 3 ? '🥉' : '#' + yourRank.rank;
      html += '<div class="hive-your-rank">' +
        '<div class="hive-your-rank-label">Your Rank</div>' +
        '<div class="hive-your-rank-value">' + rankEmoji + ' <strong>' + yourRank.rank + '</strong> of ' + yourRank.totalParticipants + inTop10Badge + '</div>' +
        '<div class="hive-your-rank-value">$' + yourRank.value.toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2}) + ' ' +
        '<span class="' + (yourRank.return >= 0 ? 'hive-positive' : 'hive-negative') + '">' + (yourRank.return >= 0 ? '+' : '') + yourRank.return + '%</span></div>' +
        '</div>';
    }

    html += '<div class="hive-lb-table-wrap"><table class="hive-lb-table">' +
      '<thead><tr><th>Rank</th><th>Trader</th><th>Value</th><th>Return</th><th>Trades</th></tr></thead><tbody>';

    for (var i = 0; i < top10.length; i++) {
      var e = top10[i];
      var isMe = e.uid === currentUid;
      var rankClass = 'hive-lb-rank';
      if (e.rank === 1) rankClass += ' hive-rank-1';
      else if (e.rank === 2) rankClass += ' hive-rank-2';
      else if (e.rank === 3) rankClass += ' hive-rank-3';
      if (isMe) rankClass += ' hive-rank-me';
      var medal = e.rank === 1 ? '🥇' : e.rank === 2 ? '🥈' : e.rank === 3 ? '🥉' : '#' + e.rank;

      html += '<tr class="' + (isMe ? 'hive-lb-row-me' : '') + '">' +
        '<td class="' + rankClass + '">' + medal + '</td>' +
        '<td class="hive-lb-user">' +
          (e.photoURL ? '<img src="' + e.photoURL + '" class="hive-lb-avatar" onerror="this.style.display=\'none\'">' : '<div class="hive-lb-avatar-placeholder">' + (e.displayName ? e.displayName.charAt(0).toUpperCase() : '?') + '</div>') +
          '<span class="hive-lb-name">' + (e.displayName || 'Anonymous') + '</span>' +
        '</td>' +
        '<td class="hive-mono">$' + e.value.toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2}) + '</td>' +
        '<td class="' + (e.return >= 0 ? 'hive-positive' : 'hive-negative') + '">' + (e.return >= 0 ? '+' : '') + e.return + '%</td>' +
        '<td>' + e.trades + '</td>' +
        '</tr>';
    }

    html += '</tbody></table></div>';
    container.innerHTML = html;
  }

  // === Signal Master ===
  function loadSignalMaster() {
    var container = document.getElementById('hiveSignalMasterContent');
    if (!container) return;

    container.innerHTML = '<div class="hive-loading"><div class="hive-spinner"></div><span>Loading Signal Master...</span></div>';

    fetch(API_BASE + '?signal-master=true')
      .then(function(r) { return r.json(); })
      .then(function(data) {
        renderSignalMaster(data, container);
      })
      .catch(function(err) {
        container.innerHTML = '<div class="hive-error">Failed to load Signal Master: ' + err.message + '</div>';
      });
  }

  function renderSignalMaster(data, container) {
    var holdings = data.holdings || [];

    if (holdings.length === 0) {
      container.innerHTML = '<div class="hive-empty-state"><p>Not enough data yet. Signal Master activates when enough traders join.</p></div>';
      return;
    }

    var user = getCurrentUser();
    var html = '<div class="hive-sm-header">' +
      '<p class="hive-sm-desc">Aggregated portfolio of the top ' + data.topCount + ' traders (' + Math.ceil(data.topCount * 10) + '% of participants)</p>' +
      '<div class="hive-sm-stats">' +
      '<span>Portfolios: <strong>' + data.totalPortfolios + '</strong></span>' +
      '<span>Total Value: <strong>$' + (data.totalAggValue || 0).toLocaleString(undefined, {maximumFractionDigits: 0}) + '</strong></span>' +
      '</div>' +
      '</div>';

    html += '<div class="hive-holdings-table-wrap"><table class="hive-holdings-table">' +
      '<thead><tr><th>#</th><th>Ticker</th><th>Allocation</th><th>Value</th></tr></thead><tbody>';

    for (var i = 0; i < holdings.length; i++) {
      var h = holdings[i];
      var rank = i + 1;
      html += '<tr>' +
        '<td>' + rank + '</td>' +
        '<td class="hive-ticker-cell"><span class="hive-ticker">' + h.ticker + '</span></td>' +
        '<td><div class="hive-alloc-bar"><div class="hive-alloc-fill" style="width:' + h.allocation + '%"></div><span class="hive-alloc-label">' + h.allocation + '%</span></div></td>' +
        '<td class="hive-mono">$' + (h.value || 0).toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2}) + '</td>' +
        '</tr>';
    }

    html += '</tbody></table></div>';

    html += '<div class="hive-sm-thesis">' +
      '<h4>Signal Master Thesis</h4>' +
      '<p><strong>Concentration in Leaders:</strong> The smartest money clusters around sector leaders with durable competitive advantages — AI compute (NVDA, AVGO), defense prime contractors (LMT, RTX), and cybersecurity platforms (CRWD, PANW).</p>' +
      '<p><strong>Space & Defense Upside:</strong> Emerging space infrastructure plays (RKLB, ASTS) and next-gen defense tech (PLTR, AXON) attract outsized allocations from top performers.</p>' +
      '<p><strong>Balanced Exposure:</strong> Top traders maintain 4-7 positions across at least 3 sectors, avoiding over-concentration while capturing thematic upside.</p>' +
      '</div>';

    container.innerHTML = html;
  }

  // === Rules Tab ===
  function loadRules() {
    var container = document.getElementById('hiveRulesContent');
    if (!container) return;

    var html =
      '<div class="hive-rules-section">' +
      // Trading Rules
      '<div class="hive-rules-card">' +
      '<div class="hive-rules-icon">📋</div>' +
      '<h3 class="hive-rules-heading">Trading Rules</h3>' +
      '<ul class="hive-rules-list">' +
      '<li>You start with a <strong>$100,000</strong> simulated portfolio</li>' +
      '<li>Minimum <strong>3 positions</strong>, maximum <strong>15 positions</strong> at any time</li>' +
      '<li>Maximum <strong>40% allocation</strong> per ticker (no single stock concentration)</li>' +
      '<li>Trades execute at <strong>market close prices</strong> (simulated at 4pm EST)</li>' +
      '<li>Cash-only — <strong>no margin</strong> or leverage allowed</li>' +
      '<li><strong>No short selling</strong> — long-only trading only</li>' +
      '</ul>' +
      '</div>' +
      // Coverage Universe
      '<div class="hive-rules-card">' +
      '<div class="hive-rules-icon">🎯</div>' +
      '<h3 class="hive-rules-heading">Coverage Universe</h3>' +
      '<p class="hive-rules-text">You can only trade stocks in The Signal\'s coverage universe — <strong>54 tickers</strong> across six sectors:</p>' +
      '<ul class="hive-rules-list">' +
      '<li><span class="hive-rules-sector" style="color:#3b82f6">AI</span> — NVDA, AMD, AVGO, MRVL, TSM, ASML, MU, CBRS, CRWV, NBIS, INTC, IREN, LRCX, AMAT, QCOM, SMCI</li>' +
      '<li><span class="hive-rules-sector" style="color:#22c55e">Cybersecurity</span> — CRWD, PANW, FTNT, ZS, S, CHKP, CYBR, TENB, RBRK</li>' +
      '<li><span class="hive-rules-sector" style="color:#fbbf24">Defense</span> — LMT, RTX, NOC, GD, LHX, KTOS, AVAV, PL, AXON, GE, PLTR, ONDS</li>' +
      '<li><span class="hive-rules-sector" style="color:#a78bfa">Space</span> — RKLB, RDW, LUNR, ASTS</li>' +
      '<li><span class="hive-rules-sector" style="color:#f87171">Mega-Cap</span> — AAPL, MSFT, GOOGL, AMZN, META, TSLA, NFLX</li>' +
      '<li><span class="hive-rules-sector" style="color:#06b6d4">Quantum</span> — IONQ, QBTS, QUBT, RGTI</li>' +
      '</ul>' +
      '</div>' +
      // Leaderboard Scoring
      '<div class="hive-rules-card">' +
      '<div class="hive-rules-icon">🏆</div>' +
      '<h3 class="hive-rules-heading">Leaderboard Scoring</h3>' +
      '<ul class="hive-rules-list">' +
      '<li>Ranked by <strong>total return percentage</strong> (current value ÷ $100,000)</li>' +
      '<li>Three periods: <strong>Weekly</strong>, <strong>30-Day</strong>, <strong>All-Time</strong></li>' +
      '<li>You must have at least <strong>3 active positions</strong> to appear on the leaderboard</li>' +
      '<li>Leaderboard updates every time you trade (prices refresh on page load)</li>' +
      '</ul>' +
      '</div>' +
      // Signal Master
      '<div class="hive-rules-card">' +
      '<div class="hive-rules-icon">⚡</div>' +
      '<h3 class="hive-rules-heading">Signal Master</h3>' +
      '<ul class="hive-rules-list">' +
      '<li>The <strong>top 10% of traders</strong> by portfolio return are aggregated into the Signal Master portfolio</li>' +
      '<li>Signal Master holdings show where the smartest money is concentrated</li>' +
      '<li>Updated in real-time as trades are executed</li>' +
      '<li>Use Signal Master allocations as a <strong>reference</strong> — not financial advice</li>' +
      '</ul>' +
      '</div>' +
      // Code of Conduct
      '<div class="hive-rules-card">' +
      '<div class="hive-rules-icon">🤝</div>' +
      '<h3 class="hive-rules-heading">Code of Conduct</h3>' +
      '<ul class="hive-rules-list">' +
      '<li><strong>One account per person</strong> — no multi-account farming</li>' +
      '<li><strong>No market manipulation</strong> — coordinated trades or price-target collusion is prohibited</li>' +
      '<li><strong>Fair play</strong> — this is a community game, respect other traders</li>' +
      '<li>Violations may result in account suspension or leaderboard removal</li>' +
      '</ul>' +
      '</div>' +
      // Important Dates
      '<div class="hive-rules-card">' +
      '<div class="hive-rules-icon">📅</div>' +
      '<h3 class="hive-rules-heading">Important Dates &amp; Notes</h3>' +
      '<ul class="hive-rules-list">' +
      '<li>Trades simulate execution at <strong>4:00 PM EST</strong> using closing prices</li>' +
      '<li>Weekend and holiday trades queue for next market session</li>' +
      '<li>Portfolio values are for <strong>educational purposes only</strong> — not real money</li>' +
      '<li>The Hive may be reset periodically for balance and fairness</li>' +
      '</ul>' +
      '</div>' +
      '<div class="hive-rules-footer">' +
      '<p>⚠️ <strong>Disclaimer:</strong> The Hive is a simulated trading game for educational purposes. All portfolio values are fictional. Past performance does not guarantee future results. No real investments are made.</p>' +
      '</div>' +
      '</div>';

    container.innerHTML = html;
  }

  // === Stocks Tab ===
  function loadStocks() {
    var container = document.getElementById('hiveStocksContent');
    if (!container) return;

    container.innerHTML = '<div class="hive-loading"><div class="hive-spinner"></div><span>Loading stocks...</span></div>';

    fetch(API_BASE + '?stocks=true')
      .then(function(r) { return r.json(); })
      .then(function(data) {
        renderStocks(data, container);
      })
      .catch(function(err) {
        // Fallback: render from local data with no prices
        renderStocks({ stocks: STOCKS.map(function(s) { return { ticker: s.ticker, name: s.name, sector: s.sector, price: null }; }) }, container);
      });
  }

  function renderStocks(data, container) {
    var stocks = data.stocks || [];

    // Group by sector
    var grouped = {};
    var sectorNames = SECTOR_ORDER.slice();
    for (var i = 0; i < stocks.length; i++) {
      var s = stocks[i];
      if (!grouped[s.sector]) grouped[s.sector] = [];
      grouped[s.sector].push(s);
    }

    // Sector colors
    var sectorColors = {
      'AI': '#3b82f6',
      'Cybersecurity': '#22c55e',
      'Defense': '#fbbf24',
      'Space': '#a78bfa',
      'Mega-Cap': '#f87171',
      'Quantum': '#06b6d4'
    };

    var html = '<div class="hive-stocks-search-wrap">' +
      '<input type="text" class="hive-input hive-stocks-search" id="hiveStocksSearch" placeholder="Search by ticker or company name..." autocomplete="off">' +
      '</div>' +
      '<div class="hive-stocks-list" id="hiveStocksList">';

    for (var si = 0; si < sectorNames.length; si++) {
      var sec = sectorNames[si];
      var secStocks = grouped[sec] || [];
      if (secStocks.length === 0) continue;
      var color = sectorColors[sec] || '#888';

      html += '<div class="hive-sector-group">' +
        '<div class="hive-sector-header" style="border-left:3px solid ' + color + ';color:' + color + '" onclick="toggleSector(this)">' +
          '<span class="hive-sector-arrow">▾</span>' +
          '<span class="hive-sector-name">' + sec + '</span>' +
          '<span class="hive-sector-count">' + secStocks.length + ' stocks</span>' +
        '</div>' +
        '<div class="hive-sector-body">';

      for (var j = 0; j < secStocks.length; j++) {
        var st = secStocks[j];
        var priceHtml = st.price ? '<span class="hive-mono hive-stock-price">$' + st.price.toFixed(2) + '</span>' : '<span class="hive-mono hive-stock-price" style="color:var(--text-muted)">—</span>';
        html += '<div class="hive-stock-row" onclick="openTradeModal(\'' + st.ticker + '\')">' +
          '<div class="hive-stock-info">' +
            '<span class="hive-stock-ticker">' + st.ticker + '</span>' +
            '<span class="hive-stock-name">' + (st.name || st.ticker) + '</span>' +
          '</div>' +
          '<div class="hive-stock-right">' +
            '<span class="hive-stock-tag" style="background:' + color + '20;color:' + color + '">' + st.sector + '</span>' +
            priceHtml +
          '</div>' +
        '</div>';
      }

      html += '</div></div>';
    }

    html += '</div>';
    container.innerHTML = html;

    // Setup search
    var searchInput = document.getElementById('hiveStocksSearch');
    if (searchInput) {
      searchInput.addEventListener('input', function() {
        var q = this.value.toLowerCase().trim();
        var rows = document.querySelectorAll('.hive-stock-row');
        var groups = document.querySelectorAll('.hive-sector-group');
        for (var i = 0; i < rows.length; i++) {
          var row = rows[i];
          var tickerEl = row.querySelector('.hive-stock-ticker');
          var nameEl = row.querySelector('.hive-stock-name');
          var ticker = tickerEl ? tickerEl.textContent.toLowerCase() : '';
          var name = nameEl ? nameEl.textContent.toLowerCase() : '';
          var match = !q || ticker.indexOf(q) === 0 || name.indexOf(q) !== -1;
          row.style.display = match ? '' : 'none';
        }
        // Hide empty groups
        for (var g = 0; g < groups.length; g++) {
          var visible = groups[g].querySelectorAll('.hive-stock-row[style*="display: none"]');
          var total = groups[g].querySelectorAll('.hive-stock-row').length;
          groups[g].style.display = (visible.length === total && total > 0 && q) ? 'none' : '';
        }
      });
    }
  }

  window.toggleSector = function(header) {
    var body = header.nextElementSibling;
    var arrow = header.querySelector('.hive-sector-arrow');
    if (body) {
      body.classList.toggle('hive-sector-collapsed');
      if (arrow) arrow.textContent = body.classList.contains('hive-sector-collapsed') ? '▸' : '▾';
    }
  };

  // === Toast notification ===
  function showToast(message) {
    var existing = document.querySelector('.hive-toast');
    if (existing) existing.remove();
    var toast = document.createElement('div');
    toast.className = 'hive-toast';
    toast.textContent = message;
    var targetEl = document.querySelector('.hive-app') || document.body;
    targetEl.appendChild(toast);
    setTimeout(function() { toast.classList.add('hive-toast-show'); }, 10);
    setTimeout(function() {
      toast.classList.remove('hive-toast-show');
      setTimeout(function() { toast.remove(); }, 300);
    }, 3000);
  }

  // === Tab switching ===
  function setupTabs() {
    var tabContainer = document.getElementById('hiveTabs');
    if (!tabContainer) return;
    var tabs = tabContainer.querySelectorAll('.hive-tab');
    tabs.forEach(function(tab) {
      tab.addEventListener('click', function() {
        var target = this.getAttribute('data-tab');
        tabs.forEach(function(t) { t.classList.remove('hive-tab-active'); });
        this.classList.add('hive-tab-active');
        document.querySelectorAll('.hive-tab-content').forEach(function(c) { c.classList.remove('hive-tab-active'); });
        var contentId = 'hiveTab' + target.charAt(0).toUpperCase() + target.slice(1);
        var content = document.getElementById(contentId);
        if (content) content.classList.add('hive-tab-active');

        if (target === 'portfolio') loadPortfolio();
        else if (target === 'leaderboard') {
          var activePeriod = document.querySelector('.hive-lb-period-btn.hive-lb-period-active');
          loadLeaderboard(activePeriod ? activePeriod.getAttribute('data-period') : 'monthly');
        }
        else if (target === 'signalmaster') loadSignalMaster();
        else if (target === 'stocks') loadStocks();
        else if (target === 'rules') loadRules();
      });
    });

    // Leaderboard period buttons
    var periodBtns = document.querySelectorAll('.hive-lb-period-btn');
    periodBtns.forEach(function(btn) {
      btn.addEventListener('click', function() {
        periodBtns.forEach(function(b) { b.classList.remove('hive-lb-period-active'); });
        this.classList.add('hive-lb-period-active');
        loadLeaderboard(this.getAttribute('data-period'));
      });
    });

    // Initial load
    var activeTab = document.querySelector('.hive-tab.hive-tab-active');
    if (activeTab) {
      var target = activeTab.getAttribute('data-tab');
      if (target === 'portfolio') loadPortfolio();
      else if (target === 'leaderboard') loadLeaderboard('monthly');
      else if (target === 'signalmaster') loadSignalMaster();
      else if (target === 'stocks') loadStocks();
      else if (target === 'rules') loadRules();
    }
  }

  // === Homepage section integration ===
  function loadHomepageHive() {
    var section = document.getElementById('hiveHomeSection');
    if (!section) return;

    // Load Signal Master spotlight
    var spotlight = section.querySelector('.hive-spotlight-holdings');
    if (spotlight) {
      fetch(API_BASE + '?signal-master=true')
        .then(function(r) { return r.json(); })
        .then(function(data) {
          var holdings = data.holdings || [];
          if (holdings.length === 0) {
            spotlight.innerHTML = '<div class="hive-spotlight-empty">Not enough traders yet</div>';
            return;
          }
          var html = '';
          for (var i = 0; i < Math.min(holdings.length, 3); i++) {
            var h = holdings[i];
            html += '<div class="hive-spotlight-item">' +
              '<span class="hive-ticker">' + h.ticker + '</span>' +
              '<span class="hive-spotlight-bar-wrap"><span class="hive-spotlight-bar" style="width:' + h.allocation + '%"></span></span>' +
              '<span class="hive-spotlight-pct">' + h.allocation + '%</span>' +
              '</div>';
          }
          spotlight.innerHTML = html;
        })
        .catch(function() {});
    }

    // Load leaderboard preview
    var preview = section.querySelector('.hive-preview-entries');
    if (preview) {
      fetch(API_BASE + '?leaderboard=monthly')
        .then(function(r) { return r.json(); })
        .then(function(data) {
          var entries = data.leaderboard || [];
          if (entries.length === 0) {
            preview.innerHTML = '<div class="hive-preview-empty">No traders yet. Be the first!</div>';
            return;
          }
          var html = '';
          var slice = entries.slice(0, 5);
          for (var i = 0; i < slice.length; i++) {
            var e = slice[i];
            var medal = e.rank === 1 ? '🥇' : e.rank === 2 ? '🥈' : e.rank === 3 ? '🥉' : '#' + e.rank;
            html += '<div class="hive-preview-row">' +
              '<span class="hive-preview-rank ' + (e.rank <= 3 ? 'hive-rank-' + e.rank : '') + '">' + medal + '</span>' +
              '<span class="hive-preview-name">' + (e.displayName || 'Anonymous') + '</span>' +
              '<span class="hive-preview-value">$' + e.value.toLocaleString(undefined, {minimumFractionDigits: 0}) + '</span>' +
              '<span class="' + (e.return >= 0 ? 'hive-positive' : 'hive-negative') + '">' + (e.return >= 0 ? '+' : '') + e.return + '%</span>' +
              '</div>';
          }
          preview.innerHTML = html;
        })
        .catch(function() {});
    }
  }

  // === Auth Modal (Login / Register / Google) ===
  window.showHiveJoinModal = function(view) {
    view = view || 'login';
    var existing = document.getElementById('hiveJoinModal');
    if (existing) return;

    var overlay = document.createElement('div');
    overlay.className = 'hive-modal-overlay';
    overlay.id = 'hiveJoinModal';
    overlay.innerHTML =
      '<div class="hive-modal hive-auth-modal">' +
      '<div class="hive-modal-header">' +
      '<h3>🐝 The Hive</h3>' +
      '<button class="hive-modal-close" onclick="closeJoinModal()">&times;</button>' +
      '</div>' +
      '<div class="hive-auth-tabs">' +
      '<button class="hive-auth-tab hive-auth-tab-active" data-authview="login" onclick="switchAuthView(\'login\')">Sign In</button>' +
      '<button class="hive-auth-tab" data-authview="register" onclick="switchAuthView(\'register\')">Register</button>' +
      '</div>' +
      '<div class="hive-modal-body">' +
      // Login view
      '<div class="hive-auth-view" id="hiveAuthLogin">' +
      '<div class="hive-form-group">' +
      '<label>Username</label>' +
      '<input type="text" class="hive-input" id="hiveLoginUsername" placeholder="Your username" maxlength="30" autocomplete="username">' +
      '</div>' +
      '<div class="hive-form-group">' +
      '<label>Password</label>' +
      '<input type="password" class="hive-input" id="hiveLoginPassword" placeholder="Your password" autocomplete="current-password">' +
      '</div>' +
      '<div class="hive-auth-error" id="hiveLoginError" style="display:none"></div>' +
      '<button class="hive-cta-btn" id="hiveLoginBtn" style="width:100%;padding:12px;font-size:15px" onclick="hiveLogin()">Sign In</button>' +
      '<div class="hive-auth-divider"><span>or</span></div>' +
      '<div class="hive-google-btn" id="hiveGoogleBtn">' +
      '<div class="g_id_signin" data-type="standard" data-shape="rectangular" data-theme="outline" data-text="signin_with" data-size="large" data-width="280"></div>' +
      '</div>' +
      '</div>' +
      // Register view
      '<div class="hive-auth-view" id="hiveAuthRegister" style="display:none">' +
      '<div class="hive-form-group">' +
      '<label>Username</label>' +
      '<input type="text" class="hive-input" id="hiveRegUsername" placeholder="Choose a username" maxlength="30" autocomplete="username">' +
      '</div>' +
      '<div class="hive-form-group">' +
      '<label>Display Name</label>' +
      '<input type="text" class="hive-input" id="hiveRegDisplayName" placeholder="Your display name" maxlength="30">' +
      '</div>' +
      '<div class="hive-form-group">' +
      '<label>Password</label>' +
      '<input type="password" class="hive-input" id="hiveRegPassword" placeholder="At least 6 characters" autocomplete="new-password">' +
      '</div>' +
      '<div class="hive-form-group">' +
      '<label>Confirm Password</label>' +
      '<input type="password" class="hive-input" id="hiveRegConfirm" placeholder="Confirm your password" autocomplete="new-password">' +
      '</div>' +
      '<div class="hive-auth-error" id="hiveRegError" style="display:none"></div>' +
      '<button class="hive-cta-btn" id="hiveRegBtn" style="width:100%;padding:12px;font-size:15px" onclick="hiveRegister()">Create Account</button>' +
      '</div>' +
      '</div>' +
      '</div>';

    var targetEl = document.querySelector('.hive-app') || document.body;
    targetEl.appendChild(overlay);
    setTimeout(function() { overlay.classList.add('hive-modal-open'); }, 10);

    // Focus first input
    setTimeout(function() {
      var firstInput = document.getElementById(view === 'login' ? 'hiveLoginUsername' : 'hiveRegUsername');
      if (firstInput) firstInput.focus();
    }, 200);

    // Enter key handlers
    setTimeout(function() {
      if (view === 'login') {
        var pw = document.getElementById('hiveLoginPassword');
        if (pw) pw.addEventListener('keydown', function(e) { if (e.key === 'Enter') hiveLogin(); });
      } else {
        var confirm = document.getElementById('hiveRegConfirm');
        if (confirm) confirm.addEventListener('keydown', function(e) { if (e.key === 'Enter') hiveRegister(); });
      }
    }, 300);

    // Load Firebase Auth for Google sign-in (same project as m30a scanner)
    if (typeof firebase === 'undefined') {
      var fbApp = document.createElement('script');
      fbApp.src = 'https://www.gstatic.com/firebasejs/10.14.1/firebase-app-compat.js';
      fbApp.async = true;
      fbApp.defer = true;
      fbApp.onload = function() {
        var fbAuth = document.createElement('script');
        fbAuth.src = 'https://www.gstatic.com/firebasejs/10.14.1/firebase-auth-compat.js';
        fbAuth.async = true;
        fbAuth.defer = true;
        fbAuth.onload = function() {
          initFirebaseGoogleSignIn();
        };
        document.head.appendChild(fbAuth);
      };
      document.head.appendChild(fbApp);
    } else {
      initFirebaseGoogleSignIn();
    }
  };

  var firebaseApp = null;
  var firebaseGoogleProvider = null;

  function initFirebaseGoogleSignIn() {
    try {
      if (typeof firebase === 'undefined' || !firebase.initializeApp) {
        var gSignIn = document.querySelector('.g_id_signin');
        if (gSignIn) {
          gSignIn.innerHTML = '<div style="padding:10px;color:var(--text-muted);font-size:13px;text-align:center;border:1px dashed #333;border-radius:8px;margin-top:4px">Google sign-in unavailable. Use username/password.</div>';
        }
        return;
      }
      // Use same Firebase project as m30a scanner (kalitta-logs)
      if (!firebaseApp) {
        firebaseApp = firebase.initializeApp({
          apiKey: "AIzaSyDhlnHXYACuXc0VWk07JEUA9gMQ3CwZ8Eo",
          authDomain: "kalitta-logs.firebaseapp.com",
          projectId: "kalitta-logs"
        }, "thesignal-hive");
      }
      firebaseGoogleProvider = new firebase.auth.GoogleAuthProvider();

      var gSignIn = document.querySelector('.g_id_signin');
      if (!gSignIn) return;
      gSignIn.innerHTML = '<button class="hive-cta-btn" id="firebaseGoogleBtn" style="width:100%;padding:10px;font-size:14px;background:transparent;border:1px solid #333;border-radius:8px;cursor:pointer;color:var(--text);display:flex;align-items:center;justify-content:center;gap:8px">' +
        '<span style="font-weight:700;color:#fff;background:#4285f4;border-radius:50%;width:22px;height:22px;display:inline-flex;align-items:center;justify-content:center;font-size:13px">G</span>' +
        ' Sign in with Google</button>';
      document.getElementById('firebaseGoogleBtn').onclick = handleFirebaseGoogleSignIn;
    } catch(e) {
      console.warn('Firebase Google sign-in init:', e.message);
      var gSignIn = document.querySelector('.g_id_signin');
      if (gSignIn) {
        gSignIn.innerHTML = '<div style="padding:10px;color:var(--text-muted);font-size:13px;text-align:center">Google sign-in unavailable. Use username/password.</div>';
      }
    }
  }

  function handleFirebaseGoogleSignIn() {
    if (!firebaseApp || !firebaseGoogleProvider) {
      showAuthError('login', 'Google sign-in not initialized. Try again.');
      return;
    }
    // Show loading
    var loginBtn = document.getElementById('firebaseGoogleBtn');
    if (loginBtn) { loginBtn.disabled = true; loginBtn.textContent = 'Signing in...'; }

    firebase.auth(firebaseApp).signInWithPopup(firebaseGoogleProvider)
      .then(function(result) {
        var credential = result.credential;
        var idToken = credential ? credential.idToken : null;
        if (!idToken) {
          showAuthError('login', 'Failed to get Google authentication token.');
          if (loginBtn) resetFirebaseGoogleBtn();
          return;
        }
        // Send idToken to our backend
        fetch(API_BASE + '?action=google-auth', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ credential: idToken })
        })
        .then(function(r) { return r.json(); })
        .then(function(data) {
          if (data.error) {
            showAuthError('login', data.error);
            if (loginBtn) resetFirebaseGoogleBtn();
            return;
          }
          setToken(data.token);
          setCurrentUser(data.user);
          closeJoinModal();
          onAuthSuccess(data.user);
        })
        .catch(function(err) {
          showAuthError('login', 'Network error: ' + err.message);
          if (loginBtn) resetFirebaseGoogleBtn();
        });
      })
      .catch(function(error) {
        if (error.code === 'auth/popup-closed-by-user') {
          // User cancelled — just reset, no error shown
          if (loginBtn) resetFirebaseGoogleBtn();
          return;
        }
        showAuthError('login', error.message || 'Google sign-in failed.');
        if (loginBtn) resetFirebaseGoogleBtn();
      });
  }

  function resetFirebaseGoogleBtn() {
    var btn = document.getElementById('firebaseGoogleBtn');
    if (btn) {
      btn.disabled = false;
      btn.innerHTML = '<span style="font-weight:700;color:#fff;background:#4285f4;border-radius:50%;width:22px;height:22px;display:inline-flex;align-items:center;justify-content:center;font-size:13px">G</span> Sign in with Google';
    }
  }

  window.switchAuthView = function(view) {
    var tabs = document.querySelectorAll('.hive-auth-tab');
    tabs.forEach(function(t) { t.classList.remove('hive-auth-tab-active'); });
    var activeTab = document.querySelector('.hive-auth-tab[data-authview="' + view + '"]');
    if (activeTab) activeTab.classList.add('hive-auth-tab-active');

    document.getElementById('hiveAuthLogin').style.display = view === 'login' ? '' : 'none';
    document.getElementById('hiveAuthRegister').style.display = view === 'register' ? '' : 'none';
  };

  function showAuthError(view, message) {
    var el = document.getElementById(view === 'login' ? 'hiveLoginError' : 'hiveRegError');
    if (el) {
      el.textContent = message;
      el.style.display = 'block';
    }
  }

  window.hiveLogin = function() {
    var username = document.getElementById('hiveLoginUsername');
    var password = document.getElementById('hiveLoginPassword');
    var errorEl = document.getElementById('hiveLoginError');
    var btn = document.getElementById('hiveLoginBtn');

    if (!username || !password) return;
    var u = username.value.trim();
    var p = password.value;

    if (!u || !p) {
      showAuthError('login', 'Please enter your username and password');
      return;
    }

    btn.disabled = true;
    btn.textContent = 'Signing in...';
    errorEl.style.display = 'none';

    fetch(API_BASE + '?action=login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username: u, password: p })
    })
    .then(function(r) { return r.json(); })
    .then(function(data) {
      if (data.error) {
        showAuthError('login', data.error);
        btn.disabled = false;
        btn.textContent = 'Sign In';
        return;
      }
      setToken(data.token);
      setCurrentUser(data.user);
      closeJoinModal();
      onAuthSuccess(data.user);
    })
    .catch(function(err) {
      showAuthError('login', 'Network error: ' + err.message);
      btn.disabled = false;
      btn.textContent = 'Sign In';
    });
  };

  window.hiveRegister = function() {
    var username = document.getElementById('hiveRegUsername');
    var displayName = document.getElementById('hiveRegDisplayName');
    var password = document.getElementById('hiveRegPassword');
    var confirm = document.getElementById('hiveRegConfirm');
    var errorEl = document.getElementById('hiveRegError');
    var btn = document.getElementById('hiveRegBtn');

    if (!username || !password || !confirm) return;
    var u = username.value.trim();
    var d = displayName ? displayName.value.trim() : u;
    var p = password.value;
    var c = confirm.value;

    if (!u || u.length < 3) {
      showAuthError('register', 'Username must be at least 3 characters');
      return;
    }
    if (p.length < 6) {
      showAuthError('register', 'Password must be at least 6 characters');
      return;
    }
    if (p !== c) {
      showAuthError('register', 'Passwords do not match');
      return;
    }

    btn.disabled = true;
    btn.textContent = 'Creating account...';
    errorEl.style.display = 'none';

    fetch(API_BASE + '?action=register', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username: u, password: p, displayName: d })
    })
    .then(function(r) { return r.json(); })
    .then(function(data) {
      if (data.error) {
        showAuthError('register', data.error);
        btn.disabled = false;
        btn.textContent = 'Create Account';
        return;
      }
      setToken(data.token);
      setCurrentUser(data.user);
      closeJoinModal();
      onAuthSuccess(data.user);
    })
    .catch(function(err) {
      showAuthError('register', 'Network error: ' + err.message);
      btn.disabled = false;
      btn.textContent = 'Create Account';
    });
  };

  window.closeJoinModal = function() {
    var modal = document.getElementById('hiveJoinModal');
    if (modal) {
      modal.classList.remove('hive-modal-open');
      setTimeout(function() { modal.remove(); }, 300);
    }
  };

  // Called after successful auth
  function onAuthSuccess(user) {
    // Update nav
    var authLabel = document.getElementById('authLabel');
    if (authLabel) authLabel.textContent = user.displayName || user.username;
    var authUserInfo = document.getElementById('authUserInfo');
    if (authUserInfo) authUserInfo.style.display = 'flex';
    var authOptions = document.getElementById('authOptions');
    if (authOptions) authOptions.style.display = 'none';
    var authName = document.getElementById('authName');
    if (authName) authName.textContent = user.displayName || user.username;

    // Reload portfolio if active
    var activeTab = document.querySelector('.hive-tab.hive-tab-active');
    if (activeTab && activeTab.getAttribute('data-tab') === 'portfolio') {
      loadPortfolio();
    }
    loadHomepageHive();
    showToast('Welcome, ' + (user.displayName || user.username) + '!');
  }

  window.logoutHive = window.hiveLogout = function() {
    clearToken();
    clearCurrentUser();
    var authOptions = document.getElementById('authOptions');
    var authUserInfo = document.getElementById('authUserInfo');
    if (authOptions) authOptions.style.display = '';
    if (authUserInfo) authUserInfo.style.display = 'none';
    showToast('Signed out');
    var activeTab = document.querySelector('.hive-tab.hive-tab-active');
    if (activeTab && activeTab.getAttribute('data-tab') === 'portfolio') {
      loadPortfolio();
    }
  };

  // === Init ===
  document.addEventListener('DOMContentLoaded', function() {
    migrateOldUser();
    setupTabs();
    loadHomepageHive();

    // Handle sessionStorage hint from auth.js profile dropdown
    try {
      var pendingTab = sessionStorage.getItem('hive_open_tab');
      if (pendingTab && window.location.pathname === '/hive') {
        sessionStorage.removeItem('hive_open_tab');
        var tabBtn = document.querySelector('.hive-tab[data-tab="' + pendingTab + '"]');
        if (tabBtn) tabBtn.click();
      }
    } catch(e) {}

    // Listen for auth changes to refresh
    window.addEventListener('storage', function(e) {
      if (e.key === 'hive_user' || e.key === 'hive_token') {
        var activeTab = document.querySelector('.hive-tab.hive-tab-active');
        if (activeTab && activeTab.getAttribute('data-tab') === 'portfolio') {
          loadPortfolio();
        }
        loadHomepageHive();
      }
    });

    // Check existing session on page load
    var token = getToken();
    var user = getCurrentUser();
    if (token && user) {
      // Verify token is still valid
      fetch(API_BASE + '?action=me&token=' + encodeURIComponent(token))
        .then(function(r) { return r.json(); })
        .then(function(data) {
          if (data.authenticated) {
            // Update user info
            setCurrentUser({ uid: data.uid, displayName: data.displayName, username: data.username });
            var authLabel = document.getElementById('authLabel');
            if (authLabel) authLabel.textContent = data.displayName || data.username;
            var authUserInfo = document.getElementById('authUserInfo');
            if (authUserInfo) authUserInfo.style.display = 'flex';
            var authOptions = document.getElementById('authOptions');
            if (authOptions) authOptions.style.display = 'none';
            var authName = document.getElementById('authName');
            if (authName) authName.textContent = data.displayName || data.username;
          } else {
            // Token expired
            clearToken();
            clearCurrentUser();
          }
        })
        .catch(function() {
          // If verification fails, keep local session anyway (offline tolerance)
        });
    }
  });

})();
