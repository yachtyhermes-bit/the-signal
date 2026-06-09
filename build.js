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

const SECTORS = {
  ai: 'AI', cyber: 'Cyber', defense: 'Defense',
  space: 'Space', 'mega-cap': 'Mega-Cap', quantum: 'Quantum'
};

const HOMEPAGE_LIMIT = 36;

// ─── 1. Copy frozen assets ───
console.log('📦 Copying frozen assets from _backup_dist/...');
if (!fs.existsSync(SRC)) {
  console.error('ERROR: _backup_dist/ not found!');
  process.exit(1);
}
fs.rmSync(DST, { recursive: true, force: true });
fs.cpSync(SRC, DST, { recursive: true });

// GUARD: Abort if homepage is suspiciously small (< 45KB = stripped design)
const htmlSize = fs.statSync(path.join(DST, 'index.html')).size;
if (htmlSize < 45000) {
  console.error(`⛔ FATAL: index.html is ${htmlSize} bytes — expected ~48,000+.`);
  console.error('   The frozen design may be corrupted.');
  process.exit(1);
}
console.log(`  ✅ ${htmlSize} bytes design → dist/`);

// ─── 1.5. Copy article images ───
const imgDir = path.join(ROOT, 'public', 'img');
const distImgDir = path.join(DST, 'img');
if (fs.existsSync(imgDir)) {
  fs.cpSync(imgDir, distImgDir, { recursive: true });
  console.log(`  ✅ ${countFiles(distImgDir)} image files → dist/img/`);
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
const grid1 = homepage.slice(1, 5);              // 4 articles
const grid2 = homepage.slice(5, 12);             // 7 articles
const grid3 = homepage.slice(12, 21);            // 9 articles
const grid4 = homepage.slice(21, 36);            // 15 articles

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
  `<section class="feed">\n  <div class="article-grid">\n${featuredHtml}\n  </div>\n</section>`);

indexHtml = indexHtml.replace('<!-- GRID_1 -->',
  `<section class="feed feed-continued">\n  <div class="article-grid">\n${grid1Html}\n  </div>\n</section>`);

indexHtml = indexHtml.replace('<!-- GRID_2 -->',
  `<section class="feed feed-continued">\n  <div class="article-grid">\n${grid2Html}\n  </div>\n</section>`);

indexHtml = indexHtml.replace('<!-- GRID_3 -->',
  `<section class="feed feed-continued">\n  <div class="article-grid">\n${grid3Html}\n  </div>\n</section>`);

indexHtml = indexHtml.replace('<!-- GRID_4 -->',
  `<section class="feed feed-continued">\n  <div class="article-grid">\n${grid4Html}\n  </div>\n</section>`);

fs.writeFileSync(path.join(DST, 'index.html'), indexHtml);

const finalSize = fs.statSync(path.join(DST, 'index.html')).size;
console.log(`  ✅ Homepage built: ${finalSize} bytes`);

