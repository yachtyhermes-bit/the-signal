#!/usr/bin/env python3
"""
Apply Rocket Lab-style nav to all _backup_dist HTML files.
Strategy: For each file, remove old nav+drawer+old-JS, then insert new nav+drawer+new-JS.
"""

import re
import os

DIST = os.path.join(os.path.dirname(os.path.dirname(__file__)), '_backup_dist')

# ========== NEW DRAWER HTML (shared across all pages) ==========
NEW_DRAWER_HTML = """  <!-- ROCKET LAB DRAWER -->
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
        <a href="javascript:void(0)" class="drawer-link drawer-link-has-sub" onclick="openSubDrawer()">SECTORS</a>
        <a href="/stocks/" class="drawer-link">STOCK PAGES</a>
        <a href="/#scorecard" class="drawer-link">SIGNAL SCORECARD</a>
        <a href="/hive" class="drawer-link">HIVE</a>
        <a href="/signal-vs-the-street" class="drawer-link">SIGNAL VS. STREET</a>
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
  </div>"""

# ========== DESKTOP TOPNAV HTML (shared across all pages) ==========
NEW_TOPNAV_HTML = """  <!-- DESKTOP TOP NAV -->
  <nav class="topnav" id="topnav">
    <div class="topnav-inner">
      <a href="/" class="topnav-logo">
        <span class="the">THE</span>
        <span class="signal">SIGNAL</span>
      </a>
      <div class="topnav-items">
        <div class="topnav-item has-dropdown" id="sectorsDropdown">
          <button class="topnav-link" onclick="toggleDropdown(event)">SECTORS <span class="chevron">&#8250;</span></button>
          <div class="topnav-dropdown">
            <a href="/sector/ai">AI</a>
            <a href="/sector/cyber">CYBER</a>
            <a href="/sector/defense">DEFENSE</a>
            <a href="/sector/space">SPACE</a>
            <a href="/sector/mega-cap">MEGA-CAP</a>
            <a href="/sector/quantum">QUANTUM</a>
            <a href="/sector/ai-power">AI POWER</a>
            <a href="/sector/etfs">ETFS</a>
          </div>
        </div>
        <div class="topnav-item"><a href="/stocks/" class="topnav-link">STOCK PAGES</a></div>
        <div class="topnav-item"><a href="/#scorecard" class="topnav-link">SCORECARD</a></div>
        <div class="topnav-item"><a href="/hive" class="topnav-link">HIVE</a></div>
        <div class="topnav-item"><a href="/signal-vs-the-street" class="topnav-link">VS. STREET</a></div>
        <div class="topnav-item"><a href="/pricing" class="topnav-link">PREMIUM</a></div>
        <a href="/pricing" class="topnav-cta">GET PREMIUM ACCESS</a>
      </div>
      <div class="topnav-actions">
        <button class="topnav-search-btn" id="searchToggle" aria-label="Search">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg>
        </button>
        <div class="auth-container" id="authContainer">
          <button class="topnav-nav-btn" id="authToggle" aria-label="Sign In">
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
                <div class="auth-stat"><span class="auth-stat-label">Portfolio</span><span class="auth-stat-value" id="authStatValue">-</span></div>
                <div class="auth-stat"><span class="auth-stat-label">Return</span><span class="auth-stat-value" id="authStatReturn">-</span></div>
              </div>
              <div class="auth-drop-divider"></div>
              <div class="auth-profile-nav">
                <a href="/sector/ai" class="auth-nav-item">AI</a>
                <a href="/sector/cyber" class="auth-nav-item">Cyber</a>
                <a href="/sector/defense" class="auth-nav-item">Defense</a>
                <a href="/sector/space" class="auth-nav-item">Space</a>
                <a href="/sector/mega-cap" class="auth-nav-item">Mega-Cap</a>
                <a href="/sector/quantum" class="auth-nav-item">Quantum</a>
                <a href="/sector/ai-power" class="auth-nav-item">AI Power</a>
                <a href="/sector/etfs" class="auth-nav-item">ETFs</a>
              </div>
              <div class="auth-drop-divider"></div>
              <div class="auth-profile-footer">
                <a href="/hive" class="auth-footer-link" onclick="navigateToHiveLeaderboard(event)">Leaderboard</a>
                <a href="/account/settings" class="auth-footer-link">Settings</a>
                <button class="auth-signout-btn" id="authSignOut">Sign Out</button>
              </div>
            </div>
            <div class="auth-guest" id="authGuest">
              <div class="auth-guest-brand">
                <span class="auth-guest-title">Welcome to <strong>The Signal</strong></span>
                <span class="auth-guest-sub">Join the hive to track your portfolio</span>
              </div>
              <button class="auth-option auth-option-primary" onclick="showHiveJoinModal('login')">Sign In</button>
              <button class="auth-option" onclick="showHiveJoinModal('register')">Create Account</button>
            </div>
          </div>
        </div>
        <button class="topnav-hamburger" onclick="openDrawer()" aria-label="Open menu">
          <span></span><span></span><span></span>
        </button>
      </div>
    </div>
  </nav>"""

