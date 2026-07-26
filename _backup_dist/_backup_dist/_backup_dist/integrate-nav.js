/**
 * Script to integrate Rocket Lab-style nav into all site pages.
 * Run once from /home/chino/thesignal/
 */
const fs = require('fs');
const path = require('path');

const DIST = path.join(__dirname, '_backup_dist');

// The new nav HTML (desktop topnav + mobile topbar + drawer overlay + drawer)
// Note: search and auth are handled by existing JS (search.js, auth.js) which target IDs
// We'll preserve authContainer and searchToggle IDs so they still work
function getNewNavHTML(hasSearch) {
  return `
  <!-- ===== ROCKET LAB NAV SYSTEM ===== -->
  <!-- Desktop Top Nav -->
  <nav class="rl-topnav" id="rlTopnav">
    <div class="rl-topnav-inner">
      <div class="rl-topnav-left">
        <a href="/" class="rl-topnav-logo">
          <span class="rl-the">THE</span>
          <span class="rl-signal">SIGNAL</span>
        </a>
        <div class="rl-topnav-items">
          <div class="rl-topnav-item has-dropdown" id="rlSectorsDropdown">
            <button class="rl-topnav-link" id="rlDropdownBtn">
              SECTORS <span class="rl-chevron">›</span>
            </button>
            <div class="rl-topnav-dropdown">
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
          <div class="rl-topnav-item"><a href="/stocks/" class="rl-topnav-link">STOCK PAGES</a></div>
          <div class="rl-topnav-item"><a href="/#scorecard" class="rl-topnav-link">SCORECARD</a></div>
          <div class="rl-topnav-item"><a href="/hive" class="rl-topnav-link">HIVE</a></div>
          <div class="rl-topnav-item"><a href="/signal-vs-the-street" class="rl-topnav-link">VS. STREET</a></div>
          <div class="rl-topnav-item"><a href="/pricing" class="rl-topnav-link">PREMIUM</a></div>
          <a href="/pricing" class="rl-topnav-cta">GET PREMIUM ACCESS</a>
        </div>
      </div>
      <div class="rl-topnav-actions">
        ${hasSearch ? `<button class="rl-nav-btn" id="searchToggle" aria-label="Search">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <circle cx="11" cy="11" r="8"></circle>
            <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
          </svg>
        </button>` : ''}
        <button class="rl-topnav-hamburger rl-hamburger" aria-label="Open menu">
          <span></span><span></span><span></span>
        </button>
      </div>
    </div>
  </nav>

  <!-- Mobile Top Bar -->
  <div class="rl-mobile-topbar" id="rlMobileTopbar">
    <button class="rl-mobile-hamburger rl-hamburger" aria-label="Open menu">
      <span></span><span></span><span></span>
    </button>
    <a href="/" class="rl-topnav-logo">
      <span class="rl-the">THE</span>
      <span class="rl-signal">SIGNAL</span>
    </a>
    <div class="rl-mobile-actions">
      ${hasSearch ? `<button class="rl-nav-btn" id="searchToggleMobile" aria-label="Search">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <circle cx="11" cy="11" r="8"></circle>
          <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
        </svg>
      </button>` : ''}
    </div>
  </div>

  <!-- Drawer Overlay -->
  <div class="rl-overlay" id="rlOverlay"></div>

  <!-- Drawer -->
  <div class="rl-drawer" id="rlDrawer">
    <div class="rl-drawer-header">
      <a href="/" class="rl-drawer-logo">
        <span class="rl-the">THE</span>
        <span class="rl-signal">SIGNAL</span>
      </a>
      <button class="rl-drawer-close" id="rlDrawerClose" aria-label="Close menu">✕</button>
    </div>
    <div class="rl-drawer-body">
      <div class="rl-drawer-main" id="rlDrawerMain">
        <div class="rl-menu-item rl-open-sub">
          <span class="rl-menu-item-text">SECTORS</span>
          <span class="rl-menu-item-chevron">›</span>
        </div>
        <a href="/stocks/" class="rl-menu-item">
          <span class="rl-menu-item-text">STOCK PAGES</span>
        </a>
        <a href="/#scorecard" class="rl-menu-item">
          <span class="rl-menu-item-text">SIGNAL SCORECARD</span>
        </a>
        <a href="/hive" class="rl-menu-item">
          <span class="rl-menu-item-text">HIVE</span>
        </a>
        <a href="/signal-vs-the-street" class="rl-menu-item">
          <span class="rl-menu-item-text">SIGNAL VS. STREET</span>
        </a>
        <a href="/pricing" class="rl-menu-item">
          <span class="rl-menu-item-text">SIGNAL PREMIUM</span>
        </a>
        <a href="/pricing" class="rl-drawer-cta">GET PREMIUM ACCESS</a>
      </div>
      <div class="rl-drawer-sub" id="rlDrawerSub">
        <div class="rl-sub-header" id="rlSubBack">
          <span class="rl-sub-back">‹</span>
          <span class="rl-sub-title">SECTORS</span>
        </div>
        <a href="/sector/ai" class="rl-menu-item">
          <span class="rl-menu-item-text">AI</span>
        </a>
        <a href="/sector/cyber" class="rl-menu-item">
          <span class="rl-menu-item-text">CYBER</span>
        </a>
        <a href="/sector/defense" class="rl-menu-item">
          <span class="rl-menu-item-text">DEFENSE</span>
        </a>
        <a href="/sector/space" class="rl-menu-item">
          <span class="rl-menu-item-text">SPACE</span>
        </a>
        <a href="/sector/mega-cap" class="rl-menu-item">
          <span class="rl-menu-item-text">MEGA-CAP</span>
        </a>
        <a href="/sector/quantum" class="rl-menu-item">
          <span class="rl-menu-item-text">QUANTUM</span>
        </a>
        <a href="/sector/ai-power" class="rl-menu-item">
          <span class="rl-menu-item-text">AI POWER</span>
        </a>
        <a href="/sector/etfs" class="rl-menu-item">
          <span class="rl-menu-item-text">ETFS</span>
        </a>
      </div>
    </div>
  </div>
  <!-- ===== END ROCKET LAB NAV ===== -->
`;
}

