// build.js — JSON-DRIVEN with proper homepage layout (June 9, 2026)
//
// ARCHITECTURE:
//   _backup_dist/ = FROZEN design-only pages (~50KB index.html with placeholders)
//   articles/posts/*.json = SINGLE SOURCE OF TRUTH for all article data
//   articles/sector-template.html = sector page template
//   build.js reads JSON → generates articles-data blob + article cards → injects into placeholders
//
// HOMEPAGE LAYOUT (30 articles):
//   Hero → Featured Article (1) → Ask Pulse → GRID_1 (4) → Scorecards → GRID_2 (6)
//   → Signal Highlights → Community Trading (Hive) → GRID_3 (8) → Newsletter → GRID_4 (11)
//
// Content pipeline agents ONLY write articles/posts/*.json — never touch _backup_dist/index.html.
// Design agents ONLY edit _backup_dist/index.html — never touch article JSON files.

const fs = require('fs');
const path = require('path');

const ROOT = path.join(__dirname);
const SRC = path.join(ROOT, '_backup_dist');
const DST = path.join(ROOT, 'dist');
const ARTICLE_TEMPLATE = path.join(ROOT, 'articles', 'template.html');
const SECTOR_TEMPLATE = path.join(ROOT, 'articles', 'sector-template.html');
const POSTS_DIR = path.join(ROOT, 'articles', 'posts');
const BUILD_TS = Date.now(); // cache-busting timestamp for images

const SECTORS = {
  ai: 'AI', cyber: 'Cyber', defense: 'Defense',
  space: 'Space', 'mega-cap': 'Mega-Cap', quantum: 'Quantum',
  etfs: 'ETFs', 'ai-power': 'AI Power', fintech: 'FinTech', semiconductors: 'Semiconductors'
};

const HOMEPAGE_LIMIT = 40;

// R2 image CDN base — all /img/ paths in HTML get rewritten to absolute R2 URLs
const R2_IMG_BASE = 'https://pub-4b6ad449790f433c8b0fde9b167147c9.r2.dev';

// ─── Rocket Lab Drawer-Only Navigation Block ───
// Only the drawer — original Signal nav bar stays unchanged
const ROCKET_DRAWER = `  <!-- Rocket Lab-Style Drawer -->
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
        <a href="/pricing" class="drawer-link">SIGNAL PREMIUM</a>
        <a href="/pricing" class="drawer-cta">GET PREMIUM ACCESS</a>
      </div>
      <div class="drawer-sub" id="drawerSub">
        <div class="sub-header" onclick="closeSubDrawer()">
          <span class="sub-back">&#8249;</span>
          <span class="sub-title">SECTORS</span>
        </div>
        <a href="/sector/ai/" class="drawer-link">AI</a>
        <a href="/sector/cyber/" class="drawer-link">CYBER</a>
        <a href="/sector/defense/" class="drawer-link">DEFENSE</a>
        <a href="/sector/space/" class="drawer-link">SPACE</a>
        <a href="/sector/mega-cap/" class="drawer-link">MEGA-CAP</a>
        <a href="/sector/quantum/" class="drawer-link">QUANTUM</a>
        <a href="/sector/ai-power/" class="drawer-link">AI POWER</a>
        <a href="/sector/fintech/" class="drawer-link">FINTECH</a>
        <a href="/sector/etfs/" class="drawer-link">ETFS</a>
      </div>
    </div>
  </div>`;

// ─── Inject Rocket Lab Drawer into generated HTML (keeps original nav bar) ───
function injectRocketNav(html) {
  // 1. Add Barlow Condensed to Google Fonts URL if not already present
  if (!html.includes('Barlow+Condensed')) {
    html = html.replace(
      /fonts\.googleapis\.com\/css2\?[^"']+/g,
      (match) => match + '&family=Barlow+Condensed:wght@400;500;600;700'
    );
  }

  // 2. Add nav.css stylesheet before </head> if not already present
  if (!html.includes('/css/nav.css')) {
    html = html.replace('</head>', '  <link rel="stylesheet" href="/css/nav.css?v=1">\n</head>');
  }

  // 2b. Add nav.js script before </head> if not already present
  if (!html.includes('/js/nav.js')) {
    html = html.replace('</head>', '  <script src="/js/nav.js?v=1" defer></script>\n</head>');
  }

  // 3. Replace DRAWER placeholder with Rocket Lab drawer
  const drawerPlaceholder = '<!-- DRAWER -->';
  const drawerIdx = html.indexOf(drawerPlaceholder);
  if (drawerIdx !== -1) {
    html = html.replace(drawerPlaceholder, ROCKET_DRAWER);
  }

  // 4. Remove old inline DOMContentLoaded drawer scripts (hamburger-based)
  html = html.replace(/\s*<script>\s*document\.addEventListener\('DOMContentLoaded',\s*function\(\)\{[\s\S]*?hamburgerToggle[\s\S]*?\}\);\s*<\/script>/g, '');
  // Also handle scripts with 'DOMContentLoaded' that reference drawer logic
  html = html.replace(/\s*<script>\s*\/\/ ── Sector[^<]*<\/script>/g, '');
  // Handle the sector template's drawer script
  html = html.replace(/\s*<script>\s*document\.addEventListener\('DOMContentLoaded',\s*function\(\)\{[\s\S]*?drawerSectorsBtn[\s\S]*?\}\);\s*<\/script>/g, '');

  return html;
}

// ─── Monthly Stock Picks Builder ───
const MONTHS_SHORT = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];