# ========== MOBILE TOPBAR HTML ==========
NEW_MOBILE_TOPBAR_HTML = """  <!-- MOBILE TOP BAR -->
  <div class="mobile-topbar">
    <button class="mobile-hamburger" onclick="openDrawer()" aria-label="Open menu">
      <span></span><span></span><span></span>
    </button>
    <a href="/" class="topnav-logo">
      <span class="the">THE</span>
      <span class="signal">SIGNAL</span>
    </a>
    <div class="mobile-actions">
      <button class="topnav-search-btn mobile-search-trigger" aria-label="Search">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg>
      </button>
      <div class="auth-container" id="mobileAuthContainer">
        <button class="topnav-nav-btn" id="mobileAuthToggle" aria-label="Sign In">
          <div class="auth-btn-avatar" id="mobileAuthBtnAvatar">
            <span class="auth-btn-initial" id="mobileAuthBtnInitial"></span>
            <img class="auth-btn-img" id="mobileAuthBtnImg" src="" alt="" style="display:none">
          </div>
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="auth-btn-icon" id="mobileAuthBtnIcon">
            <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path>
            <circle cx="12" cy="7" r="4"></circle>
          </svg>
          <span class="auth-label" id="mobileAuthLabel">Sign In</span>
        </button>
      </div>
    </div>
  </div>"""

# ========== NEW DRAWER JS ==========
NEW_DRAWER_JS = """  <script>
  (function() {
    var drawer = document.getElementById('drawer');
    var overlay = document.getElementById('drawerOverlay');
    var drawerMain = document.getElementById('drawerMain');
    var drawerSub = document.getElementById('drawerSub');
    var sectorsDropdown = document.getElementById('sectorsDropdown');
    var drawerBody = document.getElementById('drawerBody');

    // Fallback: make drawerBody behave like the content area
    if (drawerBody) {
      drawerBody.style.position = 'relative';
      drawerBody.style.overflow = 'visible';
      if (drawerMain) { drawerMain.style.position = 'absolute'; drawerMain.style.inset = '0'; }
      if (drawerSub) { drawerSub.style.position = 'absolute'; drawerSub.style.inset = '0'; }
    }

    window.openDrawer = function() {
      drawer.classList.add('open');
      overlay.classList.add('open');
      document.body.style.overflow = 'hidden';
    };
    window.closeDrawer = function() {
      drawer.classList.remove('open');
      overlay.classList.remove('open');
      document.body.style.overflow = '';
      setTimeout(function() {
        if (drawerMain) drawerMain.classList.remove('hidden');
        if (drawerSub) drawerSub.classList.remove('active');
      }, 350);
    };
    window.openSubDrawer = function() {
      if (drawerMain) drawerMain.classList.add('hidden');
      if (drawerSub) drawerSub.classList.add('active');
    };
    window.closeSubDrawer = function() {
      if (drawerMain) drawerMain.classList.remove('hidden');
      if (drawerSub) drawerSub.classList.remove('active');
    };
    window.toggleDropdown = function(e) {
      e.stopPropagation();
      if (sectorsDropdown) sectorsDropdown.classList.toggle('open');
    };

    // Close buttons
    var closeBtn = document.getElementById('drawerClose');
    if (closeBtn) closeBtn.addEventListener('click', window.closeDrawer);
    if (overlay) overlay.addEventListener('click', window.closeDrawer);

    // ESC to close
    document.addEventListener('keydown', function(e) {
      if (e.key === 'Escape') {
        window.closeDrawer();
        if (sectorsDropdown) sectorsDropdown.classList.remove('open');
      }
    });
    // Click-outside dropdown
    document.addEventListener('click', function(e) {
      if (sectorsDropdown && !sectorsDropdown.contains(e.target)) {
        sectorsDropdown.classList.remove('open');
      }
    });
    // Close drawer on any link click inside
    if (drawer) {
      drawer.querySelectorAll('a[href^="/"]').forEach(function(a) {
        a.addEventListener('click', function() { window.closeDrawer(); });
      });
    }
    // Mobile search → trigger desktop search toggle
    (function() {
      var mobileSearch = document.querySelector('.mobile-search-trigger');
      var desktopSearch = document.getElementById('searchToggle');
      if (mobileSearch && desktopSearch) {
        mobileSearch.addEventListener('click', function() {
          if (desktopSearch.click) desktopSearch.click();
        });
      }
    })();
  })();
  </script>"""


