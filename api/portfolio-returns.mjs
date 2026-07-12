// Serves portfolio-returns.json data via API endpoint
// Compiled data from calc-portfolio-returns.js
import { join, dirname } from 'path';
import { readFileSync } from 'fs';

const DATA_PATH = join(dirname(new URL(import.meta.url).pathname), '..', 'data', 'portfolio-returns.json');

export default async function handler(req, res) {
  try {
    const json = readFileSync(DATA_PATH, 'utf8');
    res.setHeader('Content-Type', 'application/json');
    res.setHeader('Access-Control-Allow-Origin', '*');
    res.status(200).end(json);
  } catch (err) {
    res.status(500).json({ error: 'Failed to load portfolio data', message: err.message });
  }
}