function buildMonthlyPicks() {
  const picksDir = path.join(ROOT, 'articles', 'monthly-picks');
  if (!fs.existsSync(picksDir)) return '';

  const files = fs.readdirSync(picksDir)
    .filter(f => f.endsWith('.json'))
    .sort()
    .reverse();

  if (files.length === 0) return '';

  const latest = JSON.parse(fs.readFileSync(path.join(picksDir, files[0]), 'utf8'));

  if (!latest.youtubeEmbed) return '';

  const monthDisplay = MONTHS_SHORT[latest.month - 1] + ' ' + latest.year;

  return `
    <section class="monthly-picks-section">
      <div class="monthly-picks-bg"></div>
      <div class="monthly-picks-inner">
        <div class="monthly-picks-header">
          <div class="monthly-picks-badge">
            <span class="monthly-picks-badge-dot"></span>
            Monthly Picks
          </div>
          <h2 class="monthly-picks-title">Our <span class="monthly-picks-gradient">Top Picks</span> for <span class="monthly-picks-month">${monthDisplay}</span></h2>
          <p class="monthly-picks-desc">${escapeHtml(latest.description || 'This month we\'re bullish on AI infrastructure, defense contracts, and space expansion. Here are our 6 top stock picks for July 2025.')}</p>
        </div>
        <div class="monthly-picks-video-full">
          <div class="monthly-picks-video-wrapper">
            <iframe src="${latest.youtubeEmbed}" title="${escapeAttr(latest.youtubeTitle || latest.title)}"
              frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
              allowfullscreen loading="lazy"></iframe>
          </div>
          <div class="monthly-picks-video-caption">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="currentColor"><path d="M8 5v14l11-7z"/></svg>
            Watch the full breakdown
          </div>
        </div>
      </div>
    </section>`;
}

// ─── 1. Copy frozen assets ───
console.log('📦 Copying frozen assets from _backup_dist/...');
if (!fs.existsSync(SRC)) {
  console.error('ERROR: _backup_dist/ not found!');
  process.exit(1);
}
fs.rmSync(DST, { recursive: true, force: true });
fs.cpSync(SRC, DST, { recursive: true });

// GUARD: Abort if homepage is suspiciously small (< 35KB = stripped design)
const htmlSize = fs.statSync(path.join(DST, 'index.html')).size;
if (htmlSize < 35000) {
  console.error(`⛔ FATAL: index.html is ${htmlSize} bytes — expected ~40,000+.`);
  console.error('   The frozen design may be corrupted.');
  process.exit(1);
}
console.log(`  ✅ ${htmlSize} bytes design → dist/`);

// ─── 1.5. Copy article images (root-level only — article images served from R2) ───
// Article images under img/articles/ are served directly from R2 CDN.
// We skip copying them to dist/ (and remove if present from _backup_dist/) to keep deployment small.
const imgDir = path.join(ROOT, 'public', 'img');
const distImgDir = path.join(DST, 'img');
if (fs.existsSync(imgDir)) {
  // Copy only root-level img files (skip articles/ subdirectory — served from R2)
  fs.mkdirSync(distImgDir, { recursive: true });
  const entries = fs.readdirSync(imgDir, { withFileTypes: true });
  let copied = 0;
  for (const entry of entries) {
    if (entry.isDirectory()) continue; // skip articles/ subdir
    fs.copyFileSync(path.join(imgDir, entry.name), path.join(distImgDir, entry.name));
    copied++;
  }
  console.log(`  ✅ ${copied} root image files → dist/img/ (articles/ served from R2)`);
}
// Remove dist/img/articles/ if it was copied from _backup_dist/ (served from R2 instead)
const distArticlesImg = path.join(DST, 'img', 'articles');
if (fs.existsSync(distArticlesImg)) {
  fs.rmSync(distArticlesImg, { recursive: true, force: true });
  console.log('  🗑  Removed dist/img/articles/ (served from R2 CDN)');
}

// ─── 1.5.5. Copy article audio ───
const audioDir = path.join(ROOT, 'public', 'audio');
const distAudioDir = path.join(DST, 'audio');
if (fs.existsSync(audioDir)) {
  fs.cpSync(audioDir, distAudioDir, { recursive: true });
  console.log(`  ✅ ${countFiles(distAudioDir)} audio files → dist/audio/`);
}

// ─── 1.5.6. Check for missing TTS audio ───
(function checkMissingAudio() {
  if (!fs.existsSync(POSTS_DIR)) return;
  const jsonFiles = fs.readdirSync(POSTS_DIR).filter(f => f.endsWith('.json'));
  const missing = [];
  for (const file of jsonFiles) {
    try {
      const article = JSON.parse(fs.readFileSync(path.join(POSTS_DIR, file), 'utf8'));
      if (!article.slug) continue;
      const mp3Path = path.join(ROOT, 'public', 'audio', `${article.slug}.mp3`);
      if (!fs.existsSync(mp3Path)) {
        missing.push(article.slug);
      }
    } catch {}
  }
  if (missing.length > 0) {
    console.log(`  ⚠️  ${missing.length} articles missing TTS audio. Generate with:`);
    for (const slug of missing) {
      console.log(`     python3 scripts/regenerate-tts.py ${slug}`);
    }
  }
})();