# ========== CSS to add/replace in main.css ==========
NEW_DRAWER_CSS = """/* ============================================================
   ROCKET LAB-STYLE DRAWER + TOPNAV
   Desktop: horizontal top nav with SECTORS dropdown
   Mobile: full-screen overlay drawer with sub-drawer for sectors
   Font: Barlow Condensed, black bg, off-white text, Signal blue
   ============================================================ */

/* ---- Drawer Overlay ---- */
.drawer-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.6);
  z-index: 900;
  opacity: 0;
  visibility: hidden;
  transition: opacity 0.3s ease, visibility 0.3s;
  backdrop-filter: blur(2px);
  -webkit-backdrop-filter: blur(2px);
}
.drawer-overlay.open,
.drawer-overlay.active {
  opacity: 1;
  visibility: visible;
}

/* ---- Drawer Panel ---- */
.drawer {
  position: fixed;
  top: 0;
  left: 0;
  bottom: 0;
  width: 100%;
  max-width: 420px;
  background: #000;
  z-index: 1000;
  transform: translateX(-100%);
  transition: transform 0.35s cubic-bezier(0.25, 0.46, 0.45, 0.94);
  display: flex;
  flex-direction: column;
  overflow: hidden;
}
.drawer.open {
  transform: translateX(0);
}

/* ---- Drawer Header ---- */
.drawer-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 24px 28px;
  border-bottom: 1px solid rgba(229, 229, 229, 0.15);
  min-height: 80px;
}
.drawer-logo {
  font-family: 'Barlow Condensed', sans-serif;
  font-weight: 900;
  font-size: 16px;
  line-height: 1;
  display: flex;
  flex-direction: column;
  text-decoration: none;
}
.drawer-logo .the {
  background: linear-gradient(135deg, #3b82f6, #8b5cf6);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  font-size: 10px;
  letter-spacing: 0.25em;
  line-height: 1.1;
}
.drawer-logo .signal {
  background: linear-gradient(135deg, #3b82f6, #8b5cf6);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  font-size: 20px;
  letter-spacing: 0.05em;
  line-height: 1;
}
.drawer-logo-text { display: none !important; }
.drawer-logo-img { display: none !important; }
.drawer-close {
  background: none;
  border: none;
  cursor: pointer;
  width: 36px;
  height: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #3b82f6;
  font-size: 24px;
  font-weight: 300;
  transition: opacity 0.15s ease;
  padding: 0;
  line-height: 1;
}
.drawer-close:hover { opacity: 0.6; }

/* ---- Drawer Body (content wrapper for main+sub) ---- */
.drawer-body {
  flex: 1;
  position: relative;
  overflow: hidden;
}
.drawer-main,
.drawer-sub {
  position: absolute;
  inset: 0;
  overflow-y: auto;
  transition: transform 0.3s cubic-bezier(0.25, 0.46, 0.45, 0.94);
}
.drawer-main {
  transform: translateX(0);
}
.drawer-sub {
  transform: translateX(100%);
}
.drawer-main.hidden {
  transform: translateX(-100%);
}
.drawer-sub.active {
  transform: translateX(0);
}

/* ---- Menu Items ---- */
.drawer-link {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 22px 28px;
  border-bottom: 1px solid rgba(229, 229, 229, 0.15);
  cursor: pointer;
  text-decoration: none;
  color: #e5e5e5;
  transition: opacity 0.15s ease;
  font-family: 'Barlow Condensed', sans-serif;
  font-size: 18px;
  font-weight: 500;
  letter-spacing: 0.18em;
  text-transform: uppercase;
}
.drawer-link:hover { opacity: 0.6; }
.drawer-link::after {
  content: '\\203A';
  font-size: 20px;
  font-weight: 300;
  color: #e5e5e5;
  opacity: 0.7;
  line-height: 1;
}
.drawer-arrow { display: none; }

/* ---- Section Labels ---- */
.drawer-section-label {
  font-family: 'Barlow Condensed', sans-serif;
  font-size: 10px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.2em;
  color: rgba(229, 229, 229, 0.4);
  padding: 20px 28px 8px;
}

/* ---- Divider ---- */
.drawer-divider {
  height: 1px;
  background: rgba(229, 229, 229, 0.15);
  margin: 0;
  border: none;
}

/* ---- CTA Button ---- */
.drawer-cta {
  margin: 24px 28px;
  display: block;
  text-align: center;
  text-transform: uppercase;
  font-size: 12px;
  font-weight: 600;
  letter-spacing: 0.18em;
  color: #3b82f6;
  border: 1px solid #3b82f6;
  padding: 16px 24px;
  text-decoration: none;
  transition: background 0.15s ease, color 0.15s ease;
  font-family: 'Barlow Condensed', sans-serif;
}
.drawer-cta::after { content: none !important; }
.drawer-cta:hover {
  background: #3b82f6;
  color: #e5e5e5;
}

/* ---- Sub-drawer Header ---- */
.sub-header {
  display: flex;
  align-items: center;
  padding: 22px 28px;
  border-bottom: 1px solid rgba(229, 229, 229, 0.15);
  cursor: pointer;
  text-decoration: none;
  color: #e5e5e5;
  transition: opacity 0.15s ease;
  font-family: 'Barlow Condensed', sans-serif;
}
.sub-header::after { content: none !important; }
.sub-header:hover { opacity: 0.6; }
.sub-back {
  font-size: 20px;
  font-weight: 300;
  margin-right: 12px;
  opacity: 0.7;
  line-height: 1;
}
.sub-title {
  text-transform: uppercase;
  font-size: 18px;
  font-weight: 500;
  letter-spacing: 0.18em;
}

/* ============================================================
   Desktop Top Navigation
   ============================================================ */
.topnav {
  display: none;
  position: fixed;
  top: 0; left: 0; right: 0;
  z-index: 1000;
  background: #000;
  border-bottom: 1px solid rgba(229, 229, 229, 0.15);
  height: 64px;
}
.topnav-inner {
  max-width: 1400px;
  margin: 0 auto;
  padding: 0 32px;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: space-between;
}
.topnav-logo {
  font-family: 'Barlow Condensed', sans-serif;
  font-weight: 900;
  font-size: 20px;
  letter-spacing: 0.02em;
  line-height: 1;
  display: flex;
  flex-direction: column;
  text-decoration: none;
  color: #e5e5e5;
}
.topnav-logo .the {
  background: linear-gradient(135deg, #3b82f6, #8b5cf6);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  font-size: 12px;
  letter-spacing: 0.2em;
  line-height: 1.1;
}
.topnav-logo .signal {
  background: linear-gradient(135deg, #3b82f6, #8b5cf6);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  font-size: 22px;
  letter-spacing: 0.05em;
  line-height: 1;
}
.topnav-items {
  display: flex;
  align-items: center;
  height: 100%;
  margin-left: 40px;
}
.topnav-item {
  position: relative;
  height: 100%;
  display: flex;
  align-items: center;
}
.topnav-link {
  color: #e5e5e5;
  text-decoration: none;
  text-transform: uppercase;
  font-family: 'Barlow Condensed', sans-serif;
  font-size: 12px;
  font-weight: 500;
  letter-spacing: 0.15em;
  padding: 0 20px;
  height: 100%;
  display: flex;
  align-items: center;
  transition: opacity 0.15s ease;
  cursor: pointer;
  background: none;
  border: none;
}
.topnav-link:hover { opacity: 0.6; }
.topnav-link .chevron { font-size: 16px; margin-left: 6px; font-weight: 300; }

/* Desktop dropdown */
.topnav-dropdown {
  position: absolute;
  top: 100%;
  left: 0;
  background: #000;
  border: 1px solid rgba(229, 229, 229, 0.15);
  border-top: none;
  min-width: 220px;
  opacity: 0;
  visibility: hidden;
  transform: translateY(-4px);
  transition: opacity 0.2s ease, transform 0.2s ease, visibility 0.2s;
  z-index: 200;
}
.topnav-item.has-dropdown:hover .topnav-dropdown,
.topnav-item.has-dropdown.open .topnav-dropdown {
  opacity: 1;
  visibility: visible;
  transform: translateY(0);
}
.topnav-dropdown a {
  display: block;
  color: #e5e5e5;
  text-decoration: none;
  text-transform: uppercase;
  font-family: 'Barlow Condensed', sans-serif;
  font-size: 11px;
  font-weight: 500;
  letter-spacing: 0.15em;
  padding: 14px 24px;
  border-bottom: 1px solid rgba(229, 229, 229, 0.15);
  transition: opacity 0.15s ease;
}
.topnav-dropdown a:last-child { border-bottom: none; }
.topnav-dropdown a:hover { opacity: 0.6; }

.topnav-cta {
  color: #3b82f6;
  text-decoration: none;
  text-transform: uppercase;
  font-family: 'Barlow Condensed', sans-serif;
  font-size: 11px;
  font-weight: 600;
  letter-spacing: 0.15em;
  border: 1px solid #3b82f6;
  padding: 8px 16px;
  margin-left: 16px;
  transition: background 0.15s ease, color 0.15s ease;
  cursor: pointer;
}
.topnav-cta:hover { background: #3b82f6; color: #e5e5e5; }

.topnav-actions {
  display: flex;
  align-items: center;
  height: 100%;
  gap: 8px;
}
.topnav-search-btn {
  background: none;
  border: none;
  cursor: pointer;
  color: #e5e5e5;
  padding: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
}
.topnav-search-btn:hover { opacity: 0.6; }
.topnav-nav-btn {
  background: none;
  border: 1px solid rgba(229, 229, 229, 0.2);
  cursor: pointer;
  color: #e5e5e5;
  padding: 6px 12px;
  display: flex;
  align-items: center;
  gap: 6px;
  border-radius: 6px;
  font-family: 'Barlow Condensed', sans-serif;
  font-size: 11px;
  text-transform: uppercase;
  letter-spacing: 0.1em;
}
.topnav-nav-btn:hover { border-color: rgba(229, 229, 229, 0.4); }
.topnav-hamburger {
  background: none;
  border: none;
  cursor: pointer;
  padding: 8px;
  display: flex;
  flex-direction: column;
  gap: 5px;
}
.topnav-hamburger span {
  display: block;
  width: 20px;
  height: 1.5px;
  background: #e5e5e5;
  transition: transform 0.2s ease;
}
.topnav-hamburger:hover span { transform: scaleX(0.7); transform-origin: left; }

/* ============================================================
   Mobile Top Bar
   ============================================================ */
.mobile-topbar {
  position: fixed;
  top: 0; left: 0; right: 0;
  z-index: 1000;
  background: #000;
  border-bottom: 1px solid rgba(229, 229, 229, 0.15);
  height: 60px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 20px;
}
.mobile-hamburger {
  background: none;
  border: none;
  cursor: pointer;
  padding: 8px;
  display: flex;
  flex-direction: column;
  gap: 5px;
}
.mobile-hamburger span {
  display: block;
  width: 22px;
  height: 1.5px;
  background: #e5e5e5;
}
.mobile-actions {
  display: flex;
  align-items: center;
  gap: 8px;
}

/* ============================================================
   Responsive Breakpoints
   ============================================================ */
@media (min-width: 901px) {
  .mobile-topbar { display: none !important; }
  .topnav { display: block; }
  .drawer { max-width: 440px; }
}
@media (max-width: 900px) {
  .topnav { display: none !important; }
  .mobile-topbar { display: flex; }
}

/* Hide OLD nav when new drawer is present */
body:has(.drawer) > .nav,
body:has(.drawer) > nav.nav,
body:has(.drawer) > .site-nav {
  display: none !important;
}
@supports not selector(:has(*)) {
  .new-nav-active > .nav,
  .new-nav-active > nav.nav {
    display: none !important;
  }
}
"""


