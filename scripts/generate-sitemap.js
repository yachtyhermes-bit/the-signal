#!/usr/bin/env node
// Generates sitemap.xml into dist/ — called by build.js after all pages are built
// SEO consolidation (2026-09-07): canonical URL form is NO trailing slash
// (matches article canonicals + Google's established canonicalization). All locs
// here are no-slash, deduped, with real per-article lastmods (no fake daily churn).
const fs = require('fs');
const path = require('path');

const ROOT = path.join(__dirname, '..');
const DST = path.join(ROOT, 'dist');
const POSTS_DIR = path.join(ROOT, 'articles', 'posts');

const today = new Date().toISOString().split('T')[0];
const SITE = 'https://readthesignal.net';
const seen = new Set();
const urls = [];

function add(loc, priority, changefreq, lastmod) {
  // Canonical URL form = trailing slash (Vercel trailingSlash:true 308s bare
  // forms to slash; slash is the 200-served canonical form)
  if (loc !== `${SITE}/` && !loc.endsWith('/')) loc += '/';
  if (seen.has(loc)) return; // dedupe (slug collisions etc.)
  seen.add(loc);
  urls.push({ loc, priority, changefreq, lastmod });
}

// Article lastmod: real edit date (file mtime) when newer than publish date,
// else publish date — mirrors build.js dateModified logic. No build-date stamps.
function articleLastmod(a, file) {
  try {
    const date = a.date ? String(a.date).slice(0, 10) : '';
    const mtime = new Date(fs.statSync(path.join(POSTS_DIR, file)).mtime)
      .toISOString().slice(0, 10);
    if (date && mtime > date) return mtime;
    if (date) return date;
    return mtime;
  } catch (_) { return today; }
}

// Homepage — genuinely changes daily (new articles, prices)
add(`${SITE}/`, '1.0', 'daily', today);

// Stocks index + stock pages
add(`${SITE}/stocks`, '0.9', 'weekly');
const finPath = path.join(ROOT, 'data', 'financials.json');
if (fs.existsSync(finPath)) {
  const fins = JSON.parse(fs.readFileSync(finPath, 'utf8'));
  for (const ticker of Object.keys(fins)) {
    add(`${SITE}/stocks/${ticker}`, '0.8', 'weekly');
  }
}

// Sector pages — derived from actual article sector values (matches build.js bySector)
const sectors = new Set();
if (fs.existsSync(POSTS_DIR)) {
  const files = fs.readdirSync(POSTS_DIR).filter(f => f.endsWith('.json'));
  for (const file of files) {
    try {
      const a = JSON.parse(fs.readFileSync(path.join(POSTS_DIR, file), 'utf8'));
      if (a.sector) sectors.add(a.sector);
    } catch (_) {}
  }
}
for (const sector of sectors) {
  add(`${SITE}/sector/${sector}`, '0.7', 'weekly');
}

// Article pages
if (fs.existsSync(POSTS_DIR)) {
  const files = fs.readdirSync(POSTS_DIR).filter(f => f.endsWith('.json'));
  for (const file of files) {
    try {
      const a = JSON.parse(fs.readFileSync(path.join(POSTS_DIR, file), 'utf8'));
      if (a.slug) {
        add(`${SITE}/article/${a.slug}`, '0.6', 'weekly', articleLastmod(a, file));
      }
    } catch (_) {}
  }
}

// Static pages
add(`${SITE}/explainers`, '0.7', 'weekly');
add(`${SITE}/pricing`, '0.7', 'monthly');
add(`${SITE}/hive`, '0.5', 'weekly');
add(`${SITE}/hive/boardroom`, '0.4', 'weekly');
add(`${SITE}/signal-vs-the-street`, '0.5', 'weekly');
add(`${SITE}/about`, '0.3', 'monthly');
add(`${SITE}/premium`, '0.5', 'monthly');
add(`${SITE}/insights`, '0.6', 'weekly');
add(`${SITE}/watchlist`, '0.6', 'weekly');
add(`${SITE}/buffett`, '0.4', 'monthly');
add(`${SITE}/pelosi`, '0.4', 'monthly');

// Generate XML
let xml = '<?xml version="1.0" encoding="UTF-8"?>\n';
xml += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n';
for (const u of urls) {
  xml += '  <url>\n';
  xml += `    <loc>${u.loc}</loc>\n`;
  if (u.lastmod) xml += `    <lastmod>${u.lastmod}</lastmod>\n`;
  xml += `    <changefreq>${u.changefreq}</changefreq>\n`;
  xml += `    <priority>${u.priority}</priority>\n`;
  xml += '  </url>\n';
}
xml += '</urlset>\n';

fs.writeFileSync(path.join(DST, 'sitemap.xml'), xml);
console.log(`  ✅ Sitemap: ${urls.length} URLs (slash canonicals, real lastmods)`);
