#!/usr/bin/env node
// Passthrough build — copies known-good backup to dist/
// The backup at _backup_dist/ is the canonical 807KB site (deployment nphmhgo0f).
// To update the site: modify files in _backup_dist/ directly and commit.
const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

const ROOT = __dirname;
const BACKUP = path.join(ROOT, '_backup_dist');
const DIST = path.join(ROOT, 'dist');

if (!fs.existsSync(BACKUP)) {
  console.error('ERROR: _backup_dist/ not found. Cannot build.');
  process.exit(1);
}

// Clean dist/
if (fs.existsSync(DIST)) {
  fs.rmSync(DIST, { recursive: true });
}

// Copy backup → dist
fs.cpSync(BACKUP, DIST, { recursive: true });

const htmlSize = fs.statSync(path.join(DIST, 'index.html')).size;
const fileCount = execSync(`find ${DIST} -type f | wc -l`, { encoding: 'utf8' }).trim();
console.log(`Build complete: ${fileCount} files, index.html = ${(htmlSize / 1024).toFixed(0)} KB`);
