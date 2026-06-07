// build.js — PASSTHROUGH (June 4, 2026 architecture)
// Copies the known-good _backup_dist/ → dist/ verbatim.
// DO NOT replace this with a code generator!
// The known-good deployment has uncommitted features.
// Source of truth: _backup_dist/ (807KB, Jun 2, 2026 deployment nphmhgo0f)
// See: Obsidian → The Signal — Deployment Architecture.md

const fs = require('fs');
const path = require('path');

const SRC = path.join(__dirname, '_backup_dist');
const DST = path.join(__dirname, 'dist');

if (!fs.existsSync(SRC)) {
  console.error('ERROR: _backup_dist/ not found. Restore from backup first.');
  process.exit(1);
}

// Remove old dist
fs.rmSync(DST, { recursive: true, force: true });

// Copy entire _backup_dist → dist
fs.cpSync(SRC, DST, { recursive: true });

const htmlSize = fs.statSync(path.join(DST, 'index.html')).size;
console.log(`✅ Passthrough complete — ${htmlSize} bytes → dist/`);
