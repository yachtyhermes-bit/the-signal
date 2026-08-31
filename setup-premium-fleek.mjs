#!/usr/bin/env node
// Grant premium access to a Hive user (admin tool)
// Usage: node setup-premium-fleek.mjs <username> <plan>  (reads ADMIN_KEY from env or .env.local)
import fs from 'fs';
import path from 'path';

const SITE_URL = process.argv[2] || 'https://readthesignal.net';
const USERNAME = process.argv[3] || 'fleek';
const PLAN = process.argv[4] || 'premium';

// Load ADMIN_KEY from .env.local if present
let adminKey = process.env.ADMIN_KEY || '';
if (!adminKey) {
  try {
    const envPath = path.join(process.cwd(), '.env.local');
    const envContent = fs.readFileSync(envPath, 'utf8');
    const m = envContent.match(/^ADMIN_KEY="?([^"\n]+)"?/m);
    if (m) adminKey = m[1];
  } catch (e) { /* no .env.local */ }
}

if (!adminKey) {
  console.error('❌ ADMIN_KEY not found. Set ADMIN_KEY env var or add to .env.local');
  process.exit(1);
}

const API = `${SITE_URL}/api/hive?action=set-premium&admin_key=${encodeURIComponent(adminKey)}`;

const body = {
  admin_key: adminKey,
  email: USERNAME,
  plan: PLAN,
  since: new Date().toISOString()
};

fetch(API, {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify(body)
})
.then(r => r.json())
.then(data => {
  if (data.status === 'ok') {
    console.log(`✅ ${USERNAME} granted ${PLAN} access!`);
    console.log('Plan:', data.plan);
  } else {
    console.error('❌ Failed:', data.error || JSON.stringify(data));
    console.log('If user does not exist, create account first.');
  }
})
.catch(err => {
  console.error('❌ Error:', err.message);
});
