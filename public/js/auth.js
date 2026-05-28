(function() {
  'use strict';

  // Auth system for The Signal — nav sign-in & profile dropdown
  // Integrates with hive.js auth (localStorage tokens) and the Hive API

  var authToggle = document.getElementById('authToggle');
  var authDropdown = document.getElementById('authDropdown');
  var authLabel = document.getElementById('authLabel');
  var authBtnIcon = document.getElementById('authBtnIcon');
  var authBtnImg = document.getElementById('authBtnImg');
  var authBtnInitial = document.getElementById('authBtnInitial');
  var authBtnAvatar = document.getElementById('authBtnAvatar');

  var authProfile = document.getElementById('authProfile');
  var authGuest = document.getElementById('authGuest');
  var authProfileName = document.getElementById('authProfileName');
  var authProfileUsername = document.getElementById('authProfileUsername');
  var authProfileImg = document.getElementById('authProfileImg');
  var authProfileInitial = document.getElementById('authProfileInitial');
  var authStatValue = document.getElementById('authStatValue');
  var authStatReturn = document.getElementById('authStatReturn');
  var authSignOut = document.getElementById('authSignOut');

  if (!authToggle) return;

  var userCache = null;
  var portfolioCache = null;

  // === Utilities ===

  function getHiveToken() {
    try { return localStorage.getItem('hive_token'); } catch(e) { return null; }
  }

  function getHiveUser() {
    try {
      var data = localStorage.getItem('hive_user');
      return data ? JSON.parse(data) : null;
    } catch(e) { return null; }
  }

  function clearHiveSession() {
    try {
      localStorage.removeItem('hive_token');
      localStorage.removeItem('hive_user');
    } catch(e) {}
  }

  // === Button avatar display ===

  function setButtonAvatar(user) {
    if (!authBtnAvatar || !authBtnIcon || !authBtnInitial || !authBtnImg) return;
    if (!user) {
      authBtnAvatar.style.display = 'none';
      authBtnIcon.style.display = '';
      return;
    }
    authBtnAvatar.style.display = '';
    authBtnIcon.style.display = 'none';
    var initial = (user.displayName || user.username || '?').charAt(0).toUpperCase();
    authBtnInitial.textContent = initial;
    if (user.photoURL) {
      authBtnImg.src = user.photoURL;
      authBtnImg.style.display = '';
      authBtnInitial.style.display = 'none';
    } else {
      authBtnImg.style.display = 'none';
      authBtnInitial.style.display = '';
      authBtnInitial.textContent = initial;
    }
  }

  // === Profile dropdown ===

  function updateProfileDropdown(user, portfolio) {
    if (!authProfile || !authGuest) return;

    if (!user) {
      authProfile.style.display = 'none';
      authGuest.style.display = '';
      if (authLabel) authLabel.textContent = 'Sign In';
      setButtonAvatar(null);
      return;
    }

    authProfile.style.display = '';
    authGuest.style.display = 'none';
    if (authLabel) authLabel.textContent = user.displayName || user.username || 'User';
    setButtonAvatar(user);

    // Name and username
    if (authProfileName) authProfileName.textContent = user.displayName || user.username || 'User';
    if (authProfileUsername) authProfileUsername.textContent = '@' + (user.username || user.uid || 'user');

    // Avatar in dropdown
    if (authProfileImg && authProfileInitial) {
      var initial = (user.displayName || user.username || '?').charAt(0).toUpperCase();
      authProfileInitial.textContent = initial;
      if (user.photoURL) {
        authProfileImg.src = user.photoURL;
        authProfileImg.style.display = '';
        authProfileInitial.style.display = 'none';
      } else {
        authProfileImg.style.display = 'none';
        authProfileInitial.style.display = '';
      }
    }

    // Portfolio stats
    if (portfolio && portfolio.cash !== undefined) {
      if (authStatValue) authStatValue.textContent = '$' + (portfolio.totalValue || 0).toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2});
      if (authStatReturn) {
        var ret = portfolio.return || 0;
        authStatReturn.textContent = (ret >= 0 ? '+' : '') + ret + '%';
        authStatReturn.className = 'auth-stat-value' + (ret >= 0 ? ' auth-stat-positive' : ' auth-stat-negative');
      }
    }
  }

  // === Fetch portfolio stats ===

  function fetchPortfolioStats(user) {
    if (!user) return;
    var uid = user.uid;
    var token = getHiveToken();
    var url = '/api/hive?uid=' + encodeURIComponent(uid)
      + '&displayName=' + encodeURIComponent(user.displayName || '')
      + '&photoURL=' + encodeURIComponent(user.photoURL || '');
    if (token) url += '&token=' + encodeURIComponent(token);

    fetch(url)
      .then(function(r) { return r.json(); })
      .then(function(data) {
        portfolioCache = data;
        updateProfileDropdown(user, data);
      })
      .catch(function() {
        // Keep dropdown info without stats
        updateProfileDropdown(user, null);
      });
  }

  // === UI update for current auth state ===

  function updateAuthUI() {
    var user = getHiveUser();
    var token = getHiveToken();
    userCache = user;

    if (user && token) {
      // Verify with server
      fetch('/api/hive?action=me&token=' + encodeURIComponent(token))
        .then(function(r) { return r.json(); })
        .then(function(data) {
          if (data.authenticated) {
            var updatedUser = {
              uid: data.uid,
              username: data.username,
              displayName: data.displayName,
              photoURL: data.photoURL
            };
            try { localStorage.setItem('hive_user', JSON.stringify(updatedUser)); } catch(e) {}
            userCache = updatedUser;
            updateProfileDropdown(updatedUser, null);
            fetchPortfolioStats(updatedUser);
          } else {
            clearHiveSession();
            userCache = null;
            portfolioCache = null;
            updateProfileDropdown(null, null);
          }
        })
        .catch(function() {
          // Server unreachable — use cached data
          updateProfileDropdown(user, portfolioCache);
        });
    } else {
      updateProfileDropdown(null, null);
    }
  }

  // === Dropdown toggle ===

  var isDropdownOpen = false;

  function openDropdown() {
    authDropdown.classList.add('active');
    isDropdownOpen = true;
    // Refresh stats when opening
    var user = getHiveUser();
    if (user) fetchPortfolioStats(user);
  }

  function closeDropdown() {
    authDropdown.classList.remove('active');
    isDropdownOpen = false;
  }

  function toggleDropdown() {
    if (isDropdownOpen) closeDropdown();
    else openDropdown();
  }

  authToggle.addEventListener('click', function(e) {
    e.stopPropagation();
    var user = getHiveUser();
    if (user) {
      toggleDropdown();
    } else {
      if (typeof showHiveJoinModal === 'function') {
        showHiveJoinModal('login');
      } else {
        window.location.href = '/hive';
      }
    }
  });

  // Close dropdown on outside click
  document.addEventListener('click', function(e) {
    if (isDropdownOpen && !e.target.closest('.auth-container')) {
      closeDropdown();
    }
  });

  // Close dropdown on Escape
  document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape' && isDropdownOpen) {
      closeDropdown();
    }
  });

  // === Sign Out ===

  if (authSignOut) {
    authSignOut.addEventListener('click', function() {
      clearHiveSession();
      userCache = null;
      portfolioCache = null;
      updateProfileDropdown(null, null);
      closeDropdown();
      if (typeof loadHomepageHive === 'function') loadHomepageHive();
      if (typeof loadPortfolio === 'function') loadPortfolio();
    });
  }

  // === Navigate to Hive Leaderboard ===

  window.navigateToHiveLeaderboard = function(e) {
    if (e) e.preventDefault();
    closeDropdown();
    // Redirect to /hive — the SPA defaults to Portfolio tab
    // After navigation, we can't programmatically click Leaderboard
    // So we use a sessionStorage hint
    try { sessionStorage.setItem('hive_open_tab', 'leaderboard'); } catch(e2) {}
    window.location.href = '/hive';
  };

  // Check if redirected from leaderboard click
  var pendingTab = null;
  try { pendingTab = sessionStorage.getItem('hive_open_tab'); } catch(e) {}
  if (pendingTab) {
    try { sessionStorage.removeItem('hive_open_tab'); } catch(e) {}
    // The hive.js will handle this via init
  }

  // === Listen for auth changes (cross-tab) ===

  window.addEventListener('storage', function(e) {
    if (e.key === 'hive_user') {
      var newUser = e.newValue ? JSON.parse(e.newValue) : null;
      if (newUser) {
        userCache = newUser;
        updateProfileDropdown(newUser, null);
        fetchPortfolioStats(newUser);
      } else {
        userCache = null;
        portfolioCache = null;
        updateProfileDropdown(null, null);
      }
    }
  });

  // === Initial load ===

  updateAuthUI();

})();
