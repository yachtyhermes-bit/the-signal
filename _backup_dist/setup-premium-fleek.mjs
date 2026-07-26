#!/usr/bin/env node
// Grant premium access to Fleek
// Usage: node setup-premium-fleek.js <site-url> or without args for local
const SITE_URL = process.argv[2] || 'https://readthesignal.net';
const API = `${SITE_URL}/api/hive?action=set-premium`;

const body = {
  username: 'fleek',
  secret: 'signal_admin_2026',
  plan: 'premium',
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
    console.log('✅ Fleek granted premium access!');
    console.log('Plan:', data.plan);
  } else {
    console.error('❌ Failed:', data.error || JSON.stringify(data));
    console.log('If user does not exist, create account first.');
  }
})
.catch(err => {
  console.error('❌ Error:', err.message);
});