// ─── 1.6. Build stock pages ───
console.log('📊 Building stock pages...');
try {
  require('./scripts/build-stock-page.js');
  // Copy stock pages into dist/stocks/ for readthesignal.net hosting
  const stockSrc = path.join(DST, 'stock', 'stock');
  const stockDst = path.join(DST, 'stocks');
  if (fs.existsSync(stockSrc)) {
    fs.cpSync(stockSrc, stockDst, { recursive: true });
    console.log('  ✅ Stock pages copied to dist/stocks/');
  }
  // Copy stock CSS/JS
  const stockCssSrc = path.join(DST, 'stock', 'css');
  const stockCssDst = path.join(DST, 'css');
  if (fs.existsSync(stockCssSrc)) fs.cpSync(stockCssSrc, stockCssDst, { recursive: true });
  const stockJsSrc = path.join(DST, 'stock', 'js');
  const stockJsDst = path.join(DST, 'js');
  if (fs.existsSync(stockJsSrc)) fs.cpSync(stockJsSrc, stockJsDst, { recursive: true });
  // Build stocks index page
  require('./scripts/build-stocks-index.js');
} catch (e) {
  console.error('  ⚠️  Stock pages build failed:', e.message);
}

// ─── 2. Load all articles from JSON files ───
const articles = loadArticles();
console.log(`📝 ${articles.length} articles loaded from articles/posts/*.json`);

// ─── 3. Generate articles-data JSON blob ───
const articlesJson = JSON.stringify(articles);
console.log(`  📄 articles-data: ${articlesJson.length} bytes`);

// ─── 4. Sort by date desc, split homepage vs sector ───
articles.sort((a, b) => (b.date || '').localeCompare(a.date || ''));

const homepage = articles.slice(0, HOMEPAGE_LIMIT);
const sectorArticles = articles.slice(HOMEPAGE_LIMIT);

// Homepage splits
const featuredArticle = homepage.slice(0, 1);   // 1 featured
const grid1 = homepage.slice(1, 7);              // 6 articles
const grid2 = homepage.slice(7, 13);             // 6 articles
const grid3 = homepage.slice(13, 19);            // 6 articles
const grid4 = homepage.slice(19, 40);            // 21 remaining

console.log(`  📰 Homepage: ${homepage.length} total (1 featured + ${grid1.length} + ${grid2.length} + ${grid3.length} + ${grid4.length})`);
console.log(`  📂 Sector pages: ${sectorArticles.length} articles`);

// ─── 5. Generate card HTML ───
const featuredHtml = featuredArticle.map(a => featuredCard(a)).join('\n');
const grid1Html = grid1.map(a => articleCard(a)).join('\n');
const grid2Html = grid2.map(a => articleCard(a)).join('\n');
const grid3Html = grid3.map(a => articleCard(a)).join('\n');
const grid4Html = grid4.map(a => articleCard(a)).join('\n');

// ─── 6. Inject into placeholders ───
let indexHtml = fs.readFileSync(path.join(DST, 'index.html'), 'utf8');

indexHtml = indexHtml.replace('<!-- ARTICLES_DATA_JSON -->',
  `<script id="articles-data" type="application/json">${articlesJson}</script>`);

indexHtml = indexHtml.replace('<!-- FEATURED_ARTICLE -->',
  `<section class="featured-hero">\n  <div class="article-grid">\n${featuredHtml}\n  </div>\n</section>`);

indexHtml = indexHtml.replace('<!-- GRID_1 -->',
  `<section class="feed feed-continued">\n  <div class="article-grid">\n${grid1Html}\n  </div>\n</section>`);

indexHtml = indexHtml.replace('<!-- GRID_2 -->',
  `<section class="feed feed-continued">\n  <div class="article-grid">\n${grid2Html}\n  </div>\n</section>`);

indexHtml = indexHtml.replace('<!-- GRID_3 -->',
  `<section class="feed feed-continued">\n  <div class="article-grid">\n${grid3Html}\n  </div>\n</section>`);

indexHtml = indexHtml.replace('<!-- GRID_4 -->',
  `<section class="feed feed-continued">\n  <div class="article-grid">\n${grid4Html}\n  </div>\n</section>`);

// Inject Rocket Lab navigation into homepage
indexHtml = injectRocketNav(indexHtml);

fs.writeFileSync(path.join(DST, 'index.html'), indexHtml);

const finalSize = fs.statSync(path.join(DST, 'index.html')).size;
console.log(`  ✅ Homepage built: ${finalSize} bytes`);

// GUARD: Abort if homepage is suspiciously small (< 350KB with 40 articles)
if (finalSize < 350000) {
  console.error(`⛔ FATAL: Built index.html is ${finalSize} bytes — expected ~400,000+.`);
  console.error('   Article generation may have failed. Check articles/posts/*.json.');
  console.error('   Recovery: npx vercel promote the-signal-nphmhgo0f-beachsquadlas-projects.vercel.app');
  process.exit(1);
}

// ─── 7. Generate article pages ───
const template = fs.existsSync(ARTICLE_TEMPLATE)
  ? fs.readFileSync(ARTICLE_TEMPLATE, 'utf8')
  : null;