def fix_main_css():
    """Replace the old drawer CSS in main.css with the Rocket Lab CSS."""
    path = os.path.join(DIST, 'css', 'main.css')
    with open(path, 'r') as f:
        content = f.read()

    # Old drawer CSS runs from line 1985 (.drawer-overlay) to line 2193 (.drawer-footer { display: none; })
    start_marker = '.drawer-overlay {\n  display: none;'
    end_marker = '/* === SEARCH OVERLAY === */'
    
    start_idx = content.find(start_marker)
    end_idx = content.find(end_marker)
    
    if start_idx == -1:
        # Try alternative start (without "display: none")
        start_marker = '.drawer-overlay {'
        start_idx = content.find(start_marker)
    
    if start_idx == -1 or end_idx == -1:
        print(f"  ⚠️  Could not find drawer CSS markers in main.css (start={start_idx}, end={end_idx})")
        # Last resort: replace any .drawer-overlay section
        if start_idx != -1:
            # Find next major section after the drawer
            # Just replace from .drawer-overlay to .search-overlay
            search_overlay_idx = content.find('.search-overlay {', start_idx + 100)
            if search_overlay_idx != -1:
                new_content = content[:start_idx] + NEW_DRAWER_CSS + '\n' + content[search_overlay_idx:]
                with open(path, 'w') as f:
                    f.write(new_content)
                print(f"  ✅ Replaced drawer CSS in main.css (fallback)")
                return True
        return False
    
    old_css = content[start_idx:end_idx]
    print(f"  Found old drawer CSS: {len(old_css)} chars")
    
    new_content = content[:start_idx] + NEW_DRAWER_CSS + '\n' + content[end_idx:]
    
    with open(path, 'w') as f:
        f.write(new_content)
    print(f"  ✅ Replaced drawer CSS in main.css")
    return True


