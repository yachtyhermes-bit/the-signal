// build.js — HYBRID (June 7, 2026)
//
// ARCHITECTURE:
//   _backup_dist/ = FROZEN assets from known-good deployment (dpl_Cj8826, Jun 2)
//     → index.html (807KB), hive/, signal-vs-the-street/, sector/*, account/, css/, js/
//   articles/template.html = article page template
//   articles/posts/*.json = article data → generates dist/article/<slug>/index.html
//   API functions = COPIED from api/ directory
//
// TO UPDATE THE SITE:
//   Homepage/design → edit files in _backup_dist/
//   New articles → add JSON to articles/posts/ + img to public/img/articles/
//   CSS/JS → edit _backup_dist/css/ or _backup_dist/js/

const fs = require('fs');
const path = require('path');

const ROOT = path.join(__dirname);
const SRC = path.join(ROOT, '_backup_dist');
const DST = path.join(ROOT, 'dist');
const ARTICLE_TEMPLATE = path.join(ROOT, 'articles', 'template.html');
const POSTS_DIR = path.join(ROOT, 'articles', 'posts');

const SECTORS = {
  ai: 'AI', cyber: 'Cyber', defense: 'Defense',
  space: 'Space', 'mega-cap': 'Mega-Cap', quantum: 'Quantum'
};

// ─── 1. Copy frozen assets ───
console.log('📦 Copying frozen assets from _backup_dist/...');
if (!fs.existsSync(SRC)) {
  console.error('ERROR: _backup_dist/ not found!');
  process.exit(1);
}
fs.rmSync(DST, { recursive: true, force: true });
fs.cpSync(SRC, DST, { recursive: true });
const htmlBytes = fs.statSync(path.join(DST, 'index.html')).size;
console.log(`  ✅ ${htmlBytes} bytes homepage → dist/`);

// ─── 1.5. Copy article images ───
const imgDir = path.join(ROOT, 'public', 'img');
const distImgDir = path.join(DST, 'img');
if (fs.existsSync(imgDir)) {
  fs.cpSync(imgDir, distImgDir, { recursive: true });
  const imgCount = countFiles(distImgDir);
  console.log(`  ✅ ${imgCount} image files → dist/img/`);
}

// ─── 2. Generate article pages ───
const template = fs.existsSync(ARTICLE_TEMPLATE)
  ? fs.readFileSync(ARTICLE_TEMPLATE, 'utf8')
  : null;

if (template && fs.existsSync(POSTS_DIR)) {
  const posts = fs.readdirSync(POSTS_DIR).filter(f => f.endsWith('.json'));
  console.log(`📝 Generating ${posts.length} article pages...`);
  let generated = 0;

  for (const file of posts) {
    try {
      const article = JSON.parse(fs.readFileSync(path.join(POSTS_DIR, file), 'utf8'));
      const slug = article.slug || file.replace('.json', '');
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

      // Tags
      let tagsHtml = '';
      const tags = article.tags || [];
      if (tags.length > 0) {
        tagsHtml = '<div class="article-tags">' + tags.map(t => `<span class="tag">${escapeHtml(t)}</span>`).join('') + '</div>';
      }

      // Source links
      let linksHtml = '';
      const links = article.links || [];
      if (links.length > 0) {
        linksHtml = '<div class="article-links"><h4>📎 Sources &amp; References</h4><ul>' +
          links.map(l => `<li><a href="${escapeAttr(l.url)}" target="_blank" rel="noopener">${escapeHtml(l.label || l.url)}</a></li>`).join('') +
          '</ul></div>';
      }

      // Body: fix article body HTML links (they use /ticker/XXX paths)
      let bodyHtml = article.bodyHtml || '';
      // Convert /ticker/XXX links to proper <a> tags
      bodyHtml = bodyHtml.replace(/<a href='\/ticker\/([^']+)'>([^<]*)<\/a>/g, '<a href="/ticker/$1">$2</a>');

      // Remove escaped quotes from double-escaped JSON
      bodyHtml = bodyHtml.replace(/\\"/g, '"').replace(/\\n/g, '\n');

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
        // Replace remaining unused placeholders
        .replace(/\{\{[A-Z_]+\}\}/g, '');

      const outDir = path.join(DST, 'article', slug);
      fs.mkdirSync(outDir, { recursive: true });
      fs.writeFileSync(path.join(outDir, 'index.html'), html);
      generated++;
    } catch (e) {
      console.error(`  ⚠️  Error generating ${file}: ${e.message}`);
    }
  }
  console.log(`  ✅ ${generated} articles generated`);
} else if (!template) {
  console.log('⚠️  No template found at articles/template.html — skipping article generation');
}

// ─── 3. Copy API serverless functions ───
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

// ─── Helpers ───
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