if (!template) {
  console.log('⚠️  No template found at articles/template.html — skipping article pages');
} else {
  let generated = 0;
  for (const article of articles) {
    try {
      const slug = article.slug;
      if (!slug) continue;

      const date = article.date ? article.date.slice(0, 10) : '';
      const readTime = (article.meta && article.meta.estimatedReadTime) || '1 min read';
      const rawSrc = (article.image && article.image.src) || '/img/articles/_default.jpg';
      const imageSrc = (rawSrc.startsWith('/') ? rawSrc : '/' + rawSrc) + '?v=' + BUILD_TS;
      const imageCaption = (article.image && article.image.caption) || article.title || '';
      const sector = article.sector || 'ai';
      const sectorName = SECTORS[sector] || sector.toUpperCase();
      const subtitle = article.subtitle ? `<p class="article-subtitle">${article.subtitle}</p>` : '';
      const imageHtml = `<div class="article-image"><img src="${imageSrc}" alt="${escapeHtml(imageCaption)}" width="1200" height="675"></div>`;

      let tagsHtml = '';
      const tags = article.tags || [];
      if (tags.length > 0) {
        tagsHtml = '<div class="article-tags">' + tags.map(t => `<span class="tag">${escapeHtml(t)}</span>`).join('') + '</div>';
      }

      let linksHtml = '';
      const links = article.links || [];
      if (links.length > 0) {
        linksHtml = '<div class="article-links"><h4>📎 Sources &amp; References</h4><ul>' +
          links.map(l => `<li><a href="${escapeAttr(l.url)}" target="_blank" rel="noopener">${escapeHtml(l.label || l.url)}</a></li>`).join('') +
          '</ul></div>';
      }

      let bodyHtml = article.bodyHtml || '';
      bodyHtml = bodyHtml.replace(/\\"/g, '"');
      bodyHtml = bodyHtml.replace(/\\n/g, '\n');
      // Rewrite /ticker/SYMBOL links to stock pages (single + double quotes)
      bodyHtml = bodyHtml.replace(/href=['"]\/ticker\/([A-Z]+)['"]/g, 'href="https://signal-stock-pi.vercel.app/stock/$1/"');

      let html = template
        .replace(/{{TITLE}}/g, article.title || '')
        .replace(/{{SUMMARY}}/g, (article.summary || '').replace(/"/g, '&quot;'))
        .replace(/{{SLUG}}/g, slug)
        .replace(/{{TICKER}}/g, article.ticker || '')
        .replace(/{{SECTOR}}/g, sector)
        .replace(/{{SECTOR_UC}}/g, sectorName)
        .replace(/{{SUBTITLE_HTML}}/g, subtitle)
        .replace(/{{DATE}}/g, article.date || '')
        .replace(/{{DATE_FORMATTED}}/g, formatDate(date))
        .replace(/{{READ_TIME}}/g, readTime)
        .replace(/{{IMAGE_SRC}}/g, imageSrc)
        .replace(/{{IMAGE_HTML}}/g, imageHtml)
        .replace(/{{BODY}}/g, bodyHtml)
        .replace(/{{TAGS_HTML}}/g, tagsHtml)
        .replace(/{{LINKS_HTML}}/g, linksHtml)
        .replace(/{{RELATED_ARTICLES}}/g, pickRelated(articles, slug, 4))
        .replace('<!-- ARTICLES_DATA_JSON -->',
          `<script id="articles-data" type="application/json">${articlesJson}</script>`)
        .replace(/\{\{[A-Z_]+\}\}/g, '');

      // Inject Rocket Lab navigation
      html = injectRocketNav(html);

      const outDir = path.join(DST, 'article', slug);
      fs.mkdirSync(outDir, { recursive: true });
      fs.writeFileSync(path.join(outDir, 'index.html'), html);
      generated++;
    } catch (e) {
      console.error(`  ⚠️  Error generating ${article.slug || '?'}: ${e.message}`);
    }
  }
  console.log(`  ✅ ${generated} article pages generated`);
}

// ─── 7.5. Generate /articles/index.json for search fallback ───
const articlesIndexDir = path.join(DST, 'articles');
fs.mkdirSync(articlesIndexDir, { recursive: true });
fs.writeFileSync(path.join(articlesIndexDir, 'index.json'), articlesJson);
const indexJsonKb = Math.round(articlesJson.length / 1024);
console.log(`  📄 /articles/index.json written (${indexJsonKb}KB) — search fallback ready`);

// ─── 8. Generate sector pages ───
const sectorTemplate = fs.existsSync(SECTOR_TEMPLATE)
  ? fs.readFileSync(SECTOR_TEMPLATE, 'utf8')
  : null;

if (!sectorTemplate) {
  console.log('⚠️  No sector template — skipping sector pages');
} else {
  // Group articles by sector (ALL articles — homepage AND archive)
  const bySector = {};
  for (const a of articles) {
    const s = a.sector || 'other';
    if (!bySector[s]) bySector[s] = [];
    bySector[s].push(a);
  }

  const SECTOR_PAGE_SIZE = 12;
  let sectorCount = 0;
  for (const [sector, arts] of Object.entries(bySector)) {
    const sectorName = SECTORS[sector] || sector.toUpperCase();
    const visible = arts.slice(0, SECTOR_PAGE_SIZE).map(a => articleCard(a)).join('\n');
    const hidden = arts.slice(SECTOR_PAGE_SIZE).map(a => articleCard(a).replace('class="article-card"', 'class="article-card sector-hidden"')).join('\n');
    const loadMoreBtn = arts.length > SECTOR_PAGE_SIZE
      ? `\n<button class="sector-load-more" id="sectorLoadMore" onclick="showMoreSector()"><span class="sector-load-more-text">Load More Articles</span><span class="sector-load-more-count">${arts.length - SECTOR_PAGE_SIZE} remaining</span></button>`
      : '';
    const cards = visible + '\n' + hidden + loadMoreBtn;
    
    let html = sectorTemplate
      .replace(/{{SECTOR}}/g, sector)
      .replace(/{{SECTOR_NAME}}/g, sectorName)
      .replace('{{ARTICLE_CARDS}}', cards)
      .replace('<!-- ARTICLES_DATA_JSON -->',
        `<script id="articles-data" type="application/json">${articlesJson}</script>`);
    
    // Inject Rocket Lab navigation
    html = injectRocketNav(html);
    
    const outDir = path.join(DST, 'sector', sector);
    fs.mkdirSync(outDir, { recursive: true });
    fs.writeFileSync(path.join(outDir, 'index.html'), html);
    sectorCount++;
    console.log(`  📂 /sector/${sector}/ — ${arts.length} articles`);
  }

  // Also create empty sector pages for any defined sector with no articles
  for (const [sector, sectorName] of Object.entries(SECTORS)) {
    if (bySector[sector]) continue; // already built
    let html = sectorTemplate
      .replace(/{{SECTOR}}/g, sector)
      .replace(/{{SECTOR_NAME}}/g, sectorName)
      .replace('{{ARTICLE_CARDS}}', '<p class="sector-empty">Articles coming soon.</p>')
      .replace('<!-- ARTICLES_DATA_JSON -->',
        `<script id="articles-data" type="application/json">${articlesJson}</script>`);
    
    // Inject Rocket Lab navigation
    html = injectRocketNav(html);
    
    const outDir = path.join(DST, 'sector', sector);
    fs.mkdirSync(outDir, { recursive: true });
    fs.writeFileSync(outDir + '/index.html', html);
    sectorCount++;
    console.log(`  📂 /sector/${sector}/ — 0 articles (empty page)`);
  }
  console.log(`  ✅ ${sectorCount} sector pages generated`);
}

// ─── 8.5. Inject Trending Stocks list from live prices ───
const pricesPath2 = path.join(ROOT, 'data', 'prices.json');
const prices = fs.existsSync(pricesPath2) ? JSON.parse(fs.readFileSync(pricesPath2, 'utf8')) : {};
const trendingTickers = ['NVDA', 'AVGO', 'TSLA', 'MSFT', 'AMZN', 'PLTR', 'META'];
let trendingHtml = '';
for (const sym of trendingTickers) {
  const p = prices[sym] || {};
  const priceVal = p.price != null ? p.price : null;
  const chgPct = p.changePercent != null ? p.changePercent : null;
  const priceStr = priceVal != null ? '$' + priceVal.toFixed(2) : '—';
  const chgStr = chgPct != null ? (chgPct >= 0 ? '+' : '') + chgPct.toFixed(2) + '%' : '—';
  const dirClass = chgPct != null ? (chgPct >= 0 ? 'up' : 'down') : '';
  trendingHtml += `<a href="/stocks/${sym}/" class="trending-row" data-ticker="${sym}">
    <div class="trending-row-left">
      <span class="trending-row-ticker">${sym}</span>
      <span class="trending-row-name">${p.name || sym}</span>
    </div>
    <div class="trending-row-right">
      <span class="trending-row-price" data-price="${sym}">${priceStr}</span>
      <span class="trending-row-change ${dirClass}" data-change="${sym}">${chgStr}</span>
    </div>
  </a>`;
}
indexHtml = indexHtml.replace('TRENDING_STOCKS_PLACEHOLDER', trendingHtml);

// ─── 8.6. Inject Signal Highlights cards from live data ───
const highlightsPath = path.join(ROOT, 'data', 'signal-highlights.json');
if (fs.existsSync(highlightsPath)) {
  const highlights = JSON.parse(fs.readFileSync(highlightsPath, 'utf8'));
  let cardsHtml = '';
  for (const h of highlights) {
    const dir = h.changeDirection || (h.changePercent >= 0 ? 'up' : 'down');
    const buys = h.analyst.buys || 0;
    const holds = h.analyst.holds || 0;
    const sells = h.analyst.sells || 0;
    const total = buys + holds + sells || 1;
    const buyPct = Math.round(buys / total * 100);
    const holdPct = Math.round(holds / total * 100);

    cardsHtml += `<a href="/stocks/${h.ticker}/" class="detail-card-link"><div class="detail-card-accent"></div><div class="detail-card-inner">` +
      `<div class="detail-header"><div class="detail-header-left">` +
      `<div class="detail-badge">Signal Highlight</div>` +
      `<div class="detail-ticker">${h.ticker}</div>` +
      `<div class="detail-name">${h.name}</div></div>` +
      `<div class="detail-header-right">` +
      `<div class="detail-price">$${h.currentPrice}</div>` +
      `<div class="detail-change ${dir}">${h.changePercent >= 0 ? '+' : ''}${h.changePercent}%</div>` +
      `</div></div>` +
      // Fair Value
      `<div class="detail-card-section"><div class="detail-section-title">Fair Value</div>` +
      `<div class="detail-fair-value"><div class="detail-fv-status">` +
      `<span class="detail-fv-badge">${h.fairValue.status}</span></div>` +
      `<div class="detail-fv-rows">` +
      `<div class="detail-fv-row"><span class="detail-fv-label">Fair Value</span><span class="detail-fv-val">$${h.fairValue.price}</span></div>` +
      `<div class="detail-fv-row"><span class="detail-fv-label">Current Price</span><span class="detail-fv-val">$${h.currentPrice}</span></div>` +
      `<div class="detail-fv-row"><span class="detail-fv-label">Upside</span><span class="detail-fv-val detail-fv-upside">${h.fairValue.upside}</span></div>` +
      `</div></div></div>` +
      // Earnings
      `<div class="detail-card-section"><div class="detail-section-title">Earnings</div>` +
      `<div class="detail-earnings">` +
      `<div class="detail-earn-row"><span class="detail-earn-label">Revenue (TTM)</span><span class="detail-earn-val">${h.earnings.revTtm}</span></div>` +
      `<div class="detail-earn-row"><span class="detail-earn-label">Revenue Growth</span><span class="detail-earn-val detail-revision-up">${h.earnings.revGrowth}</span></div>` +
      `<div class="detail-earn-row"><span class="detail-earn-label">Net Income</span><span class="detail-earn-val">${h.earnings.netIncome}</span></div>` +
      `</div></div>` +
      // Analyst
      `<div class="detail-card-section detail-section-last"><div class="detail-section-title">Analyst Ratings</div>` +
      `<div class="detail-analyst"><div class="detail-ana-top">` +
      `<span class="detail-consensus-badge">${h.analyst.consensus}</span>` +
      `<span class="detail-ana-target">Target <strong>$${h.analyst.target}</strong></span></div>` +
      `<div class="detail-rating-bar">` +
      `<div class="detail-rating-seg detail-rating-buy" style="width:${buyPct}%"></div>` +
      `<div class="detail-rating-seg detail-rating-hold" style="width:${holdPct}%"></div>` +
      `</div><div class="detail-rating-legend">` +
      `<span class="detail-legend-item"><span class="detail-rating-dot detail-dot-buy"></span>Buy ${buys}</span>` +
      `<span class="detail-legend-item"><span class="detail-rating-dot detail-dot-hold"></span>Hold ${holds}</span>` +
      `</div></div></div></div></a>`;
  }
  indexHtml = indexHtml.replace('SIGNAL_HIGHLIGHTS_PLACEHOLDER', cardsHtml);

  // ─── 8.7. Inject Monthly Stock Picks ───
  const monthlyPicksHtml = buildMonthlyPicks();
  if (monthlyPicksHtml) {
    indexHtml = indexHtml.replace('<!-- MONTHLY_PICKS -->', monthlyPicksHtml);
    console.log('  ✅ Monthly Stock Picks section injected');
  } else {
    console.log('  ⚠️  No monthly picks data found — skipping');
  }

  fs.writeFileSync(path.join(DST, 'index.html'), indexHtml);
  console.log(`  ✅ ${highlights.length} Signal Highlight cards injected`);
} else {
  console.log('  ⚠️  No data/signal-highlights.json — run scripts/refresh-signal-highlights.py first');
}

// ─── 9. Copy API serverless functions ───
// Clean dist/api/ first to remove stale files from previous builds
const apiDir = path.join(ROOT, 'api');
const distApiDir = path.join(DST, 'api');
if (fs.existsSync(distApiDir)) {
  fs.rmSync(distApiDir, { recursive: true, force: true });
}
if (fs.existsSync(apiDir)) {
  fs.mkdirSync(distApiDir, { recursive: true });
  const apiFiles = fs.readdirSync(apiDir);
  for (const f of apiFiles) {
    const srcPath = path.join(apiDir, f);
    const dstPath = path.join(distApiDir, f);
    if (fs.statSync(srcPath).isDirectory()) {
      fs.cpSync(srcPath, dstPath, { recursive: true });
    } else {
      fs.copyFileSync(srcPath, dstPath);
    }
  }
  console.log(`  ✅ ${apiFiles.length} API items copied`);
}

// ─── 9.5. Copy article JSON data for Pulse AI ───
// Pulse AI (api/pulse.mjs) reads articles/posts/*.json at runtime to build
// article context for its answers. Without these files in dist/, the
// serverless function finds an empty directory and returns no Signal context.
const postsSrc = path.join(ROOT, 'articles', 'posts');
const postsDst = path.join(DST, 'articles', 'posts');
if (fs.existsSync(postsSrc)) {
  fs.mkdirSync(postsDst, { recursive: true });
  const jsonFiles = fs.readdirSync(postsSrc).filter(f => f.endsWith('.json'));
  for (const f of jsonFiles) {
    fs.copyFileSync(path.join(postsSrc, f), path.join(postsDst, f));
  }
  console.log(`  ✅ ${jsonFiles.length} article JSON files → dist/articles/posts/`);
} else {
  console.log('  ⚠️  No articles/posts/ directory found — Pulse AI will have no article context');
}

// ─── 9.6. Generate article data module for Pulse AI (bundled with function) ───
// Vercel isolates function code from static assets, so filesystem reads of
// articles/posts/*.json don't work at runtime. Instead we compile the article
// metadata into a JS module that the function imports directly.
(function generateArticlesDataModule() {
  const postsDir = path.join(ROOT, 'articles', 'posts');
  const outputPath = path.join(DST, 'api', 'articles-data.mjs');
  if (!fs.existsSync(postsDir)) {
    console.log('  ⚠️  No articles/posts/ — skipping articles-data.mjs');
    return;
  }
  const articles = [];
  for (const f of fs.readdirSync(postsDir).filter(f => f.endsWith('.json'))) {
    try {
      const a = JSON.parse(fs.readFileSync(path.join(postsDir, f), 'utf8'));
      articles.push({
        title: a.title || '',
        slug: a.slug || f.replace('.json', ''),
        ticker: (a.ticker || '').toUpperCase(),
        sector: a.sector || '',
        date: a.date || '',
        summary: (a.summary || '').slice(0, 500)
      });
    } catch (e) { /* skip corrupt */ }
  }
  articles.sort((a, b) => new Date(b.date) - new Date(a.date));
  const moduleContent = '// Auto-generated by build.js — do not edit\n' +
    '// Contains article metadata for Pulse AI\n' +
    `const ARTICLES = ${JSON.stringify(articles, null, 2)};\n` +
    'export default ARTICLES;\n';
  fs.writeFileSync(outputPath, moduleContent, 'utf8');
  console.log(`  ✅ articles-data.mjs generated with ${articles.length} articles → dist/api/`);

  // Also inline a compact article index into api/pulse.mjs for Vercel
  // Inline replaces the placeholder: const articles = [];
  const pulsePath = path.join(DST, 'api', 'pulse.mjs');
  if (fs.existsSync(pulsePath)) {
    let pulseContent = fs.readFileSync(pulsePath, 'utf8');
    const compactArticles = articles.map(a => ({
      t: a.ticker, s: a.slug,
      u: a.title.slice(0, 60),
      c: a.sector, d: (a.date || '').slice(0, 10)
    }));
    const dataJSON = JSON.stringify(compactArticles);
    const placeholder = 'const articles = [];';
    const placeholderLine = pulseContent.indexOf(placeholder);
    if (placeholderLine !== -1) {
      const indent = pulseContent.slice(0, placeholderLine).split('\n').pop();
      const inlineData = `const articles = ${dataJSON};`;
      pulseContent = pulseContent.replace(placeholder, inlineData);
      fs.writeFileSync(pulsePath, pulseContent, 'utf8');
      const sizeKB = Math.round(Buffer.byteLength(dataJSON, 'utf8') / 1024);
      console.log(`  ✅ Pulse article index inlined (${sizeKB}KB)`);
    } else {
      console.log('  ⚠️  Pulse placeholder not found in api/pulse.mjs — skipping inline');
    }
  }
})();

// ─── 10. Rewrite all /img/ paths in HTML to absolute R2 URLs ───
// This ensures img/articles/* images are served from R2 CDN, bypassing
// Vercel's SPA catch-all routing that would otherwise 404 subdirectory images.
console.log('🔄 Rewriting image paths to R2 CDN...');
(function rewriteImagePaths() {
  function walkHtml(dir) {
    const entries = fs.readdirSync(dir, { withFileTypes: true });
    for (const entry of entries) {
      const full = path.join(dir, entry.name);
      if (entry.isDirectory()) {
        walkHtml(full);
      } else if (entry.name.endsWith('.html')) {
        let content = fs.readFileSync(full, 'utf8');
        // Replace "/img/ with R2 absolute URL — catches both HTML attributes (src="/img/)
        // and JSON strings inside <script id="articles-data"> blocks
        // 1) Local "/img/" paths (HTML src="/img/..." and JSON strings)
        let rewritten = content.replace(/"\/img\//g, '"' + R2_IMG_BASE + '/img/');
        // 2) Absolute readthesignal.net URLs (stock page news cards, etc.)
        rewritten = rewritten.replace(/https?:\/\/readthesignal\.net\/img\//gi, R2_IMG_BASE + '/img/');
        if (rewritten !== content) {
          fs.writeFileSync(full, rewritten);
        }
      }
    }
  }
  walkHtml(DST);
  console.log('  ✅ All /img/ paths rewritten to R2 CDN (local + absolute URLs)');
})();

// ─── Summary ───
const totalFiles = countFiles(DST);
console.log(`✅ Build complete — ${totalFiles} files in dist/`);

// ─── Article loader ───
function loadArticles() {
  const articles = [];
  if (!fs.existsSync(POSTS_DIR)) {
    console.error('ERROR: articles/posts/ directory not found!');
    process.exit(1);
  }

  const jsonFiles = fs.readdirSync(POSTS_DIR).filter(f => f.endsWith('.json'));
  for (const file of jsonFiles) {
    try {
      const article = JSON.parse(fs.readFileSync(path.join(POSTS_DIR, file), 'utf8'));
      if (article.slug && article.title && article.bodyHtml) {
        articles.push(article);
      } else {
        console.log(`  ⚠️  Skipping ${file}: missing slug/title/bodyHtml`);
      }
    } catch (e) {
      console.log(`  ⚠️  Skipping ${file}: ${e.message}`);
    }
  }
  return articles;
}

// ─── Card generators ───
function featuredCard(a) {
  const img = ((a.image && a.image.src) || '/img/articles/_default.jpg') + '?v=' + BUILD_TS;
  const readTime = (a.meta && a.meta.estimatedReadTime) || '1 min read';
  const dateStr = formatDate((a.date || '').slice(0, 10));

  return `<a href="/article/${a.slug}" class="article-card featured-card">
    <div class="card-image"><img src="${img}" alt="${escapeAttr(a.title || '')}" loading="eager" decoding="async" width="1200" height="675"></div>
    <div class="card-body">
    <div class="card-top">
      <span class="ticker-badge">${escapeHtml(a.ticker || '')}</span>
    </div>
    <h3 class="card-title">${escapeHtml(a.title || '')}</h3>
    <p class="card-summary">${escapeHtml((a.summary || '').substring(0, 280))}${(a.summary || '').length > 280 ? '...' : ''}</p>
    <div class="card-meta"><span>${dateStr}</span><span>${readTime}</span></div>
    </div></a>`;
}

function articleCard(a) {
  const img = ((a.image && a.image.src) || '/img/articles/_default.jpg') + '?v=' + BUILD_TS;
  const readTime = (a.meta && a.meta.estimatedReadTime) || '1 min read';
  const dateStr = formatDate((a.date || '').slice(0, 10));
  const summary = (a.summary || '').substring(0, 160);
  const ellipsis = (a.summary || '').length > 160 ? '...' : '';

  return `<a href="/article/${a.slug}" class="article-card">
    <div class="card-image"><img src="${img}" alt="${escapeAttr(a.title || '')}" loading="lazy" decoding="async" width="1200" height="675"></div>
    <div class="card-body">
    <div class="card-top">
      <span class="ticker-badge">${escapeHtml(a.ticker || '')}</span>
    </div>
    <h3 class="card-title">${escapeHtml(a.title || '')}</h3>
    <p class="card-summary">${escapeHtml(summary)}${ellipsis}</p>
    <div class="card-meta"><span>${dateStr}</span><span>${readTime}</span></div>
    </div></a>`;
}

// ─── Helpers ───
function pickRelated(allArticles, currentSlug, count) {
  const others = allArticles.filter(a => a.slug !== currentSlug);
  const shuffled = others.sort(() => 0.5 - Math.random());
  const picked = shuffled.slice(0, count);
  return picked.map(a => {
    const img = ((a.image && a.image.src) || '/img/articles/_default.jpg') + '?v=' + BUILD_TS;
    return `<a href="/article/${a.slug}" class="related-card">
      <div class="card-image"><img src="${img}" alt="${escapeAttr(a.title || '')}" loading="lazy" decoding="async" width="1200" height="675"></div>
      <div class="card-body">
        <h3 class="card-title">${escapeHtml(a.title || '')}</h3>
      </div>
    </a>`;
  }).join('\n');
}

function countFiles(dir) {
  let count = 0;
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    if (entry.isDirectory()) count += countFiles(path.join(dir, entry.name));
    else count++;
  }
  return count;
}

function escapeHtml(str) {
  return (str || '').replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
}

function escapeAttr(str) {
  return (str || '').replace(/&/g, '&amp;').replace(/"/g, '&quot;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
}

function formatDate(d) {
  if (!d) return '';
  const months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
  try {
    const dt = new Date(d);
    return `${months[dt.getMonth()]} ${dt.getDate()}, ${dt.getFullYear()}`;
  } catch { return d; }
}

// ─── Copy data/ directory for static JSON assets ───
const dataDir = path.join(ROOT, 'data');
const distDataDir = path.join(DST, 'data');
if (fs.existsSync(dataDir)) {
  fs.cpSync(dataDir, distDataDir, { recursive: true });
  const dataCount = countFiles(distDataDir);
  console.log(`  ✅ ${dataCount} data files → dist/data/`);
}

// ─── Signal vs. Street page — always use latest source ───
const svsSrc = path.join(ROOT, 'signal-vs-the-street.html');
const svsDst = path.join(DST, 'signal-vs-the-street', 'index.html');
if (fs.existsSync(svsSrc)) {
  fs.mkdirSync(path.dirname(svsDst), { recursive: true });
  fs.copyFileSync(svsSrc, svsDst);
  // Rewrite image paths in SVS page too (copied after main rewriter)
  let svsContent = fs.readFileSync(svsDst, 'utf8');
  svsContent = svsContent.replace(/"\/img\//g, '"' + R2_IMG_BASE + '/img/');
  fs.writeFileSync(svsDst, svsContent);
  console.log(`  ✅ Signal vs. Street page synced from project root`);
}

// ─── Pricing page ───
const pricingSrc = path.join(ROOT, 'pricing', 'index.html');
const pricingDst = path.join(DST, 'pricing', 'index.html');
if (fs.existsSync(pricingSrc)) {
  fs.mkdirSync(path.dirname(pricingDst), { recursive: true });
  fs.copyFileSync(pricingSrc, pricingDst);
  let pricingContent = fs.readFileSync(pricingDst, 'utf8');
  pricingContent = pricingContent.replace(/"\/img\//g, '"' + R2_IMG_BASE + '/img/');
  fs.writeFileSync(pricingDst, pricingContent);
  console.log(`  ✅ Pricing page synced`);
}

// ─── Account page ───
const accountSrc = path.join(ROOT, 'account', 'index.html');
const accountDst = path.join(DST, 'account', 'index.html');
if (fs.existsSync(accountSrc)) {
  fs.mkdirSync(path.dirname(accountDst), { recursive: true });
  fs.copyFileSync(accountSrc, accountDst);
  let accountContent = fs.readFileSync(accountDst, 'utf8');
  accountContent = accountContent.replace(/"\/img\//g, '"' + R2_IMG_BASE + '/img/');
  fs.writeFileSync(accountDst, accountContent);
  console.log(`  ✅ Account page synced`);
}

// ─── Post-build: Sync Ask Pulse CSS/JS to public/ (lock-in) ───
// Prevents stale copies in public/ from overwriting our curated _backup_dist/ changes
const pulseCssSrc = path.join(SRC, 'css', 'main.css');
const pulseCssDst = path.join(ROOT, 'public', 'css', 'main.css');
if (fs.existsSync(pulseCssSrc)) {
  fs.copyFileSync(pulseCssSrc, pulseCssDst);
  console.log('  🔒 Synced Ask Pulse CSS to public/ (lock-in)');
}

const pulseJsSrc = path.join(SRC, 'js', 'pulse.js');
const pulseJsDst = path.join(ROOT, 'public', 'js', 'pulse.js');
if (fs.existsSync(pulseJsSrc) && fs.existsSync(path.dirname(pulseJsDst))) {
  fs.copyFileSync(pulseJsSrc, pulseJsDst);
  console.log('  🔒 Synced Ask Pulse JS to public/ (lock-in)');
}
