/**
 * Shared Navigation Component
 * Single source of truth for the site-wide nav (nav bar + drawer + search + auth)
 * Used by build.js, build-stock-page.js, and article builder
 */

function getSharedNav() {
  return `
  <nav class="nav">
    <div class="nav-inner">
      <a href="/" class="logo"><img src="https://pub-4b6ad449790f433c8b0fde9b167147c9.r2.dev/img/logo-hex.jpg" alt="The Signal" class="logo-img"><span class="logo-text"><span class="logo-the">THE</span> <strong>SIGNAL</strong></span></a>
      <div class="nav-actions">
        <button class="nav-btn search-btn" id="searchToggle" aria-label="Search">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <circle cx="11" cy="11" r="8"></circle>
            <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
          </svg>
        </button>
        <div class="auth-container" id="authContainer">
            <button class="nav-btn auth-btn" id="authToggle" aria-label="Sign In">
              <div class="auth-btn-avatar" id="authBtnAvatar">
                <span class="auth-btn-initial" id="authBtnInitial"></span>
                <img class="auth-btn-img" id="authBtnImg" src="" alt="" style="display:none">
              </div>
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="auth-btn-icon" id="authBtnIcon">
                <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path>
                <circle cx="12" cy="7" r="4"></circle>
              </svg>
              <span class="auth-label" id="authLabel">Sign In</span>
            </button>
            <div class="auth-dropdown" id="authDropdown">
              <!-- Signed-in Profile -->
              <div class="auth-profile" id="authProfile" style="display:none">
                <div class="auth-profile-header">
                  <div class="auth-profile-avatar" id="authProfileAvatar">
                    <img id="authProfileImg" src="" alt="" style="display:none">
                    <span class="auth-profile-initial" id="authProfileInitial"></span>
                  </div>
                  <div class="auth-profile-info">
                    <span class="auth-profile-name" id="authProfileName"></span>
                    <span class="auth-profile-username" id="authProfileUsername"></span>
                  </div>
                  <div class="auth-profile-badge">HIVE</div>
                </div>
                <div class="auth-profile-stats" id="authProfileStats">
                  <div class="auth-stat">
                    <span class="auth-stat-label">Portfolio</span>
                    <span class="auth-stat-value" id="authStatValue">-</span>
                  </div>
                  <div class="auth-stat">
                    <span class="auth-stat-label">Return</span>
                    <span class="auth-stat-value" id="authStatReturn">-</span>
                  </div>
                </div>
                <div class="auth-drop-divider"></div>
                <div class="auth-profile-nav">
                  <a href="/sector/ai" class="auth-nav-item"><span class="auth-nav-icon">📡</span> AI</a>
                  <a href="/sector/cyber" class="auth-nav-item"><span class="auth-nav-icon">🛡️</span> Cyber</a>
                  <a href="/sector/defense" class="auth-nav-item"><span class="auth-nav-icon">⚔️</span> Defense</a>
                  <a href="/sector/space" class="auth-nav-item"><span class="auth-nav-icon">🚀</span> Space</a>
                  <a href="/sector/mega-cap" class="auth-nav-item"><span class="auth-nav-icon">🏢</span> Mega-Cap</a>
                  <a href="/sector/quantum" class="auth-nav-item"><span class="auth-nav-icon">🔬</span> Quantum</a>
                  <a href="/sector/ai-power" class="auth-nav-item"><span class="auth-nav-icon">⚡</span> AI Power</a>
                  <a href="/sector/etfs" class="auth-nav-item"><span class="auth-nav-icon">💼</span> ETFs</a>
                  <div class="auth-nav-section-header">FEATURES</div>
                  <a href="/hive" class="auth-nav-item"><span class="auth-nav-icon">🐝</span> Hive</a>
                  <a href="/signal-vs-the-street" class="auth-nav-item"><span class="auth-nav-icon">📈</span> Signal vs. Street</a>
                  <a href="/stocks/" class="auth-nav-item"><span class="auth-nav-icon">📉</span> Stock Pages</a>
                  <a href="/#scorecard" class="auth-nav-item"><span class="auth-nav-icon">📊</span> Signal Scorecard</a>
                </div>
                <div class="auth-drop-divider"></div>
                <div class="auth-profile-footer">
                  <a href="/hive" class="auth-footer-link" onclick="navigateToHiveLeaderboard(event)">Leaderboard</a>
                  <a href="/account/settings" class="auth-footer-link">Settings</a>
                  <button class="auth-signout-btn" id="authSignOut">Sign Out</button>
                </div>
              </div>
              <!-- Guest View -->
              <div class="auth-guest" id="authGuest">
                <div class="auth-guest-brand">
                  <span class="auth-guest-title">Welcome to <strong>The Signal</strong></span>
                  <span class="auth-guest-sub">Join the hive to track your portfolio</span>
                </div>
                <button class="auth-option auth-option-primary" onclick="showHiveJoinModal('login')">
                  <span class="auth-option-icon">🔑</span> Sign In
                </button>
                <button class="auth-option" onclick="showHiveJoinModal('register')">
                  <span class="auth-option-icon">✨</span> Create Account
                </button>
                <div class="auth-drop-divider"></div>
                <div class="auth-profile-nav">
                  <a href="/sector/ai" class="auth-nav-item"><span class="auth-nav-icon">📡</span> AI</a>
                  <a href="/sector/cyber" class="auth-nav-item"><span class="auth-nav-icon">🛡️</span> Cyber</a>
                  <a href="/sector/defense" class="auth-nav-item"><span class="auth-nav-icon">⚔️</span> Defense</a>
                  <a href="/sector/space" class="auth-nav-item"><span class="auth-nav-icon">🚀</span> Space</a>
                  <a href="/sector/mega-cap" class="auth-nav-item"><span class="auth-nav-icon">🏢</span> Mega-Cap</a>
                  <a href="/sector/quantum" class="auth-nav-item"><span class="auth-nav-icon">🔬</span> Quantum</a>
                  <a href="/sector/ai-power" class="auth-nav-item"><span class="auth-nav-icon">⚡</span> AI Power</a>
                  <a href="/sector/etfs" class="auth-nav-item"><span class="auth-nav-icon">💼</span> ETFs</a>
                  <div class="auth-nav-section-header">FEATURES</div>
                  <a href="/hive" class="auth-nav-item"><span class="auth-nav-icon">🐝</span> Hive</a>
                  <a href="/signal-vs-the-street" class="auth-nav-item"><span class="auth-nav-icon">📈</span> Signal vs. Street</a>
                  <a href="/stocks/" class="auth-nav-item"><span class="auth-nav-icon">📉</span> Stock Pages</a>
                  <a href="/#scorecard" class="auth-nav-item"><span class="auth-nav-icon">📊</span> Signal Scorecard</a>
                </div>
              </div>
          </div>
        </div>
        <button class="nav-btn hamburger-btn" id="hamburgerToggle" aria-label="Menu">
          <span class="hamburger-line"></span>
          <span class="hamburger-line"></span>
          <span class="hamburger-line"></span>
        </button>
      </div>
    </div>
  </nav>

  <!-- Rocket Lab-Style Drawer -->
  <div class="drawer-overlay" id="drawerOverlay"></div>
  <div class="drawer" id="drawer">
    <div class="drawer-header">
      <a href="/" class="drawer-logo">
        <span class="the">THE</span>
        <span class="signal">SIGNAL</span>
      </a>
      <button class="drawer-close" id="drawerClose" aria-label="Close menu">&#10005;</button>
    </div>
    <div class="drawer-body" id="drawerBody">
      <div class="drawer-main" id="drawerMain">
        <div class="drawer-section-label">SECTORS</div>
        <a href="javascript:void(0)" class="drawer-link" onclick="openSubDrawer()">SECTORS</a>
        <a href="/stocks/" class="drawer-link">STOCK PAGES</a>
        <a href="/#scorecard" class="drawer-link">SIGNAL SCORECARD</a>
        <a href="/hive" class="drawer-link">HIVE</a>
        <a href="/signal-vs-the-street" class="drawer-link">SIGNAL VS. STREET</a>
        <a href="/premium" class="drawer-link">PREMIUM DASHBOARD</a>
        <a href="/insights" class="drawer-link">TRADER INSIGHTS</a>
        <a href="/watchlist" class="drawer-link">MY WATCHLIST</a>
        <a href="/pricing" class="drawer-link">SIGNAL PREMIUM</a>
        <a href="/pricing" class="drawer-cta">GET PREMIUM ACCESS</a>
      </div>
      <div class="drawer-sub" id="drawerSub">
        <div class="sub-header" onclick="closeSubDrawer()">
          <span class="sub-back">&#8249;</span>
          <span class="sub-title">SECTORS</span>
        </div>
        <a href="/sector/ai" class="drawer-link">AI</a>
        <a href="/sector/cyber" class="drawer-link">CYBER</a>
        <a href="/sector/defense" class="drawer-link">DEFENSE</a>
        <a href="/sector/space" class="drawer-link">SPACE</a>
        <a href="/sector/mega-cap" class="drawer-link">MEGA-CAP</a>
        <a href="/sector/quantum" class="drawer-link">QUANTUM</a>
        <a href="/sector/ai-power" class="drawer-link">AI POWER</a>
        <a href="/sector/etfs" class="drawer-link">ETFS</a>
      </div>
    </div>
  </div>

  <!-- Search Overlay -->
  <div class="search-overlay" id="searchOverlay">
    <div class="search-container">
      <div class="search-header">
        <input type="text" class="search-input" id="searchInput" placeholder="Search articles, stocks, sectors..." autocomplete="off">
        <button class="search-close-btn" id="searchClose" aria-label="Close search">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <line x1="18" y1="6" x2="6" y2="18"></line>
            <line x1="6" y1="6" x2="18" y2="18"></line>
          </svg>
        </button>
      </div>
      <div class="search-results" id="searchResults"></div>
    </div>
  </div>
`;
}