def add_barlow_condensed(content):
    """Add Barlow Condensed to the Google Fonts link."""
    if 'Barlow+Condensed' in content or 'Barlow Condensed' in content:
        return content
    
    # Match the Google Fonts CSS2 link
    pattern = re.compile(r'<link[^>]*fonts\.googleapis\.com/css2\?family=[^>]+>')
    match = pattern.search(content)
    
    if match:
        old_link = match.group(0)
        # Add Barlow Condensed to the URL
        # The URL format: family=Anton&family=Inter:...&display=swap
        new_link = old_link.replace('&display=swap', '&family=Barlow+Condensed:wght@400;500;600;700&display=swap')
        if 'display=swap' not in old_link:
            new_link = new_link.replace('">', '&family=Barlow+Condensed:wght@400;500;600;700&display=swap">')
        return content[:match.start()] + new_link + content[match.end():]
    else:
        # No fonts.googleapis.com/css2 link found - add one
        # Insert after </head> or after existing stylesheet link
        insert_point = content.find('</head>')
        if insert_point != -1:
            new_link = '<link rel="preconnect" href="https://fonts.googleapis.com">\n  '
            new_link += '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n  '
            new_link += '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@400;500;600;700&display=swap">\n  '
            return content[:insert_point] + new_link + content[insert_point:]
    
    return content


