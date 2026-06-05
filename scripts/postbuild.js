// Post-build script — copies static pages and assets that build.js doesn't generate
const fs = require('fs');
const path = require('path');

const DIST = path.join(__dirname, '..', 'dist');

// 1. Copy updated assets from public/ to dist/
const assets = [
  ['public/js/hive-comments-widget.js', 'dist/js/hive-comments-widget.js'],
  ['public/css/main.css', 'dist/css/main.css'],
];
for (const [src, dest] of assets) {
  const fullSrc = path.join(__dirname, '..', src);
  const fullDest = path.join(__dirname, '..', dest);
  if (fs.existsSync(fullSrc)) {
    fs.mkdirSync(path.dirname(fullDest), { recursive: true });
    fs.copyFileSync(fullSrc, fullDest);
    console.log(`✓ ${dest}`);
  }
}

// 2. Restore static pages from backups
const pages = [
  ['account-settings.html', 'dist/account/settings/index.html'],
  ['signal-vs-the-street.html', 'dist/signal-vs-the-street/index.html'],
  ['av-style-sample.html', 'dist/av-style-sample.html'],
];

for (const [backup, dest] of pages) {
  const backupFile = path.join(__dirname, '..', backup);
  const destFull = path.join(__dirname, '..', dest);
  if (fs.existsSync(backupFile)) {
    fs.mkdirSync(path.dirname(destFull), { recursive: true });
    fs.copyFileSync(backupFile, destFull);
    console.log(`✓ ${dest} (restored)`);
  } else {
    console.log(`⚠ ${backup} not found — ${dest} may be missing`);
  }
}

// 3. Copy API serverless functions into dist/
const apiDir = path.join(__dirname, '..', 'api');
const distApiDir = path.join(DIST, 'api');
if (fs.existsSync(apiDir)) {
  fs.mkdirSync(distApiDir, { recursive: true });
  const apiFiles = fs.readdirSync(apiDir);
  for (const f of apiFiles) {
    const src = path.join(apiDir, f);
    const dest = path.join(distApiDir, f);
    fs.copyFileSync(src, dest);
    console.log(`✓ api/${f}`);
  }
}

console.log('✅ Post-build complete');