// GUARD: Abort if homepage is suspiciously small (< 350KB with 36 articles)
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
      const imageSrc = (article.image && article.image.src) || '/img/articles/_default.jpg';
      const imageCaption = (article.image && article.image.caption) || article.title || '';
      const sector = article.sector || 'ai';
      const sectorName = SECTORS[sector] || sector.toUpperCase();
      const sentiment = article.sentiment || 'neutral';
      const sentimentLabel = sentiment === 'bullish' ? '▲ Bullish' : sentiment === 'bearish' ? '▼ Bearish' : '– Neutral';
      const sentimentBadge = `<span class="sentiment-label large ${sentiment}">${sentimentLabel}</span>`;
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

      let html = template
        .replace(/{{TITLE}}/g, article.title || '')
        .replace(/{{SUMMARY}}/g, (article.summary || '').replace(/"/g, '&quot;'))
        .replace(/{{SLUG}}/g, slug)
        .replace(/{{TICKER}}/g, article.ticker || '')
        .replace(/{{SECTOR}}/g, sector)
        .replace(/{{SECTOR_UC}}/g, sectorName)
        .replace(/{{SENTIMENT}}/g, sentiment)
        .replace(/{{SENTIMENT_BADGE}}/g, sentimentBadge)
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
        .replace(/\{\{[A-Z_]+\}\}/g, '');

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

// ─── 8. Generate sector pages ───
const sectorTemplate = fs.existsSync(SECTOR_TEMPLATE)
  ? fs.readFileSync(SECTOR_TEMPLATE, 'utf8')
  : null;

if (!sectorTemplate) {
  console.log('⚠️  No sector template — skipping sector pages');
} else {
  // Group articles by sector (only for articles NOT on homepage)
  const bySector = {};
  for (const a of sectorArticles) {
    const s = a.sector || 'other';
    if (!bySector[s]) bySector[s] = [];
    bySector[s].push(a);
  }
  // Also check if homepage articles need sector duplicates — no, they don't.
  // Sector pages only show deep archive articles.

  let sectorCount = 0;
  for (const [sector, arts] of Object.entries(bySector)) {
    const sectorName = SECTORS[sector] || sector.toUpperCase();
    const cards = arts.map(a => articleCard(a)).join('\n');
    
    let html = sectorTemplate
      .replace(/{{SECTOR}}/g, sector)
      .replace(/{{SECTOR_NAME}}/g, sectorName)
      .replace('{{ARTICLE_CARDS}}', cards);
    
    const outDir = path.join(DST, 'sector', sector);
    fs.mkdirSync(outDir, { recursive: true });
    fs.writeFileSync(path.join(outDir, 'index.html'), html);
    sectorCount++;
    console.log(`  📂 /sector/${sector}/ — ${arts.length} articles`);
  }
  console.log(`  ✅ ${sectorCount} sector pages generated`);
}

// ─── 9. Copy API serverless functions ───
const apiDir = path.join(ROOT, 'api');
const distApiDir = path.join(DST, 'api');
if (fs.existsSync(apiDir)) {
  fs.mkdirSync(distApiDir, { recursive: true });
  const apiFiles = fs.readdirSync(apiDir);
  for (const f of apiFiles) {
    fs.copyFileSync(path.join(apiDir, f), path.join(distApiDir, f));
  }
  console.log(`  ✅ ${apiFiles.length} API functions copied`);
}

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
  const img = (a.image && a.image.src) || '/img/articles/_default.jpg';
  const sentiment = a.sentiment || 'neutral';
  const sentimentLabel = sentiment === 'bullish' ? '▲ Bullish' : sentiment === 'bearish' ? '▼ Bearish' : '– Neutral';
  const readTime = (a.meta && a.meta.estimatedReadTime) || '1 min read';
  const dateStr = formatDate((a.date || '').slice(0, 10));

  return `<a href="/article/${a.slug}" class="article-card featured-card">
    <div class="card-image"><img src="${img}" alt="${escapeAttr(a.title || '')}" loading="eager" decoding="async" width="1200" height="675"></div>
    <div class="card-body">
    <div class="card-top">
      <span class="ticker-badge ${sentiment}">${escapeHtml(a.ticker || '')}</span>
      <span class="sentiment-label ${sentiment}">${sentimentLabel}</span>
    </div>
    <h3 class="card-title">${escapeHtml(a.title || '')}</h3>
    <p class="card-summary">${escapeHtml((a.summary || '').substring(0, 280))}${(a.summary || '').length > 280 ? '...' : ''}</p>
    <div class="card-meta"><span>${dateStr}</span><span>${readTime}</span></div>
    </div></a>`;
}

function articleCard(a) {
  const img = (a.image && a.image.src) || '/img/articles/_default.jpg';
  const sentiment = a.sentiment || 'neutral';
  const sentimentLabel = sentiment === 'bullish' ? '▲ Bullish' : sentiment === 'bearish' ? '▼ Bearish' : '– Neutral';
  const readTime = (a.meta && a.meta.estimatedReadTime) || '1 min read';
  const dateStr = formatDate((a.date || '').slice(0, 10));
  const summary = (a.summary || '').substring(0, 160);
  const ellipsis = (a.summary || '').length > 160 ? '...' : '';

  return `<a href="/article/${a.slug}" class="article-card">
    <div class="card-image"><img src="${img}" alt="${escapeAttr(a.title || '')}" loading="lazy" decoding="async" width="1200" height="675"></div>
    <div class="card-body">
    <div class="card-top">
      <span class="ticker-badge ${sentiment}">${escapeHtml(a.ticker || '')}</span>
      <span class="sentiment-label ${sentiment}">${sentimentLabel}</span>
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
    const img = (a.image && a.image.src) || '/img/articles/_default.jpg';
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