def remove_old_nav(content):
    """Remove the old <nav class="nav">...</nav> block."""
    # Find <nav class="nav"> (or <nav class='nav'>)
    nav_pattern = re.compile(r'<nav\s+class="nav"[^>]*>[\s\S]*?</nav>')
    return nav_pattern.sub('', content)


def remove_old_drawer(content):
    """Remove the old drawer section (overlay + drawer div)."""
    # Pattern: optional comment + <div class="drawer-overlay"...>...drawer-body...</div></div>
    # The drawer ends with nested closing: </div>\n  </div>
    
    # Find the drawer-overlay div
    drawer_start_pattern = re.compile(
        r'(?:<!--\s*(?:═+\s*)?KRATOS[^\-]*(?:═+\s*)?-->\s*|'
        r'<!--\s*DRAWER\s*-->\s*|'
        r'<!--\s*Kratos[^-]*-->\s*|'
        r'<!--\s*KRATOS[^-]*-->\s*|'
        r'\s*)'
        r'<div\s+class="drawer-overlay"[^>]*id="drawerOverlay"[^>]*>\s*</div>',
        re.IGNORECASE
    )
    
    match = drawer_start_pattern.search(content)
    if not match:
        # Simpler pattern
        match = re.search(r'<div\s+class="drawer-overlay"[^>]*id="drawerOverlay"', content)
    
    if not match:
        # Even simpler
        drawer_overlay_idx = content.find('drawerOverlay')
        if drawer_overlay_idx == -1:
            return content
        # Go back to start of tag
        drawer_start = content.rfind('<div', 0, drawer_overlay_idx)
        if drawer_start == -1:
            return content
    
    start_pos = match.start() if match else drawer_start
    
    # Now find end of drawer - it's a <div class="drawer" ...>...</div>
    # The drawer div has child: .drawer-header, .drawer-body
    # Find the drawer div start
    drawer_div_idx = content.find('<div class="drawer"', start_pos)
    if drawer_div_idx == -1:
        drawer_div_idx = content.find('<div class="drawer ', start_pos)
    
    if drawer_div_idx == -1:
        # Just find </div> after drawer-body
        drawer_body_idx = content.find('drawer-body', start_pos)
        if drawer_body_idx == -1:
            return content
        # After drawer-body's content, we need to close drawer-body + drawer
        # Find </div>\n  </div> pattern
        search_region = content[drawer_body_idx:]
        end_match = re.search(r'</div>\s*</div>', search_region)
        if end_match:
            actual_end = drawer_body_idx + end_match.end()
            # Also skip any following newline
            while actual_end < len(content) and content[actual_end] in ' \t\n':
                actual_end += 1
            new_content = content[:start_pos] + content[actual_end:]
            return new_content
        return content
    
    # From drawer_div_idx, count div nesting to find the matching close
    div_count = 0
    i = drawer_div_idx
    end_pos = None
    while i < len(content):
        if content[i:i+4] == '<div':
            div_count += 1
        elif content[i:i+6] == '</div>':
            div_count -= 1
            if div_count == 0:
                end_pos = i + 6
                break
        i += 1
    
    if end_pos:
        # Also consume any trailing whitespace/newline
        while end_pos < len(content) and content[end_pos] in ' \t\n':
            end_pos += 1
        new_content = content[:start_pos] + content[end_pos:]
        # Also remove any preceding comment block if we haven't already
        return new_content
    
    return content


