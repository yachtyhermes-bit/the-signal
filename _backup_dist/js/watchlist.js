// The Signal — Multi-Watchlist Manager
// Portfolios overview + detail views, live prices via /api/prices,
// premium gating, and stock-page heart integration.
//
// API contract (see api/hive.mjs):
//   GET  /api/hive?action=watchlist&op=list&token=X
//        -> {status:'ok', watchlists:[{id,name,tickers:[{ticker,addedAt}],createdAt}]}
//   POST /api/hive?action=watchlist&op=create {name}            -> full watchlists array
//   POST /api/hive?action=watchlist&op=rename {id,name}         -> full watchlists array
//   POST /api/hive?action=watchlist&op=delete {id}              -> full watchlists array
//   POST /api/hive?action=watchlist&op=add    {id,ticker}       -> full watchlists array
//   POST /api/hive?action=watchlist&op=remove {id,ticker}       -> full watchlists array
//   Mutations return 403 {error} for non-premium; 400 {error} on validation (max 5, bad ticker).
//   GET  /api/hive?action=premium&token=X -> {premium: bool}
//
// Legacy fallback: {status:'ok', watchlist:[items]} is normalized to a single
// unnamed watchlist so old backends keep working.
(function() {
  'use strict';

  var API_BASE = '/api/hive';
  var PRICES_URL = '/api/prices/';
  var INDEX_URL = '/stocks/index.json';
  var MAX_LISTS = 5;
  var TICKER_RE = /^[A-Z0-9.-]{1,10}$/;

  // === State ===

  var state = {
    watchlists: [],   // normalized [{id, name, tickers:[{ticker,addedAt}], createdAt}]
    prices: {},       // ticker -> {price, changePercent, change}
    index: {},        // ticker -> {name, sector}
    premium: null,    // true | false | null (unknown/optimistic)
    loaded: false,    // true once the first list fetch succeeds
    currentId: null,  // id of the open detail list (null = overview)
    sort: 'symbol'
  };

  // === Tiny helpers ===

  function getToken() {
    try { return localStorage.getItem('hive_token'); } catch (e) { return null; }
  }

  function getUser() {
    try { return JSON.parse(localStorage.getItem('hive_user') || 'null'); } catch (e) { return null; }
  }

  function escapeHtml(s) {
    return String(s == null ? '' : s)
      .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;').replace(/'/g, '&#39;');
  }

  function fmtPrice(p) {
    if (p == null || isNaN(p)) return '—';
    return '$' + Number(p).toFixed(2);
  }

  function fmtPct(p) {
    if (p == null || isNaN(p)) return '—';
    return (p >= 0 ? '+' : '') + Number(p).toFixed(2) + '%';
  }

  function showHiveJoin(mode) {
    if (typeof showHiveJoinModal === 'function') showHiveJoinModal(mode || 'login');
    else window.location.href = '/hive';
  }

  // Toast — prefer the page's #watchlistToast; fall back to a tiny
  // self-created one so error surfacing never depends on page markup.
  var toastEl = null;
  var toastTimer = null;
  var toastNavUrl = null;
  function showToast(msg, navUrl) {
    toastEl = document.getElementById('watchlistToast');
    if (!toastEl) {
      toastEl = document.createElement('div');
      toastEl.className = 'watchlist-toast';
      toastEl.id = 'watchlistToast';
      toastEl.style.cssText = 'position:fixed;bottom:24px;left:50%;transform:translateX(-50%);' +
        'background:#12121a;border:1px solid #2a2a3e;border-radius:10px;padding:10px 20px;' +
        'color:#fff;font-size:.85rem;z-index:9999;opacity:0;transition:opacity .3s ease;' +
        'pointer-events:auto;cursor:default;box-shadow:0 8px 24px rgba(0,0,0,.4);';
      document.body.appendChild(toastEl);
    }
    toastEl.textContent = msg;
    toastNavUrl = navUrl || null;
    toastEl.style.cursor = toastNavUrl ? 'pointer' : 'default';
    toastEl.onclick = function() { if (toastNavUrl) window.location.href = toastNavUrl; };
    toastEl.classList.add('show');
    toastEl.style.opacity = '1';
    clearTimeout(toastTimer);
    toastTimer = setTimeout(function() {
      toastEl.classList.remove('show');
      toastEl.style.opacity = '0';
    }, 3500);
  }

  // === Normalization (new + legacy shapes) ===

  // Legacy entries may be plain strings ("NVDA") or {ticker, ...} objects.
  function normTicker(t) {
    if (typeof t === 'string') return { ticker: t, addedAt: null };
    if (t && typeof t.ticker === 'string') {
      return { ticker: t.ticker, addedAt: t.addedAt || null };
    }
    return null;
  }

  function normalizeLists(data) {
    if (!data) return [];
    if (Array.isArray(data.watchlists)) {
      return data.watchlists.map(function(w) {
        var tickers = (Array.isArray(w.tickers) ? w.tickers : [])
          .map(normTicker).filter(function(t) { return !!t; });
        return {
          id: w.id != null ? w.id : null,
          name: w.name || 'Watchlist',
          tickers: tickers,
          createdAt: w.createdAt || null
        };
      });
    }
    if (Array.isArray(data.watchlist)) {
      var tickers = data.watchlist.map(normTicker).filter(function(t) { return !!t; });
      return [{ id: null, name: 'My Watchlist', tickers: tickers, createdAt: null }];
    }
    return [];
  }

  // === API calls ===

  function apiWatchlist(op, payload) {
    var token = getToken();
    if (op === 'list') {
      return fetch(API_BASE + '?action=watchlist&op=list&token=' + encodeURIComponent(token || ''))
        .then(function(r) {
          return r.json().then(function(d) { return { status: r.status, data: d }; });
        });
    }
    var body = payload || {};
    body.token = token;
    return fetch(API_BASE + '?action=watchlist&op=' + encodeURIComponent(op), {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body)
    }).then(function(r) {
      return r.json().then(function(d) { return { status: r.status, data: d }; });
    });
  }

  function apiError(res, fallback) {
    var err = new Error((res.data && res.data.error) || fallback);
    err.code = res.status;
    return err;
  }

  function fetchWatchlists() {
    return apiWatchlist('list').then(function(res) {
      if (res.status !== 200) throw apiError(res, 'Failed to load watchlists');
      state.watchlists = normalizeLists(res.data);
      state.loaded = true;
      return state.watchlists;
    });
  }

  // Mutations return the full watchlists array (new API) or a single
  // watchlist (legacy). If neither, refetch.
  function mutate(op, payload) {
    return apiWatchlist(op, payload).then(function(res) {
      if (res.status === 403) {
        state.premium = false;
        throw apiError(res, 'Premium membership required');
      }
      if (res.status !== 200) throw apiError(res, 'Request failed');
      var lists = null;
      if (res.data && Array.isArray(res.data.watchlists)) lists = normalizeLists(res.data);
      else if (res.data && res.data.watchlist) lists = normalizeLists(res.data);
      if (lists) {
        state.watchlists = lists;
        state.loaded = true;
        return state.watchlists;
      }
      return fetchWatchlists();
    });
  }

  function checkPremium() {
    var token = getToken();
    return fetch(API_BASE + '?action=premium&token=' + encodeURIComponent(token || ''))
      .then(function(r) { return r.json(); })
      .then(function(d) {
        state.premium = !!(d && d.premium);
        // checkPremium() can resolve AFTER renderPage() has already painted
        // the overview — refresh gating now so a non-premium user actually
        // sees the upgrade CTA instead of waiting for a failed mutation.
        updateGating();
        return state.premium;
      })
      .catch(function() {
        // Optimistic — keep the UI usable; real 403s from mutations will
        // surface the upgrade CTA.
        state.premium = true;
        return true;
      });
  }

  function fetchPrices() {
    return fetch(PRICES_URL)
      .then(function(r) { return r.ok ? r.json() : null; })
      .then(function(data) {
        var px = (data && data.prices) || data || {};
        var got = false;
        Object.keys(px).forEach(function(k) {
          var p = px[k];
          if (p && typeof p === 'object' && p.price != null) {
            state.prices[k.toUpperCase()] = {
              price: p.price,
              changePercent: p.changePercent != null ? p.changePercent : null,
              change: p.change != null ? p.change : null
            };
            got = true;
          }
        });
        return got ? state.prices : null;
      })
      .catch(function() { return null; });
  }

  function fetchStockIndex() {
    if (Object.keys(state.index).length) return Promise.resolve(state.index);
    return fetch(INDEX_URL)
      .then(function(r) { return r.ok ? r.json() : null; })
      .then(function(data) {
        var stocks = (data && data.stocks) || [];
        var map = {};
        stocks.forEach(function(s) {
          if (s && s.ticker) {
            map[s.ticker.toUpperCase()] = { name: s.name || s.ticker, sector: s.sector || 'Other' };
          }
        });
        state.index = map;
        return map;
      })
      .catch(function() { return state.index; });
  }

  // === Lookups ===

  function findList(id) {
    if (id == null) return null;
    for (var i = 0; i < state.watchlists.length; i++) {
      if (String(state.watchlists[i].id) === String(id)) return state.watchlists[i];
    }
    return null;
  }

  function findListWithTicker(ticker) {
    for (var i = 0; i < state.watchlists.length; i++) {
      var wl = state.watchlists[i];
      for (var j = 0; j < (wl.tickers || []).length; j++) {
        if (wl.tickers[j].ticker === ticker) return wl;
      }
    }
    return null;
  }

  // Equal-weight mean of member changePercent; null when no data.
  function aggregateChange(wl) {
    var vals = [];
    (wl.tickers || []).forEach(function(t) {
      var p = state.prices[t.ticker];
      if (p && p.changePercent != null && !isNaN(p.changePercent)) vals.push(p.changePercent);
    });
    if (!vals.length) return { value: null, dir: '' };
    var mean = vals.reduce(function(a, b) { return a + b; }, 0) / vals.length;
    return { value: mean, dir: mean >= 0 ? ' up' : ' down' };
  }

  // === View switching ===

  function setView(view) {
    document.body.dataset.view = view;
    var overview = document.getElementById('wl-overview');
    var detail = document.getElementById('wl-detail');
    if (overview) overview.style.display = (view === 'overview') ? '' : 'none';
    if (detail) detail.style.display = (view === 'detail') ? '' : 'none';
  }

  function updateGating() {
    var user = getUser();
    var upgrade = document.getElementById('wl-upgrade');
    var createCard = document.getElementById('wl-create-card');
    var notPremium = user && state.premium === false;
    if (upgrade) upgrade.style.display = notPremium ? '' : 'none';
    if (createCard) {
      createCard.style.display = (user && state.loaded && state.premium !== false &&
        state.watchlists.length < MAX_LISTS) ? '' : 'none';
    }
  }

  // === Overview ===

  function signInHtml() {
    return '<div class="wl-login-prompt" style="text-align:center;padding:4rem 2rem;">' +
      '<div style="font-size:3rem;margin-bottom:1rem;">🐝</div>' +
      '<h2 style="font-family:\'Oxanium\',sans-serif;font-size:1.3rem;color:#fff;margin:0 0 .5rem;">Sign in to use Watchlists</h2>' +
      '<p style="color:#94a3b8;margin:0 0 2rem;">Track your favorite stocks across multiple portfolios.</p>' +
      '<button class="hive-cta-btn" onclick="_wlSignIn()">Sign In</button>' +
      '</div>';
  }

  function emptyOverviewHtml() {
    return '<div class="wl-empty" style="text-align:center;padding:4rem 2rem;">' +
      '<div style="font-size:3rem;margin-bottom:1rem;">📋</div>' +
      '<h2 style="font-family:\'Oxanium\',sans-serif;font-size:1.2rem;color:#fff;margin:0 0 .4rem;">No Watchlists Yet</h2>' +
      '<p style="color:#94a3b8;margin:0 0 .3rem;">Create your first portfolio to group the stocks you track.</p>' +
      '<p style="color:#5e7092;font-size:.82rem;margin:0 0 2rem;">Click the ☆ icon on any stock page to add it.</p>' +
      '<a href="/stocks/" class="premium-cta-btn" style="display:inline-block;padding:12px 28px;background:linear-gradient(135deg,#6366f1,#818cf8);border:none;border-radius:10px;color:#fff;font-family:\'Oxanium\',sans-serif;font-size:.9rem;font-weight:700;cursor:pointer;text-decoration:none;">Browse Stocks</a>' +
      '</div>';
  }

  function errorHtml() {
    return '<div class="wl-error" style="text-align:center;padding:3rem;color:#ef4444;">' +
      'Failed to load watchlists. Please try again.' +
      '</div>';
  }

  // Total badge in the hero: "N symbols · M lists" across all watchlists
  function fillTotalBadge() {
    var badge = document.getElementById('wl-total-badge');
    if (!badge) return;
    var lists = state.watchlists || [];
    var total = 0;
    for (var i = 0; i < lists.length; i++) total += (lists[i].tickers || []).length;
    var label = total + (total === 1 ? ' symbol' : ' symbols');
    if (lists.length > 0) label += ' · ' + lists.length + (lists.length === 1 ? ' list' : ' lists');
    // Keep the page's decorative dot span if present — only swap the text
    // node after it so Vicky's markup survives the update.
    var dot = badge.querySelector('.wl-total-dot');
    if (dot) {
      while (dot.nextSibling) badge.removeChild(dot.nextSibling);
      dot.parentNode.insertBefore(document.createTextNode(' ' + label), dot.nextSibling);
    } else {
      badge.textContent = label;
    }
    badge.style.display = lists.length ? '' : 'none';
  }

  // The create-card button lives INSIDE #wl-overview, so any innerHTML write
  // wipes it — re-append it after every render so updateGating can show/hide it.
  function ensureCreateCard(overview) {
    if (!overview || document.getElementById('wl-create-card')) return;
    var cb = document.createElement('button');
    cb.className = 'wl-create-card';
    cb.id = 'wl-create-card';
    cb.type = 'button';
    cb.innerHTML = '<span class="wl-create-plus">+</span> New Watchlist';
    overview.appendChild(cb);
  }

  function renderOverview() {
    var overview = document.getElementById('wl-overview');
    if (!overview) return;
    fillTotalBadge();
    var user = getUser();
    if (!user || !getToken()) {
      overview.innerHTML = signInHtml();
      updateGating();
      return;
    }
    if (!state.watchlists.length) {
      overview.innerHTML = emptyOverviewHtml();
      ensureCreateCard(overview);
      updateGating();
      return;
    }

    var html = '';
    state.watchlists.forEach(function(wl) {
      var agg = aggregateChange(wl);
      html += '<div class="wl-card" data-wl-id="' + escapeHtml(wl.id) + '" role="button" tabindex="0">' +
        '<span class="wl-card-star">★</span>' +
        '<div class="wl-card-body">' +
          '<div class="wl-card-name">' + escapeHtml(wl.name) + '</div>' +
          '<div class="wl-card-count">' + wl.tickers.length +
            (wl.tickers.length === 1 ? ' Symbol' : ' Symbols') + '</div>' +
        '</div>' +
        '<div class="wl-card-change' + agg.dir + '">' + fmtPct(agg.value) + '</div>' +
        '<button class="wl-card-edit" aria-label="Edit" title="Rename / delete">✎</button>' +
      '</div>';
    });
    overview.innerHTML = html;
    ensureCreateCard(overview);
    updateGating();
  }

  // === Detail ===

  function openDetail(list) {
    if (!list) return;
    state.currentId = list.id;
    var nameEl = document.getElementById('wl-detail-name');
    var countEl = document.getElementById('wl-detail-count');
    var changeEl = document.getElementById('wl-detail-change');
    if (nameEl) nameEl.textContent = list.name;
    if (countEl) countEl.textContent = list.tickers.length +
      (list.tickers.length === 1 ? ' Symbol' : ' Symbols');
    var agg = aggregateChange(list);
    if (changeEl) {
      changeEl.textContent = fmtPct(agg.value);
      changeEl.className = changeEl.className
        .replace(/\bup\b|\bdown\b|\bpositive\b|\bnegative\b/g, '').trim() +
        (agg.dir ? ' ' + agg.dir.trim() : '');
    }
    renderStockRows(list);
    setView('detail');
  }

  function renderStockRows(list) {
    var listEl = document.getElementById('wl-stock-list');
    if (!listEl) return;

    var rows = (list.tickers || []).slice();
    rows.sort(function(a, b) { return compareRows(a, b, state.sort); });

    if (!rows.length) {
      listEl.innerHTML = '<div class="wl-stock-empty" style="text-align:center;padding:3rem 1rem;color:#94a3b8;">' +
        '<div style="font-size:2.5rem;margin-bottom:.5rem;">📋</div>' +
        '<div>No symbols yet — add one above or tap ☆ on any stock page.</div>' +
        '</div>';
      return;
    }

    var html = '';
    rows.forEach(function(t) {
      var ticker = t.ticker;
      var p = state.prices[ticker] || {};
      var info = state.index[ticker] || {};
      var pct = p.changePercent;
      html += '<div class="wl-stock-row" data-ticker="' + escapeHtml(ticker) + '" role="button" tabindex="0">' +
        '<span class="wl-stock-ticker">$' + escapeHtml(ticker) + '</span>' +
        '<span class="wl-stock-name">' + escapeHtml(info.name || ticker) + '</span>' +
        '<span class="wl-stock-price">' + fmtPrice(p.price) + '</span>' +
        '<span class="wl-stock-change' +
          (pct != null ? (pct >= 0 ? ' up positive' : ' down negative') : '') + '">' +
          fmtPct(pct) + '</span>' +
        '<button class="wl-stock-remove" aria-label="Remove" title="Remove ' + escapeHtml(ticker) + '">×</button>' +
      '</div>';
    });
    listEl.innerHTML = html;
  }

  // === Sorting ===
  //
  // Canonical sort keys. The page ships a static <select id="wl-sort"> whose
  // option values historically DON'T match these keys ('ticker' instead of
  // 'symbol', 'price-desc' instead of 'price', 'change-desc'/'change-asc'
  // instead of 'gainers'/'losers', and no 'recent' at all). normalizeSortValue
  // maps any markup variant onto a canonical key, and ensureSortOptions
  // rewrites the live <select> so every option actually sorts. Without this,
  // every non-'name' mode fell through the switch to the default (symbol)
  // sort — the user-reported "Sort by doesn't work".
  var SORT_MODES = [
    ['symbol', 'Symbol (A–Z)'],
    ['name', 'Name (A–Z)'],
    ['price', 'Price (high → low)'],
    ['price-asc', 'Price (low → high)'],
    ['gainers', 'Top Gainers'],
    ['losers', 'Top Losers'],
    ['recent', 'Recently Added']
  ];

  function normalizeSortValue(v) {
    switch (v) {
      case 'ticker': return 'symbol';
      case 'price-desc': return 'price';
      case 'price-asc': return 'price-asc';
      case 'change-desc': return 'gainers';
      case 'change-asc': return 'losers';
      case 'symbol': case 'name': case 'price': case 'gainers':
      case 'losers': case 'recent': return v;
      default: return 'symbol';
    }
  }

  // Remap whatever option values the markup ships onto canonical keys
  // (preserving the page's labels), then append any modes that are missing
  // (e.g. 'recent' on the current production page). Idempotent.
  function ensureSortOptions(sort) {
    var present = {};
    Array.prototype.forEach.call(sort.options, function(opt) {
      var canon = normalizeSortValue(opt.value);
      opt.value = canon;
      present[canon] = true;
    });
    SORT_MODES.forEach(function(m) {
      if (!present[m[0]]) {
        var opt = document.createElement('option');
        opt.value = m[0];
        opt.textContent = m[1];
        sort.appendChild(opt);
      }
    });
  }

  function compareRows(a, b, key) {
    key = normalizeSortValue(key);
    var pa = state.prices[a.ticker] || {};
    var pb = state.prices[b.ticker] || {};
    var ia = state.index[a.ticker] || {};
    var ib = state.index[b.ticker] || {};
    var va, vb;
    switch (key) {
      case 'name':
        va = (ia.name || a.ticker).toLowerCase();
        vb = (ib.name || b.ticker).toLowerCase();
        return va < vb ? -1 : va > vb ? 1 : 0;
      case 'price':
        va = (pa.price != null ? pa.price : -Infinity);
        vb = (pb.price != null ? pb.price : -Infinity);
        return vb - va;
      case 'price-asc':
        va = (pa.price != null ? pa.price : Infinity);
        vb = (pb.price != null ? pb.price : Infinity);
        return va - vb;
      case 'gainers':
        va = (pa.changePercent != null ? pa.changePercent : -Infinity);
        vb = (pb.changePercent != null ? pb.changePercent : -Infinity);
        return vb - va;
      case 'losers':
        va = (pa.changePercent != null ? pa.changePercent : Infinity);
        vb = (pb.changePercent != null ? pb.changePercent : Infinity);
        return va - vb;
      case 'recent':
        va = a.addedAt || '';
        vb = b.addedAt || '';
        if (va === vb) return 0;
        if (!va) return 1;   // no date -> bottom
        if (!vb) return -1;
        return va < vb ? 1 : -1;  // newest first
      default: // symbol
        va = a.ticker.toUpperCase();
        vb = b.ticker.toUpperCase();
        return va < vb ? -1 : va > vb ? 1 : 0;
    }
  }

  // === Add / remove ===

  function handleAddTicker() {
    var wrap = document.getElementById('wl-add-search');
    var input = null;
    if (wrap) {
      input = wrap.querySelector('input[type="text"], input:not([type])');
      if (!input && wrap.tagName === 'INPUT') input = wrap;
    } else {
      input = document.getElementById('wl-add-search-input');
    }
    if (!input) return;
    var raw = (input.value || '').trim().toUpperCase();
    if (!TICKER_RE.test(raw)) {
      showToast('Enter a valid ticker (1–10 characters)');
      return;
    }
    var list = findList(state.currentId);
    if (!list) return;
    for (var i = 0; i < list.tickers.length; i++) {
      if (list.tickers[i].ticker === raw) {
        showToast(raw + ' is already in this watchlist');
        return;
      }
    }
    input.value = '';
    input.focus();
    var listName = list.name;
    mutate('add', { id: list.id, ticker: raw })
      .then(function() {
        showToast(raw + ' added to ' + listName);
        return refreshAfterMutation();
      })
      .catch(handleMutationError);
  }

  function handleRemoveTicker(ticker) {
    var list = findList(state.currentId);
    if (!list) return;
    var listName = list.name;
    mutate('remove', { id: list.id, ticker: ticker })
      .then(function() {
        showToast(ticker + ' removed from ' + listName);
        return refreshAfterMutation();
      })
      .catch(handleMutationError);
  }

  function refreshAfterMutation() {
    return fetchPrices().then(function() {
      var list = findList(state.currentId);
      if (state.currentId != null && list) openDetail(list);
      renderOverview();
      updateGating();
    });
  }

  function handleMutationError(err) {
    if (err && err.code === 403) {
      state.premium = false;
      updateGating();
      renderOverview();
      showToast('This is a Premium feature — upgrade to continue', '/pricing');
    } else if (err && err.code === 401) {
      showToast('Please sign in again');
    } else {
      showToast((err && err.message) || 'Something went wrong — please try again');
    }
  }

  // === Add-ticker autocomplete ===

  var suggestActiveIndex = -1;

  function getAddInput() {
    var wrap = document.getElementById('wl-add-search');
    var input = null;
    if (wrap) {
      input = wrap.querySelector('input[type="text"], input:not([type])');
      if (!input && wrap.tagName === 'INPUT') input = wrap;
    } else {
      input = document.getElementById('wl-add-search-input');
    }
    return input;
  }

  function hideSuggestDropdown() {
    var box = document.getElementById('wl-add-suggest');
    if (box && box.parentNode) box.parentNode.removeChild(box);
    suggestActiveIndex = -1;
  }

  // Prefix match on ticker OR substring match on company name, capped at 8.
  function suggestMatches(q) {
    var qUp = q.toUpperCase();
    var out = [];
    var keys = Object.keys(state.index);
    for (var i = 0; i < keys.length && out.length < 8; i++) {
      var k = keys[i];
      var info = state.index[k];
      if (!info) continue;
      var name = String(info.name || '');
      if (k.indexOf(qUp) === 0 || name.toUpperCase().indexOf(qUp) !== -1) {
        out.push({ ticker: k, name: name, sector: String(info.sector || 'Other') });
      }
    }
    return out;
  }

  function renderSuggestDropdown(input) {
    var wrap = document.getElementById('wl-add-search');
    if (!wrap || !input) return;
    var q = (input.value || '').trim();
    hideSuggestDropdown(); // removes the old box; also fires when input is cleared
    if (!q) return;
    if (window.getComputedStyle(wrap).position === 'static') {
      wrap.style.position = 'relative'; // anchor point for the absolute dropdown
    }
    var matches = suggestMatches(q);
    var box = document.createElement('div');
    box.id = 'wl-add-suggest';
    box.className = 'wl-add-suggest';
    box.style.cssText = 'position:absolute;top:100%;left:0;right:0;z-index:50;' +
      'background:#12121a;border:1px solid #2a2a3e;border-radius:8px;margin-top:4px;' +
      'max-height:320px;overflow-y:auto;';
    if (!matches.length) {
      var empty = document.createElement('div');
      empty.className = 'wl-add-suggest-empty';
      empty.textContent = 'No matches';
      empty.style.cssText = 'padding:10px 12px;color:#64748b;font-size:.85rem;cursor:default;';
      box.appendChild(empty);
    } else {
      for (var i = 0; i < matches.length; i++) {
        (function(m) {
          var row = document.createElement('div');
          row.className = 'wl-add-suggest-item';
          row.setAttribute('data-ticker', m.ticker);
          row.style.cssText = 'display:flex;justify-content:space-between;align-items:center;' +
            'gap:8px;padding:8px 12px;cursor:pointer;font-size:.85rem;color:#cbd5e1;';
          row.innerHTML = '<strong>' + escapeHtml(m.ticker) + '</strong>' +
            '<span style="flex:1;color:#94a3b8;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;">' +
            escapeHtml(m.name) + '</span>' +
            '<span style="color:#64748b;font-size:.75rem;">' + escapeHtml(m.sector) + '</span>';
          row.addEventListener('mousedown', function(e) { e.preventDefault(); });
          row.addEventListener('click', function() { addTickerViaSuggest(m.ticker); });
          box.appendChild(row);
        })(matches[i]);
      }
    }
    wrap.appendChild(box);
  }

  function suggestRows() {
    var box = document.getElementById('wl-add-suggest');
    if (!box) return [];
    return box.querySelectorAll('.wl-add-suggest-item');
  }

  function suggestMove(dir) {
    var rows = suggestRows();
    if (!rows.length) return;
    suggestActiveIndex = (suggestActiveIndex + dir + rows.length) % rows.length;
    for (var i = 0; i < rows.length; i++) {
      rows[i].classList.toggle('active', i === suggestActiveIndex);
      rows[i].style.background = (i === suggestActiveIndex) ? 'rgba(99,102,241,.18)' : '';
    }
    if (rows[suggestActiveIndex] && rows[suggestActiveIndex].scrollIntoView) {
      rows[suggestActiveIndex].scrollIntoView({ block: 'nearest' });
    }
  }

  function suggestActiveTicker() {
    var rows = suggestRows();
    if (suggestActiveIndex < 0 || suggestActiveIndex >= rows.length) return null;
    return rows[suggestActiveIndex].getAttribute('data-ticker');
  }

  // Reuses handleAddTicker()'s exact add path: it reads the input, validates,
  // calls mutate('add', {id: state.currentId, ticker}), clears the input, and
  // refreshes prices + detail list + overview.
  function addTickerViaSuggest(ticker) {
    var input = getAddInput();
    if (!input) return;
    input.value = ticker;
    hideSuggestDropdown();
    handleAddTicker();
  }

  // === Modal (create / rename / delete) ===

  var modalState = { mode: null, listId: null, armed: false };

  function getModal() {
    var wrap = document.getElementById('wl-modal');
    var confirmBtn = document.getElementById('wl-modal-confirm');
    var cancelBtn = document.getElementById('wl-modal-cancel');
    if (!wrap || !confirmBtn || !cancelBtn) return null;
    return {
      wrap: wrap,
      title: document.getElementById('wl-modal-title'),
      input: document.getElementById('wl-modal-input'),
      confirm: confirmBtn,
      cancel: cancelBtn
    };
  }

  function showModal(opts) {
    var m = getModal();
    if (!m) return;
    modalState.mode = opts.mode;
    modalState.listId = opts.listId != null ? opts.listId : null;
    modalState.armed = false;
    if (m.title) m.title.textContent = opts.title || '';
    if (m.input) {
      m.input.style.display = (opts.mode === 'delete') ? 'none' : '';
      m.input.value = opts.value || '';
      m.input.placeholder = opts.placeholder || '';
    }
    m.confirm.textContent = opts.confirmLabel || 'Confirm';
    m.confirm.className = m.confirm.className.replace(/\bwl-modal-danger\b/g, '').trim();
    if (opts.danger) m.confirm.className += ' wl-modal-danger';
    m.wrap.style.display = 'flex';
    if (m.wrap.classList) m.wrap.classList.add('open');
    if (m.input && opts.mode !== 'delete') {
      setTimeout(function() { m.input.focus(); }, 50);
    }
  }

  function hideModal() {
    var m = getModal();
    if (!m) return;
    m.wrap.style.display = 'none';
    if (m.wrap.classList) m.wrap.classList.remove('open');
    modalState.mode = null;
    modalState.listId = null;
    modalState.armed = false;
    // A star-picker "new watchlist" request is void once the modal closes
    // without confirming (cancel / backdrop / Escape) — no phantom adds later.
    pendingStarAdd = null;
  }

  // The delete action lives inside the rename modal. Vicky may ship a static
  // button (.wl-modal-delete); if not, we create one (JS-owned modal content).
  function ensureModalDeleteBtn(m) {
    var btn = m.wrap.querySelector('.wl-modal-delete, #wl-modal-delete');
    if (!btn) {
      btn = document.createElement('button');
      btn.className = 'wl-modal-delete';
      btn.type = 'button';
      btn.textContent = 'Delete';
      btn.setAttribute('aria-label', 'Delete watchlist');
      m.cancel.parentNode.insertBefore(btn, m.cancel.nextSibling);
    }
    return btn;
  }

  function onModalConfirm() {
    var m = getModal();
    if (!m || !modalState.mode) return;

    if (modalState.mode === 'delete') {
      // Two-step: first click arms the destructive confirm.
      if (!modalState.armed) {
        modalState.armed = true;
        if (m.title) m.title.textContent = 'Delete this watchlist?';
        if (m.input) m.input.style.display = 'none';
        m.confirm.textContent = 'Yes, Delete';
        m.confirm.className = m.confirm.className.replace(/\bwl-modal-danger\b/g, '').trim() + ' wl-modal-danger';
        return;
      }
      var delId = modalState.listId;
      hideModal();
      mutate('delete', { id: delId })
        .then(function() {
          showToast('Watchlist deleted');
          state.currentId = null;
          setView('overview');
          renderOverview();
          updateGating();
        })
        .catch(handleMutationError);
      return;
    }

    var name = m.input ? m.input.value.trim() : '';
    if (!name) { showToast('Please enter a name'); return; }
    if (name.length > 60) { showToast('Name is too long (60 characters max)'); return; }

    if (modalState.mode === 'create') {
      var starPending = pendingStarAdd;
      var idsBefore = null;
      if (starPending) {
        idsBefore = {};
        state.watchlists.forEach(function(w) { idsBefore[String(w.id)] = true; });
      }
      hideModal();
      mutate('create', { name: name })
        .then(function() {
          showToast('Watchlist "' + name + '" created');
          renderOverview();
          updateGating();
          if (starPending) {
            // Star-picker flow: add the ticker to the freshly created list.
            pendingStarAdd = null;
            var created = findNewList(idsBefore);
            closeStarPicker();
            if (created) starPickAdd(starPending.ticker, starPending.heart, created.id);
          }
        })
        .catch(function(err) {
          hideModal();
          handleMutationError(err);
          renderOverview();
        });
    } else if (modalState.mode === 'rename') {
      var renameId = modalState.listId;
      hideModal();
      mutate('rename', { id: renameId, name: name })
        .then(function() {
          showToast('Watchlist renamed');
          var list = findList(renameId);
          if (state.currentId != null && state.currentId === renameId && list) {
            openDetail(list);
          } else {
            renderOverview();
          }
          updateGating();
        })
        .catch(handleMutationError);
    }
  }

  function onModalDeleteBtn() {
    if (modalState.mode !== 'rename') return;
    var m = getModal();
    if (!m) return;
    // Switch the rename modal into delete-confirm mode.
    modalState.mode = 'delete';
    modalState.armed = false;
    if (m.title) m.title.textContent = 'Delete this watchlist?';
    if (m.input) m.input.style.display = 'none';
    m.confirm.textContent = 'Delete';
    m.confirm.className = m.confirm.className.replace(/\bwl-modal-danger\b/g, '').trim() + ' wl-modal-danger';
  }

  // === Page renderer ===

  function renderPage() {
    var overview = document.getElementById('wl-overview');
    if (!overview) return; // not the watchlist page (e.g. stock pages)

    var user = getUser();
    if (!user || !getToken()) {
      overview.innerHTML = signInHtml();
      setView('overview');
      updateGating();
      return;
    }

    overview.innerHTML = '<div class="wl-loading" style="text-align:center;padding:2.5rem;color:#94a3b8;">' +
      '<div class="hive-spinner" style="width:32px;height:32px;border:3px solid rgba(255,255,255,.1);border-top-color:#6366f1;border-radius:50%;animation:wlspin .6s linear infinite;margin:0 auto 1rem;"></div>' +
      '<span>Loading your portfolios…</span>' +
      '<style>@keyframes wlspin{to{transform:rotate(360deg)}}</style>' +
      '</div>';
    setView('overview');
    updateGating();

    Promise.all([fetchWatchlists(), fetchStockIndex()])
      .then(function() { return fetchPrices(); })
      .then(function() {
        renderOverview();
        var list = findList(state.currentId);
        if (state.currentId != null && list) openDetail(list);
      })
      .catch(function(err) {
        if (err && err.code === 401) {
          overview.innerHTML = signInHtml();
        } else if (state.watchlists.length) {
          renderOverview(); // keep last good state
          showToast('Network error — showing last saved data');
        } else {
          overview.innerHTML = errorHtml();
        }
        updateGating();
      });
  }

  // === Event bindings ===

  function bindEvents() {
    var back = document.getElementById('wl-back');
    if (back) {
      back.addEventListener('click', function() {
        state.currentId = null;
        setView('overview');
        renderOverview();
      });
    }

    var sort = document.getElementById('wl-sort');
    if (sort) {
      // The page may ship a static <select> whose option values don't match
      // our canonical sort keys ('ticker' vs 'symbol', 'price-desc' vs
      // 'price', 'change-desc'/'change-asc' vs 'gainers'/'losers', and no
      // 'recent'). Normalize whatever is there, append any missing modes,
      // and force the select to reflect state.sort so the visible option and
      // the actual sort never drift apart.
      state.sort = normalizeSortValue(state.sort);
      ensureSortOptions(sort);
      sort.value = state.sort;
      sort.addEventListener('change', function() {
        state.sort = normalizeSortValue(sort.value);
        var list = findList(state.currentId);
        if (list) renderStockRows(list);
      });
    }

    var overview = document.getElementById('wl-overview');
    if (overview) {
      overview.addEventListener('click', function(e) {
        var createBtn = e.target.closest('.wl-create-card');
        if (createBtn) {
          if (!getUser() || !getToken()) { showHiveJoin('login'); return; }
          if (state.premium === false) { showToast('This is a Premium feature', '/pricing'); return; }
          if (!state.loaded || state.watchlists.length >= MAX_LISTS) return;
          showModal({
            mode: 'create',
            title: 'New Watchlist',
            placeholder: 'Name your watchlist (e.g. AI Picks)',
            confirmLabel: 'Create'
          });
          return;
        }
        var editBtn = e.target.closest('.wl-card-edit');
        if (editBtn) {
          e.stopPropagation();
          var card = editBtn.closest('.wl-card');
          var id = card && card.getAttribute('data-wl-id');
          var list = id != null ? findList(id) : null;
          if (!list) return;
          if (state.premium === false) {
            showToast('This is a Premium feature', '/pricing');
            return;
          }
          ensureModalDeleteBtn(getModal() || { wrap: document.getElementById('wl-modal'), cancel: document.getElementById('wl-modal-cancel') });
          showModal({
            mode: 'rename',
            title: 'Rename Watchlist',
            value: list.name,
            confirmLabel: 'Rename',
            listId: list.id
          });
          return;
        }
        var wlCard = e.target.closest('.wl-card');
        if (wlCard) {
          var wlId = wlCard.getAttribute('data-wl-id');
          var wlList = wlId != null ? findList(wlId) : null;
          if (wlList) openDetail(wlList);
        }
      });
      overview.addEventListener('keydown', function(e) {
        if (e.key !== 'Enter') return;
        var wlCard = e.target.closest('.wl-card');
        if (!wlCard || e.target.closest('.wl-card-edit')) return;
        var wlId = wlCard.getAttribute('data-wl-id');
        var wlList = wlId != null ? findList(wlId) : null;
        if (wlList) openDetail(wlList);
      });
    }

    var stockList = document.getElementById('wl-stock-list');
    if (stockList) {
      stockList.addEventListener('click', function(e) {
        var row = e.target.closest('.wl-stock-row');
        if (!row) return;
        var ticker = row.getAttribute('data-ticker');
        if (!ticker) return;
        if (e.target.closest('.wl-stock-remove')) {
          e.stopPropagation();
          handleRemoveTicker(ticker);
          return;
        }
        window.location.href = '/stocks/' + encodeURIComponent(ticker) + '/';
      });
    }

    var addWrap = document.getElementById('wl-add-search');
    var addInput = null;
    if (addWrap) {
      addInput = addWrap.querySelector('input[type="text"], input:not([type])');
      if (!addInput && addWrap.tagName === 'INPUT') addInput = addWrap;
    } else {
      addInput = document.getElementById('wl-add-search-input');
    }
    var addBtn = addWrap ? addWrap.querySelector('button') : null;
    if (!addBtn) addBtn = document.getElementById('wl-add-search-btn');
    if (addBtn) addBtn.addEventListener('click', handleAddTicker);
    if (addInput) {
      addInput.maxLength = 10; // backend allows 10 chars (e.g. BRK.B); HTML maxlength="5" must not truncate
      addInput.addEventListener('input', function() { renderSuggestDropdown(addInput); });
      addInput.addEventListener('keydown', function(e) {
        if (e.key === 'Enter') {
          e.preventDefault();
          var active = suggestActiveTicker();
          if (active) addInput.value = active;
          hideSuggestDropdown();
          handleAddTicker();
          return;
        }
        if (e.key === 'ArrowDown') { e.preventDefault(); suggestMove(1); return; }
        if (e.key === 'ArrowUp') { e.preventDefault(); suggestMove(-1); return; }
        if (e.key === 'Escape') { hideSuggestDropdown(); return; }
      });
      addInput.addEventListener('blur', function() {
        setTimeout(hideSuggestDropdown, 150); // delay so row clicks still register
      });
    }

    var confirmBtn = document.getElementById('wl-modal-confirm');
    var cancelBtn = document.getElementById('wl-modal-cancel');
    var modalWrap = document.getElementById('wl-modal');
    modalButtonsBound = true; // shared wiring already done here
    if (confirmBtn) confirmBtn.addEventListener('click', onModalConfirm);
    if (cancelBtn) cancelBtn.addEventListener('click', hideModal);
    if (modalWrap) {
      modalWrap.addEventListener('click', function(e) {
        if (e.target === modalWrap) { hideModal(); return; } // backdrop click
        var del = e.target.closest('.wl-modal-delete, #wl-modal-delete');
        if (del) { e.stopPropagation(); onModalDeleteBtn(); }
      });
      var modalInput = document.getElementById('wl-modal-input');
      if (modalInput) {
        modalInput.addEventListener('keydown', function(e) {
          if (e.key === 'Enter') { e.preventDefault(); onModalConfirm(); }
        });
      }
    }
    document.addEventListener('keydown', function(e) {
      if (e.key === 'Escape') hideModal();
    });
  }

  // === Stock-page hearts (multi-watchlist aware) ===

  function createHeartIcon(ticker, isWatched, container) {
    var heart = document.createElement('span');
    heart.className = 'watchlist-heart' + (isWatched ? ' watched' : '');
    heart.setAttribute('data-ticker', ticker);
    heart.innerHTML = isWatched ? '★' : '☆';
    heart.title = isWatched ? 'Remove from watchlist' : 'Add to watchlist';
    heart.style.cssText = 'cursor:pointer;font-size:1.3rem;line-height:1;display:inline-flex;align-items:center;justify-content:center;width:36px;height:36px;border-radius:50%;transition:all .2s;color:' + (isWatched ? '#fbbf24' : '#94a3b8') + ';background:' + (isWatched ? 'rgba(251,191,36,.15)' : 'rgba(255,255,255,.05)') + ';';

    heart.addEventListener('click', function(e) {
      e.stopPropagation();
      e.preventDefault();
      var user = getUser();
      if (!user || !getToken()) { showHiveJoin('login'); return; }

      var currentlyWatched = heart.classList.contains('watched');
      if (currentlyWatched) {
        var holder = findListWithTicker(ticker);
        if (!holder) { setHeart(heart, false); return; }
        mutate('remove', { id: holder.id, ticker: ticker })
          .then(function() {
            setHeart(heart, false);
            window.dispatchEvent(new CustomEvent('watchlist-changed', {
              detail: { ticker: ticker, action: 'removed' }
            }));
          })
          .catch(handleMutationError);
        return;
      }

      // Not watched: add directly when there's a single watchlist, open the
      // star picker to choose a target when there are several, or point the
      // user at /watchlist when none exist.
      ensureListsForHeart().then(function(lists) {
        if (!lists || !lists.length) {
          showToast('No watchlists yet — create one on the Watchlist page', '/watchlist');
          return;
        }
        if (lists.length === 1) {
          var first = lists[0];
          mutate('add', { id: first.id, ticker: ticker })
            .then(function() {
              setHeart(heart, true);
              window.dispatchEvent(new CustomEvent('watchlist-changed', {
                detail: { ticker: ticker, action: 'added' }
              }));
            })
            .catch(handleMutationError);
          return;
        }
        openStarPicker(lists, ticker, heart);
      });
    });

    if (container) container.appendChild(heart);
    return heart;
  }

  function setHeart(heart, watched) {
    heart.classList.toggle('watched', watched);
    heart.innerHTML = watched ? '★' : '☆';
    heart.title = watched ? 'Remove from watchlist' : 'Add to watchlist';
    heart.style.color = watched ? '#fbbf24' : '#94a3b8';
    heart.style.background = watched ? 'rgba(251,191,36,.15)' : 'rgba(255,255,255,.05)';
  }

  function ensureListsForHeart() {
    if (state.watchlists.length) return Promise.resolve(state.watchlists);
    return fetchWatchlists().catch(function() { return []; });
  }

  // === Star picker (choose target watchlist when starring) ===

  var pendingStarAdd = null; // {ticker, heart} waiting on the create-modal flow
  var starEscapeHandler = null;
  var modalButtonsBound = false; // shared #wl-modal wiring guard (watchlist + stock pages)

  function closeStarPicker() {
    var existing = document.querySelector('.wl-star-picker-backdrop');
    if (existing && existing.parentNode) existing.parentNode.removeChild(existing);
    if (starEscapeHandler) {
      document.removeEventListener('keydown', starEscapeHandler);
      starEscapeHandler = null;
    }
  }

  function starPickAdd(ticker, heart, listId) {
    closeStarPicker();
    mutate('add', { id: listId, ticker: ticker })
      .then(function() {
        setHeart(heart, true);
        window.dispatchEvent(new CustomEvent('watchlist-changed', {
          detail: { ticker: ticker, action: 'added' }
        }));
      })
      .catch(handleMutationError);
  }

  // After mutate('create') resolves, find the list that did not exist before.
  function findNewList(idsBefore) {
    for (var i = 0; i < state.watchlists.length; i++) {
      if (!idsBefore[String(state.watchlists[i].id)]) return state.watchlists[i];
    }
    return state.watchlists.length ? state.watchlists[state.watchlists.length - 1] : null;
  }

  function openStarPicker(lists, ticker, heart) {
    closeStarPicker(); // only one picker open at a time

    var backdrop = document.createElement('div');
    backdrop.className = 'wl-star-picker-backdrop';
    backdrop.style.cssText = 'position:fixed;inset:0;z-index:9000;display:flex;' +
      'align-items:center;justify-content:center;background:rgba(8,12,24,.6);';

    var panel = document.createElement('div');
    panel.className = 'wl-star-picker';
    panel.style.cssText = 'background:#12121a;border:1px solid #2a2a3e;border-radius:12px;' +
      'padding:14px;width:320px;max-width:calc(100vw - 40px);max-height:70vh;overflow-y:auto;' +
      'box-shadow:0 16px 48px rgba(0,0,0,.5);';

    var title = document.createElement('div');
    title.className = 'wl-star-picker-title';
    title.textContent = 'Add to watchlist';
    title.style.cssText = 'font-family:\'Oxanium\',sans-serif;font-size:1rem;font-weight:700;' +
      'color:#fff;margin:0 0 10px;';
    panel.appendChild(title);

    lists.forEach(function(list) {
      var row = document.createElement('div');
      row.className = 'wl-star-picker-item';
      row.style.cssText = 'display:flex;justify-content:space-between;align-items:center;' +
        'gap:8px;padding:10px 12px;border-radius:8px;cursor:pointer;color:#e2e8f0;font-size:.9rem;';
      row.innerHTML = '<span>' + escapeHtml(list.name || 'Watchlist') + '</span>' +
        '<span style="color:#64748b;font-size:.78rem;">' + (list.tickers ? list.tickers.length : 0) + ' tickers</span>';
      row.addEventListener('mousedown', function(e) { e.preventDefault(); });
      row.addEventListener('click', function() { starPickAdd(ticker, heart, list.id); });
      panel.appendChild(row);
    });

    if (lists.length < MAX_LISTS) {
      var newRow = document.createElement('div');
      newRow.className = 'wl-star-picker-new';
      newRow.textContent = '＋ New watchlist';
      newRow.style.cssText = 'margin-top:8px;padding:10px 12px;border-radius:8px;cursor:pointer;' +
        'color:#818cf8;font-size:.9rem;text-align:center;border:1px dashed #3b3b52;';
      newRow.addEventListener('mousedown', function(e) { e.preventDefault(); });
      newRow.addEventListener('click', function() {
        if (getModal()) {
          // Modal flow (watchlist page): create via the shared modal, then add.
          var modalWrap = document.getElementById('wl-modal');
          if (modalWrap) modalWrap.style.zIndex = '9100'; // keep modal above the picker backdrop (9000)
          pendingStarAdd = { ticker: ticker, heart: heart };
          showModal({
            mode: 'create',
            title: 'New Watchlist',
            placeholder: 'Name your watchlist (e.g. AI Picks)',
            confirmLabel: 'Create'
          });
        } else {
          // Stock pages have no #wl-modal markup — inline create inside the picker.
          starPickerInlineCreate(panel, ticker, heart);
        }
      });
      panel.appendChild(newRow);
    }

    backdrop.addEventListener('click', function(e) {
      if (e.target === backdrop) closeStarPicker(); // backdrop click = no action
    });
    starEscapeHandler = function(e) { if (e.key === 'Escape') closeStarPicker(); };
    document.addEventListener('keydown', starEscapeHandler);

    backdrop.appendChild(panel);
    document.body.appendChild(backdrop);
  }

  // Minimal inline "create watchlist" form used when the page has no #wl-modal
  // markup (stock pages). Mirrors the modal flow: create, then add the ticker.
  function starPickerInlineCreate(panel, ticker, heart) {
    var old = panel.querySelector('.wl-star-picker-new');
    if (old && old.parentNode) old.parentNode.removeChild(old);

    var form = document.createElement('div');
    form.className = 'wl-star-picker-create';
    form.style.cssText = 'margin-top:8px;display:flex;gap:6px;';

    var input = document.createElement('input');
    input.type = 'text';
    input.placeholder = 'Name your watchlist (e.g. AI Picks)';
    input.maxLength = 60;
    input.style.cssText = 'flex:1;min-width:0;padding:8px 10px;background:#0c0c14;' +
      'border:1px solid #2a2a3e;border-radius:8px;color:#fff;font-size:.85rem;outline:none;';

    var btn = document.createElement('button');
    btn.type = 'button';
    btn.textContent = 'Create';
    btn.style.cssText = 'padding:8px 12px;background:linear-gradient(135deg,#6366f1,#818cf8);' +
      'border:none;border-radius:8px;color:#fff;font-weight:700;font-size:.8rem;cursor:pointer;';

    form.appendChild(input);
    form.appendChild(btn);
    panel.appendChild(form);
    input.focus();

    function doCreate() {
      var name = (input.value || '').trim();
      if (!name) { showToast('Please enter a name'); return; }
      if (name.length > 60) { showToast('Name is too long (60 characters max)'); return; }
      var idsBefore = {};
      state.watchlists.forEach(function(w) { idsBefore[String(w.id)] = true; });
      closeStarPicker();
      mutate('create', { name: name })
        .then(function() {
          showToast('Watchlist "' + name + '" created');
          var created = findNewList(idsBefore);
          if (created) starPickAdd(ticker, heart, created.id);
        })
        .catch(handleMutationError);
    }

    btn.addEventListener('click', doCreate);
    input.addEventListener('keydown', function(e) {
      if (e.key === 'Enter') { e.preventDefault(); doCreate(); }
    });
  }

  function initWatchlistHearts() {
    var user = getUser();
    if (!user || !getToken()) return;

    // Stock pages that ship the shared #wl-modal markup need the same
    // confirm/cancel wiring bindEvents() provides on the watchlist page —
    // the star picker's "＋ New watchlist" row drives that modal.
    if (!modalButtonsBound) {
      modalButtonsBound = true;
      var mWrap = document.getElementById('wl-modal');
      var mConfirm = document.getElementById('wl-modal-confirm');
      var mCancel = document.getElementById('wl-modal-cancel');
      var mInput = document.getElementById('wl-modal-input');
      if (mConfirm) mConfirm.addEventListener('click', onModalConfirm);
      if (mCancel) mCancel.addEventListener('click', hideModal);
      if (mWrap) {
        mWrap.addEventListener('click', function(e) {
          if (e.target === mWrap) { hideModal(); return; } // backdrop click
          var del = e.target.closest('.wl-modal-delete, #wl-modal-delete');
          if (del) { e.stopPropagation(); onModalDeleteBtn(); }
        });
        if (mInput) {
          mInput.addEventListener('keydown', function(e) {
            if (e.key === 'Enter') { e.preventDefault(); onModalConfirm(); }
          });
        }
      }
    }

    fetchWatchlists()
      .then(function() { return fetchStockIndex(); })
      .then(function() {
        var watched = {};
        state.watchlists.forEach(function(wl) {
          (wl.tickers || []).forEach(function(t) { watched[t.ticker] = true; });
        });
        renderHearts(watched);
      })
      .catch(function() {
        // Not authenticated or API down — skip hearts.
      });
  }

  function renderHearts(watched) {
    // Explicit containers: <span data-watchlist-ticker="NVDA"></span>
    var containers = document.querySelectorAll('[data-watchlist-ticker]');
    containers.forEach(function(container) {
      var ticker = (container.getAttribute('data-watchlist-ticker') || '').toUpperCase();
      if (ticker) createHeartIcon(ticker, !!watched[ticker], container);
    });

    // Stock-page ticker badge: <div class="stock-ticker-badge">$NVDA · NASDAQ</div>
    var badge = document.querySelector('.stock-ticker-badge');
    if (badge && !badge.querySelector('.watchlist-heart')) {
      var text = badge.textContent.trim();
      var match = text.match(/\$?([A-Z]{1,5})/);
      if (match) {
        var tickerBadge = match[1];
        if (tickerBadge && tickerBadge.length <= 5) {
          var heartWrap = document.createElement('span');
          heartWrap.style.cssText = 'display:inline-flex;align-items:center;margin-left:8px;vertical-align:middle;';
          badge.parentNode.insertBefore(heartWrap, badge.nextSibling);
          createHeartIcon(tickerBadge, !!watched[tickerBadge], heartWrap);
        }
      }
    }

    // Page title fallback: "NVDA — The Signal" on a stock page
    var titleMatch = document.title.match(/^([A-Z]{1,5})\s*(—|-)/);
    if (titleMatch) {
      var titleTicker = titleMatch[1];
      if (document.querySelector('.stock-page, .stock-hero') &&
          !document.querySelector('[data-watchlist-ticker="' + titleTicker + '"]') &&
          !document.querySelector('.watchlist-heart')) {
        var heroLeft = document.querySelector('.stock-hero-left');
        if (heroLeft) createHeartIcon(titleTicker, !!watched[titleTicker], heroLeft);
      }
    }

    // Legacy selectors
    var tickerDisplay = document.querySelector('.stock-title h1, .stock-header .ticker, .stock-ticker-display');
    if (tickerDisplay && !tickerDisplay.querySelector('.watchlist-heart') && !document.querySelector('.watchlist-heart')) {
      var legacyTicker = tickerDisplay.textContent.trim();
      if (legacyTicker && legacyTicker.length <= 5) {
        createHeartIcon(legacyTicker, !!watched[legacyTicker], tickerDisplay);
        tickerDisplay.style.display = 'inline-flex';
        tickerDisplay.style.alignItems = 'center';
        tickerDisplay.style.gap = '8px';
      }
    }
  }

  // === Init ===

  function init() {
    window._wlSignIn = function() { showHiveJoin('login'); };

    if (document.getElementById('wl-overview')) {
      // Watchlist page (Vicky's new DOM). Heart init isn't needed here.
      checkPremium();
      bindEvents();
      renderPage();
    } else {
      // Stock pages etc. — just hearts.
      initWatchlistHearts();
    }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }

  // Re-init when auth changes (token set/cleared in another tab or via auth.js)
  window.addEventListener('storage', function(e) {
    if (e.key === 'hive_user' || e.key === 'hive_token') {
      if (document.getElementById('wl-overview')) {
        checkPremium();
        renderPage();
      } else {
        setTimeout(initWatchlistHearts, 500);
      }
    }
  });

  // Sync when hearts change elsewhere (e.g. another component dispatches)
  window.addEventListener('watchlist-changed', function() {
    if (!document.getElementById('wl-overview')) return;
    fetchWatchlists()
      .then(function() { return fetchPrices(); })
      .then(function() {
        var list = findList(state.currentId);
        if (state.currentId != null && list) openDetail(list);
        renderOverview();
      })
      .catch(function() {});
  });

  // Light live-price refresh while the detail view is open
  setInterval(function() {
    if (!document.getElementById('wl-overview')) return;
    if (document.body.dataset.view !== 'detail') return;
    if (state.currentId == null) return;
    fetchPrices().then(function() {
      var list = findList(state.currentId);
      if (list) openDetail(list);
    });
  }, 60000);

  // === Public API ===

  window.watchlistAPI = {
    get: fetchWatchlists,
    add: function(ticker, id) {
      var list = id != null ? findList(id) : state.watchlists[0];
      if (!list) return Promise.reject(new Error('No watchlist — create one on /watchlist'));
      return mutate('add', { id: list.id, ticker: ticker });
    },
    remove: function(ticker, id) {
      var list = id != null ? findList(id) : findListWithTicker(ticker);
      if (!list) return Promise.resolve();
      return mutate('remove', { id: list.id, ticker: ticker });
    },
    create: function(name) { return mutate('create', { name: name }); },
    rename: function(id, name) { return mutate('rename', { id: id, name: name }); },
    removeList: function(id) { return mutate('delete', { id: id }); },
    render: renderPage,
    initHearts: initWatchlistHearts,
    createHeart: createHeartIcon
  };

})();