// Drawer JS that needs to be in every page
function getSharedNavJS() {
  return `
<script>
// Shared Navigation - Drawer, Search, Auth
document.addEventListener('DOMContentLoaded', function() {
  var btn = document.querySelector('.hamburger-btn');
  var drawer = document.getElementById('drawer');
  var overlay = document.getElementById('drawerOverlay');
  var closeBtn = document.getElementById('drawerClose');

  if (btn && drawer && overlay) {
    btn.addEventListener('click', function() {
      drawer.classList.add('open');
      overlay.classList.add('open');
      document.body.style.overflow = 'hidden';
    });
    function closeDrawer() {
      drawer.classList.remove('open');
      overlay.classList.remove('open');
      document.body.style.overflow = '';
    }
    overlay.addEventListener('click', closeDrawer);
    if (closeBtn) closeBtn.addEventListener('click', closeDrawer);
  }

  // Sub-drawer for sectors
  window.openSubDrawer = function() {
    var main = document.getElementById('drawerMain');
    var sub = document.getElementById('drawerSub');
    if (main && sub) { main.style.display = 'none'; sub.style.display = 'block'; }
  };
  window.closeSubDrawer = function() {
    var main = document.getElementById('drawerMain');
    var sub = document.getElementById('drawerSub');
    if (main && sub) { main.style.display = 'block'; sub.style.display = 'none'; }
  };

  // Search overlay
  var searchBtn = document.getElementById('searchToggle');
  var searchOverlay = document.getElementById('searchOverlay');
  var searchClose = document.getElementById('searchClose');
  var searchInput = document.getElementById('searchInput');

  if (searchBtn && searchOverlay) {
    searchBtn.addEventListener('click', function() {
      searchOverlay.classList.add('open');
      if (searchInput) setTimeout(function() { searchInput.focus(); }, 100);
    });
    if (searchClose) searchClose.addEventListener('click', function() {
      searchOverlay.classList.remove('open');
    });
    document.addEventListener('keydown', function(e) {
      if (e.key === 'Escape' && searchOverlay.classList.contains('open')) {
        searchOverlay.classList.remove('open');
      }
    });
  }
});
</script>
`;
}

module.exports = { getSharedNav, getSharedNavJS };