def remove_old_drawer_js(content):
    """Remove old drawer JavaScript."""
    # Pattern: <script> ... hamburgerToggle ... openDrawer/closeDrawer ... </script>
    patterns = [
        re.compile(r'\s*<script>\s*\n\s*document\.addEventListener\(\'DOMContentLoaded\',\s*function\(\)\{\s*\n?\s*var btn\s*=\s*document\.getElementById\(\'hamburgerToggle\'\)[\s\S]*?\}\);\s*\n?\s*\}\);\s*\n?\s*</script>', re.DOTALL),
        re.compile(r'\s*<script>\s*\n?\s*document\.addEventListener\(\'DOMContentLoaded\',\s*function\(\)\{\s*\n?\s*var drawer\s*=\s*document\.getElementById\(\'drawer\'\)[\s\S]*?\}\);\s*\n?\s*\}\);\s*\n?\s*</script>', re.DOTALL),
        # Signal-vs-street inline JS
        re.compile(r'\s*<script>\s*\n?\s*\(function\(\)\s*\{\s*\n?\s*var drawer\s*=\s*document\.getElementById\(\'drawer\'\)[\s\S]*?\}\);\s*\n?\s*\}\)\(\);\s*\n?\s*</script>', re.DOTALL),
    ]
    for pat in patterns:
        content = pat.sub('', content)
    return content


def remove_preceding_comments(content, pos_before_new_content):
    """Remove any orphan comment blocks between the old nav removal point and content."""
    return content


