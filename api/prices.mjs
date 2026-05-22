// Price proxy — Vercel serverless function
// Fetches from Yahoo Finance server-side (no CORS issues)
// .mjs for ESM on Vercel

const TICKERS = [
  'NVDA', 'PLTR', 'AVGO', 'AMD', 'GOOGL', 'META', 'MSFT', 'AMZN', 'TSLA', 'CRWV'
];

async function fetchQuote(ticker) {
  const url = `https://query1.finance.yahoo.com/v8/finance/chart/${ticker}?interval=1d&range=2d`;
  const res = await fetch(url, {
    headers: { 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36' }
  });
  const data = await res.json();
  const result = data.chart?.result?.[0];
  if (!result) return null;

  const meta = result.meta;
  const quotes = result.indicators?.quote?.[0];
  const closes = quotes?.close?.filter(c => c != null) || [];
  const price = closes.length ? closes[closes.length - 1] : meta.regularMarketPrice;
  const prevClose = closes.length >= 2 ? closes[closes.length - 2] : meta.chartPreviousClose;
  const changePercent = price && prevClose ? ((price - prevClose) / prevClose) * 100 : null;

  return {
    ticker,
    price,
    prevClose,
    change: price - prevClose,
    changePercent,
    lastUpdated: new Date().toISOString()
  };
}

export default async function handler(req, res) {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
  res.setHeader('Cache-Control', 'public, max-age=60, s-maxage=60, stale-while-revalidate=120');

  if (req.method === 'OPTIONS') return res.status(200).end();

  try {
    const results = {};
    const batchSize = 5;
    for (let i = 0; i < TICKERS.length; i += batchSize) {
      const batch = TICKERS.slice(i, i + batchSize);
      const settled = await Promise.allSettled(batch.map(fetchQuote));
      for (const r of settled) {
        if (r.status === 'fulfilled' && r.value) {
          results[r.value.ticker] = r.value;
        }
      }
      if (i + batchSize < TICKERS.length) {
        await new Promise(r => setTimeout(r, 500));
      }
    }

    return res.status(200).json({
      prices: results,
      lastUpdated: new Date().toISOString(),
      count: Object.keys(results).length
    });
  } catch (error) {
    console.error('Price proxy error:', error.message);
    return res.status(500).json({ error: 'Failed to fetch prices' });
  }
}