// Auth container HTML (reused from existing site)
function getAuthContainer() {
  return `<div class="auth-container" id="authContainer">
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
        </div>`;
}

// Find all HTML files recursively
function findHTMLFiles(dir) {
  let results = [];
  const items = fs.readdirSync(dir);
  for (const item of items) {
    const fullPath = path.join(dir, item);
    const stat = fs.statSync(fullPath);
    if (stat.isDirectory()) {
      results = results.concat(findHTMLFiles(fullPath));
    } else if (item.endsWith('.html')) {
      results.push(fullPath);
    }
  }
  return results;
}

const htmlFiles = findHTMLFiles(DIST);
console.log(`Found ${htmlFiles.length} HTML files`);

for (const file of htmlFiles) {
  const relPath = path.relative(DIST, file);
  let html = fs.readFileSync(file, 'utf8');
  let modified = false;

  // 1. Add Barlow Condensed to Google Fonts import
  const fontsRegex = /href="(https:\/\/fonts\.googleapis\.com\/css2\?[^"]+)"/;
  const fontsMatch = html.match(fontsRegex);
  if (fontsMatch) {
    const oldUrl = fontsMatch[1];
    if (!oldUrl.includes('Barlow+Condensed')) {
      // Add Barlow Condensed to the import
      const newUrl = oldUrl.replace(
        'family=',
        'family=Barlow+Condensed:wght@400;500;600;700&family='
      );
      html = html.replace(oldUrl, newUrl);
      modified = true;
      console.log(`  ✅ ${relPath}: Added Barlow Condensed font`);
    }
  }

  // 2. Add nav.css link (before closing </head> or after existing CSS links)
  if (!html.includes('nav.css')) {
    // Insert after the last <link rel="stylesheet"...> or <link...css...>
    const cssLinks = [...html.matchAll(/<link[^>]*rel="stylesheet"[^>]*>/g)];
    if (cssLinks.length > 0) {
      const lastCssLink = cssLinks[cssLinks.length - 1];
      const insertPoint = lastCssLink.index + lastCssLink[0].length;
      html = html.slice(0, insertPoint) + '\n  <link rel="stylesheet" href="/css/nav.css?v=1">' + html.slice(insertPoint);
    }
    modified = true;
  }

  // 3. Add nav.js script (after existing script tags or before </body>)
  if (!html.includes('nav.js')) {
    // Insert before </body>
    const bodyCloseIdx = html.lastIndexOf('</body>');
    if (bodyCloseIdx !== -1) {
      html = html.slice(0, bodyCloseIdx) + '  <script src="/js/nav.js?v=1" defer></script>\n' + html.slice(bodyCloseIdx);
    }
    modified = true;
  }

  // 4. Replace existing nav + drawer OR add new nav
  const hasOldNav = /<nav class="nav">/.test(html);
  const hasOldDrawer = html.includes('id="drawerOverlay"');
  const hasSearchToggle = html.includes('id="searchToggle"');

  if (hasOldNav && hasOldDrawer) {
    // Pages with full nav + drawer (10 pages): remove old nav + drawer, add new system
    // Find the old nav block
    const navStart = html.indexOf('<nav class="nav">');
    // Find the drawer end - look for </nav> then everything through the drawer closing
    // The drawer ends with </div> right before "<!-- Search Overlay -->" or "<!-- Kratos" or the search section
    
    // Strategy: Remove from <nav class="nav"> through the end of the old drawer
    // The old drawer ends before either "<!-- Search Overlay -->" or a <!-- comment or the next major section
    
    // Find the end of the old drawer section
    let navEnd = -1;
    // Look for markers after the drawer
    const searchOverlayIdx = html.indexOf('<!-- Search Overlay -->', navStart);
    const searchSectionIdx = html.indexOf('<div class="search-overlay"', navStart);
    const mainStartIdx = html.indexOf('<main', navStart + 10);
    
    if (searchOverlayIdx !== -1) {
      navEnd = searchOverlayIdx;
    } else if (searchSectionIdx !== -1) {
      navEnd = searchSectionIdx;
    } else {
      navEnd = mainStartIdx;
    }
    
    if (navStart !== -1 && navEnd !== -1) {
      // Also need to handle the search overlay - keep it if it exists
      const searchOverlayEnd = html.indexOf('</div>', html.indexOf('<!-- Search Overlay -->', navEnd)) !== -1 
        ? html.indexOf('</div>', html.indexOf('id="searchResults"', navEnd)) + 100
        : navEnd;
      
      // Extract the existing auth container HTML
      const authContainerMatch = html.substring(navStart, navEnd).match(/<div class="auth-container"[\s\S]*?<\/div>\s*<\/div>\s*<\/div>/);
      
      // Remove old nav + drawer, insert new nav
      const beforeNav = html.substring(0, navStart);
      const afterOldNav = html.substring(navEnd);
      
      const newNavHTML = getNewNavHTML(hasSearchToggle);
      html = beforeNav + newNavHTML + afterOldNav;
      modified = true;
      console.log(`  ✅ ${relPath}: Replaced old nav+drawer with Rocket Lab system`);
    }
  } else if (hasOldNav && !hasOldDrawer) {
    // account/settings - has nav but no drawer. Replace nav with new system
    const navStart = html.indexOf('<nav class="nav">');
    const navEnd = html.indexOf('</nav>', navStart) + 6;
    
    if (navStart !== -1) {
      const beforeNav = html.substring(0, navStart);
      const afterNav = html.substring(navEnd);
      const newNavHTML = getNewNavHTML(false);
      html = beforeNav + newNavHTML + afterNav;
      modified = true;
      console.log(`  ✅ ${relPath}: Replaced simple nav with Rocket Lab system`);
    }
  } else if (file.includes('hive/boardroom')) {
    // Boardroom has its own unique nav - replace it
    const navStart = html.indexOf('<nav class="nav">');
    const navEnd = html.indexOf('</nav>', navStart) + 6;
    
    // Also remove the mobile-menu div that follows
    const mobileMenuRegex = /\s*<div class="mobile-menu"[^>]*>[\s\S]*?<\/div>\s*<\/div>/;
    let endIdx = navEnd;
    const mobileMenuMatch = html.substring(navEnd).match(mobileMenuRegex);
    if (mobileMenuMatch) {
      endIdx = navEnd + mobileMenuMatch[0].length;
    }
    
    const beforeNav = html.substring(0, navStart);
    const afterNav = html.substring(endIdx);
    const newNavHTML = getNewNavHTML(false);
    html = beforeNav + newNavHTML + afterNav;
    modified = true;
    console.log(`  ✅ ${relPath}: Replaced boardroom nav with Rocket Lab system`);
  } else if (file.includes('pricing')) {
    // Pricing has NO nav - add the new system right after <body>
    const bodyIdx = html.indexOf('<body>');
    if (bodyIdx !== -1) {
      const insertPoint = bodyIdx + '<body>'.length;
      const newNavHTML = getNewNavHTML(false);
      html = html.substring(0, insertPoint) + newNavHTML + html.substring(insertPoint);
      modified = true;
      console.log(`  ✅ ${relPath}: Added nav system to pricing page`);
    }
  }

  // 5. Remove old inline drawer script (the one that references hamburgerToggle/drawer)
  const oldScriptRegex = /<script>\s*document\.addEventListener\('DOMContentLoaded',\s*function\(\)\{[\s\S]*?var btn = document\.getElementById\('hamburgerToggle'\);[\s\S]*?\}\);\s*<\/script>/;
  if (oldScriptRegex.test(html)) {
    html = html.replace(oldScriptRegex, '<!-- old drawer script removed -->');
    modified = true;
    console.log(`  ✅ ${relPath}: Removed old inline drawer script`);
  }

  // Also handle the drawer script that uses different format
  const oldScriptRegex2 = /<script>\s*document\.addEventListener\('DOMContentLoaded',\s*function\(\)\s*\{\s*var btn = document\.getElementById\('hamburgerToggle'\)[\s\S]*?\}\);\s*<\/script>/;
  if (oldScriptRegex2.test(html)) {
    html = html.replace(oldScriptRegex2, '<!-- old drawer script removed -->');
    modified = true;
  }

  fs.writeFileSync(file, html);
  if (modified) {
    console.log(`  → ${relPath}: updated`);
  } else {
    console.log(`  — ${relPath}: no changes needed`);
  }
}

console.log('\nDone! All HTML files processed.');