def process_file(filepath):
    """Process a single HTML file."""
    basename = os.path.basename(filepath)
    relpath = os.path.relpath(filepath, DIST)
    
    with open(filepath, 'r') as f:
        content = f.read()
    
    has_old_nav = bool(re.search(r'<nav\s+class="nav"', content))
    has_old_drawer = bool(re.search(r'drawerOverlay', content))
    
    if not has_old_nav and not has_old_drawer:
        # Pages like pricing that have NO nav/drawer - just insert new nav/drawer after <body>
        content = add_barlow_condensed(content)
        body_idx = content.find('<body>')
        if body_idx != -1:
            insert_pos = body_idx + len('<body>')
            new_block = '\n' + NEW_TOPNAV_HTML + '\n' + NEW_MOBILE_TOPBAR_HTML + '\n' + NEW_DRAWER_HTML + '\n'
            content = content[:insert_pos] + new_block + content[insert_pos:]
        else:
            print(f"  ⚠️  No <body> tag in {relpath}")
            return
        
        # Add drawer JS before </body>
        body_close = content.rfind('</body>')
        if body_close != -1:
            content = content[:body_close] + NEW_DRAWER_JS + '\n  ' + content[body_close:]
        
        with open(filepath, 'w') as f:
            f.write(content)
        print(f"  ✅ {relpath} (no previous nav/drawer - inserted new)")
        return
    
    # Step 1: Add Barlow Condensed to fonts
    content = add_barlow_condensed(content)
    
    # Step 2: Remove old nav
    if has_old_nav:
        content = remove_old_nav(content)
    
    # Step 3: Remove old drawer
    if has_old_drawer:
        content = remove_old_drawer(content)
    
    # Step 4: Remove old drawer JS
    content = remove_old_drawer_js(content)
    
    # Step 5: Insert new nav + topbar + drawer right after <body>
    body_idx = content.find('<body>')
    if body_idx == -1:
        print(f"  ⚠️  No <body> in {relpath}")
        return
    
    insert_pos = body_idx + len('<body>')
    new_block = '\n' + NEW_TOPNAV_HTML + '\n' + NEW_MOBILE_TOPBAR_HTML + '\n' + NEW_DRAWER_HTML + '\n'
    content = content[:insert_pos] + new_block + content[insert_pos:]
    
    # Step 6: Add drawer JS before </body>
    body_close = content.rfind('</body>')
    if body_close != -1:
        # Check if there's already our new JS - avoid duplicates
        if 'openSubDrawer' not in content:
            content = content[:body_close] + NEW_DRAWER_JS + '\n  ' + content[body_close:]
    
    # Step 7: Add class to body for fallback hiding of old nav
    if 'new-nav-active' not in content:
        content = content.replace('<body>', '<body class="new-nav-active">', 1)
    
    with open(filepath, 'w') as f:
        f.write(content)
    print(f"  ✅ {relpath}")


# Files to process
ALL_HTML_FILES = [
    os.path.join(DIST, 'index.html'),
    os.path.join(DIST, 'about', 'index.html'),
    os.path.join(DIST, 'pricing', 'index.html'),
    os.path.join(DIST, 'account', 'settings', 'index.html'),
    os.path.join(DIST, 'signal-vs-the-street', 'index.html'),
    os.path.join(DIST, 'hive', 'index.html'),
    os.path.join(DIST, 'hive', 'boardroom', 'index.html'),
    os.path.join(DIST, 'sector', 'ai', 'index.html'),
    os.path.join(DIST, 'sector', 'cyber', 'index.html'),
    os.path.join(DIST, 'sector', 'defense', 'index.html'),
    os.path.join(DIST, 'sector', 'space', 'index.html'),
    os.path.join(DIST, 'sector', 'mega-cap', 'index.html'),
    os.path.join(DIST, 'sector', 'quantum', 'index.html'),
]


def main():
    print("=" * 60)
    print("Applying Rocket Lab-style nav to readthesignal.net")
    print("=" * 60)
    
    # 1. Fix main.css
    print("\n[1] Updating css/main.css (drawer + topnav CSS)...")
    fix_main_css()
    
    # 2. Process each HTML file
    print("\n[2] Processing HTML files...")
    for filepath in ALL_HTML_FILES:
        if not os.path.exists(filepath):
            print(f"  ⚠️  MISSING: {os.path.relpath(filepath, DIST)}")
            continue
        process_file(filepath)
    
    print("\n" + "=" * 60)
    print("Done! Summary:")
    print("  - Replaced drawer CSS in css/main.css")
    print("  - Added Barlow Condensed font to all pages")
    print("  - Replaced old nav + drawer HTML in all pages")
    print("  - Added desktop topnav with SECTORS dropdown")
    print("  - Added mobile topbar + drawer with sub-drawer")
    print("  - Removed all emojis from nav labels")
    print("=" * 60)


if __name__ == '__main__':
    main()
