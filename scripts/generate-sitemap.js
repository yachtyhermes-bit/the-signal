#!/usr/bin/env node
// Generates sitemap.xml into dist/ — called by build.js after all pages are built
const fs = require('fs');
const path = require('path');

const ROOT = path.join(__dirname, '..');
const DST = path.join(ROOT, 'dist');
const POSTS_DIR = path.join(ROOT, 'articles', 'posts');

const SECTORS = {
  ai: 'AI', cyber: 'Cyber', defense: 'Defense',
  space: 'Space', 'mega-cap': 'Mega-Cap', quantum: 'Quantum'
};

const today = new Date().toISOString().split('T')[0];
const urls = [];

// Homepage
urls.push({ loc: 'https://readthesignal.net/', priority: '1.0', changefreq: 'hourly' });

// Stocks index + stock pages
urls.push({ loc: 'https://readthesignal.net/stocks/', priority: '0.9', changefreq: 'hourly' });
const finPath = path.join(ROOT, 'data', 'financials.json');
if (fs.existsSync(finPath)) {
  const fins = JSON.parse(fs.readFileSync(finPath, 'utf8'));
  for (const ticker of Object.keys(fins)) {
    urls.push({ loc: `https://readthesignal.net/stocks/${ticker}/`, priority: '0.8', changefreq: 'hourly' });
  }
}

// Sector pages
for (const sector of Object.keys(SECTORS)) {
  urls.push({ loc: `https://readthesignal.net/sector/${sector}/`, priority: '0.7', changefreq: 'daily' });
}

// Article pages
if (fs.existsSync(POSTS_DIR)) {
  const files = fs.readdirSync(POSTS_DIR).filter(f => f.endsWith('.json'));
  for (const file of files) {
    try {
      const a = JSON.parse(fs.readFileSync(path.join(POSTS_DIR, file), 'utf8'));
      if (a.slug) {
        urls.push({ loc: `https://readthesignal.net/article/${a.slug}/`, priority: '0.6', changefreq: 'weekly' });
      }
    } catch (_) {}
  }
}

// Static pages
urls.push({ loc: 'https://readthesignal.net/pricing/', priority: '0.7', changefreq: 'weekly' });
urls.push({ loc: 'https://readthesignal.net/hive/', priority: '0.5', changefreq: 'daily' });
urls.push({ loc: 'https://readthesignal.net/signal-vs-the-street/', priority: '0.5', changefreq: 'daily' });

// Generate XML
let xml = '<?xml version="1.0" encoding="UTF-8"?>\n';
xml += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n';
for (const u of urls) {
  xml += '  <url>\n';
  xml += `    <loc>${u.loc}</loc>\n`;
  xml += `    <lastmod>${today}</lastmod>\n`;
  xml += `    <changefreq>${u.changefreq}</changefreq>\n`;
  xml += `    <priority>${u.priority}</priority>\n`;
  xml += '  </url>\n';
}
xml += '</urlset>\n';

fs.writeFileSync(path.join(DST, 'sitemap.xml'), xml);
console.log(`  ✅ Sitemap: ${urls.length} URLs`);
