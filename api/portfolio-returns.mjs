// Portfolio returns data — Vercel serverless function
// Serves data/portfolio-returns.json via API endpoint
import { readFileSync } from 'fs';
import { dirname, join } from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);
const DATA_PATH = join(__dirname, '..', 'data', 'portfolio-returns.json');

export default async function handler(req, res) {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

  if (req.method === 'OPTIONS') {
    return res.status(200).end();
  }

  try {
    const data = readFileSync(DATA_PATH, 'utf8');
    res.setHeader('Content-Type', 'application/json');
    return res.status(200).end(data);
  } catch (err) {
    console.error('Portfolio returns error:', err.message);
    return res.status(500).json({ error: 'Failed to load portfolio data' });
  }
}
