// Newsletter subscribe — Vercel serverless function
// Stores emails and returns success.
// For production: connect to Buttondown / Mailchimp / ConvertKit

const SUBSCRIBERS_PATH = '/tmp/subscribers.json';
const DATA_FILE = './data/subscribers.json';

export default async function handler(req, res) {
  // CORS headers
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

  if (req.method === 'OPTIONS') {
    return res.status(200).end();
  }

  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  try {
    const { email } = req.body || {};

    // Validate email
    if (!email || typeof email !== 'string') {
      return res.status(400).json({ error: 'Email is required' });
    }

    const emailClean = email.trim().toLowerCase();
    if (!emailClean.includes('@') || !emailClean.includes('.')) {
      return res.status(400).json({ error: 'Invalid email address' });
    }

    // Read existing subscribers
    let subscribers = [];
    try {
      const fs = await import('fs/promises');
      const content = await fs.readFile(SUBSCRIBERS_PATH, 'utf8').catch(() => '[]');
      subscribers = JSON.parse(content);
    } catch {
      subscribers = [];
    }

    // Check for duplicates
    if (subscribers.some(s => s.email === emailClean)) {
      return res.json({ status: 'already_subscribed', message: "You're already subscribed!" });
    }

    // Add subscriber
    const entry = {
      email: emailClean,
      subscribedAt: new Date().toISOString(),
      source: 'thesignal.net'
    };
    subscribers.push(entry);

    // Save
    const fs = await import('fs/promises');
    await fs.writeFile(SUBSCRIBERS_PATH, JSON.stringify(subscribers, null, 2), 'utf8');

    // Also try to save to data/ for builds
    try {
      await fs.writeFile(DATA_FILE, JSON.stringify(subscribers, null, 2), 'utf8');
    } catch {
      // data/ might be read-only on Vercel, that's ok
    }

    return res.json({
      status: 'success',
      message: "You're subscribed! Welcome to The Signal 📡"
    });

  } catch (err) {
    console.error('Subscribe error:', err);
    return res.status(500).json({ error: 'Something went wrong. Try again.' });
  }
}
