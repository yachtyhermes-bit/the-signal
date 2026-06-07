// build.js — HYBRID (June 7, 2026)
//
// ARCHITECTURE:
//   _backup_dist/ = FROZEN assets from known-good deployment (dpl_Cj8826, Jun 2)
//     → index.html (807KB), hive/, signal-vs-the-street/, sector/*, account/, css/, js/
//   Article pages = GENERATED from articles/posts/*.json + templates
//   API functions = COPIED from api/ directory
//
// TO UPDATE THE SITE:
//   Homepage/design → edit files in _backup_dist/
//   New articles → add JSON to articles/posts/, this generator handles the rest
//   CSS/JS → edit _backup_dist/css/ or _backup_dist/js/

const fs = require('fs');
const path = require('path');

const ROOT = path.join(__dirname);
const SRC = path.join(ROOT, '_backup_dist');
const DST = path.join(ROOT, 'dist');
const ARTICLE_TEMPLATE = path.join(ROOT, 'articles', 'template.html');

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
const articleTemplate = fs.existsSync(ARTICLE_TEMPLATE) 
  ? fs.readFileSync(ARTICLE_TEMPLATE, 'utf8') 
  : null;

const postsDir = path.join(ROOT, 'articles', 'posts');
if (fs.existsSync(postsDir)) {
  const posts = fs.readdirSync(postsDir).filter(f => f.endsWith('.json'));
  console.log(`📝 Generating ${posts.length} article pages...`);
  
  for (const file of posts) {
    const article = JSON.parse(fs.readFileSync(path.join(postsDir, file), 'utf8'));
    const slug = article.slug || file.replace('.json', '');
    
    if (articleTemplate) {
      // Use template
      let html = articleTemplate
        .replace(/{{TITLE}}/g, article.title || '')
        .replace(/{{BODY}}/g, article.bodyHtml || '')
        .replace(/{{TICKER}}/g, article.ticker || '')
        .replace(/{{DATE}}/g, article.date || '')
        .replace(/{{SENTIMENT}}/g, article.sentiment || '')
        .replace(/{{SLUG}}/g, slug)
        .replace(/{{IMAGE}}/g, (article.image && article.image.src) || '');
      
      const outDir = path.join(DST, 'article');
      fs.mkdirSync(outDir, { recursive: true });
      fs.writeFileSync(path.join(outDir, `${slug}.html`), html);
    }
  }
  console.log(`  ✅ ${posts.length} articles generated`);
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

function countFiles(dir) {
  let count = 0;
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    if (entry.isDirectory()) count += countFiles(path.join(dir, entry.name));
    else count++;
  }
  return count;
}
