#!/usr/bin/env node
// Fetch prices for tracked tickers using Yahoo Finance public API
const https = require('https');
const fs = require('fs');
const path = require('path');

const TICKERS = [
  // AI & Semis
  'NVDA', 'AMD', 'AVGO', 'MRVL', 'TSM', 'ASML', 'MU', 'CBRS', 'INTC', 'IREN', 'LRCX', 'AMAT', 'QCOM', 'SMCI',
  // AI Infrastructure
  'VRT',
  // Cybersecurity
  'CRWD', 'PANW', 'FTNT', 'ZS', 'S', 'CHKP', 'CYBR', 'TENB', 'RBRK',
  // AI Software
  'PLTR', 'DDOG', 'SNOW', 'NOW', 'NET', 'AI',
  // Defense Primes
  'LMT', 'RTX', 'NOC', 'GD', 'LHX',
  // Space & Emerging Defense
  'RKLB', 'RDW', 'KTOS', 'AVAV', 'LUNR', 'ASTS', 'PL',
  // Mega-cap Tech
  'AAPL', 'MSFT', 'GOOGL', 'AMZN', 'META', 'TSLA', 'NFLX',
  // The Signal coverage
  'AXON', 'CRWV', 'SOFI',
  // Special tickers
  'SPCX', 'ANET'
];

// Ticker mapping: Yahoo ticker → internal key
// (No longer remapping SPCX → SPACEX; using native SPCX key)
const TICKER_MAP = {};

// Company names & websites for reference
const COMPANY_INFO = {
  'NVDA': { name: 'NVIDIA Corporation', url: 'https://www.nvidia.com/' },
  'CBRS': { name: 'Cerebras Systems', url: 'https://www.cerebras.net/' },
  'PLTR': { name: 'Palantir Technologies', url: 'https://www.palantir.com/' },
  'RKLB': { name: 'Rocket Lab USA', url: 'https://www.rocketlabusa.com/' },
  'RDW': { name: 'Redwire Corporation', url: 'https://www.rdw.com/' },
  'AMD': { name: 'Advanced Micro Devices', url: 'https://www.amd.com/' },
  'AVGO': { name: 'Broadcom Inc.', url: 'https://www.broadcom.com/' },
  'CRWD': { name: 'CrowdStrike Holdings', url: 'https://www.crowdstrike.com/' },
  'PANW': { name: 'Palo Alto Networks', url: 'https://www.paloaltonetworks.com/' },
  'LMT': { name: 'Lockheed Martin', url: 'https://www.lockheedmartin.com/' },
  'RTX': { name: 'RTX Corporation', url: 'https://www.rtx.com/' },
  'NOC': { name: 'Northrop Grumman', url: 'https://www.northropgrumman.com/' },
  'MSFT': { name: 'Microsoft Corporation', url: 'https://www.microsoft.com/' },
  'GOOGL': { name: 'Alphabet Inc.', url: 'https://abc.xyz/' },
  'AMZN': { name: 'Amazon.com Inc.', url: 'https://www.amazon.com/' },
  'META': { name: 'Meta Platforms', url: 'https://about.meta.com/' },
  'TSLA': { name: 'Tesla Inc.', url: 'https://www.tesla.com/' },
  'AAPL': { name: 'Apple Inc.', url: 'https://www.apple.com/' },
  'MRVL': { name: 'Marvell Technology', url: 'https://www.marvell.com/' },
  'TSM': { name: 'Taiwan Semiconductor', url: 'https://www.tsmc.com/' },
  'ASML': { name: 'ASML Holding', url: 'https://www.asml.com/' },
  'MU': { name: 'Micron Technology', url: 'https://www.micron.com/' },
  'FTNT': { name: 'Fortinet Inc.', url: 'https://www.fortinet.com/' },
  'ZS': { name: 'Zscaler Inc.', url: 'https://www.zscaler.com/' },
  'S': { name: 'SentinelOne Inc.', url: 'https://www.sentinelone.com/' },
  'CHKP': { name: 'Check Point Software', url: 'https://www.checkpoint.com/' },
  'CYBR': { name: 'CyberArk Software', url: 'https://www.cyberark.com/' },
  'TENB': { name: 'Tenable Holdings', url: 'https://www.tenable.com/' },
  'DDOG': { name: 'Datadog Inc.', url: 'https://www.datadoghq.com/' },
  'SNOW': { name: 'Snowflake Inc.', url: 'https://www.snowflake.com/' },
  'NOW': { name: 'ServiceNow Inc.', url: 'https://www.servicenow.com/' },
  'NET': { name: 'Cloudflare Inc.', url: 'https://www.cloudflare.com/' },
  'AI': { name: 'C3.ai Inc.', url: 'https://c3.ai/' },
  'VRT': { name: 'Vertiv Holdings', url: 'https://www.vertiv.com/' },
  'GD': { name: 'General Dynamics', url: 'https://www.gd.com/' },
  'LHX': { name: 'L3Harris Technologies', url: 'https://www.l3harris.com/' },
  'KTOS': { name: 'Kratos Defense & Security', url: 'https://www.kratosdefense.com/' },
  'AVAV': { name: 'AeroVironment Inc.', url: 'https://www.avinc.com/' },
  'LUNR': { name: 'Intuitive Machines', url: 'https://www.intuitivemachines.com/' },
  'ASTS': { name: 'AST SpaceMobile', url: 'https://www.ast-science.com/' },
  'PL': { name: 'Planet Labs', url: 'https://www.planet.com/' },
  'AXON': { name: 'Axon Enterprise', url: 'https://www.axon.com/' },
  'CRWV': { name: 'CoreWeave Inc.', url: 'https://www.coreweave.com/' },
  'SOFI': { name: 'SoFi Technologies, Inc.', url: 'https://www.sofi.com/' },
  'INTC': { name: 'Intel Corporation', url: 'https://www.intel.com/' },
  'IREN': { name: 'Iris Energy', url: 'https://www.irisenergy.co/' },
  'LRCX': { name: 'Lam Research Corp.', url: 'https://www.lamresearch.com/' },
  'AMAT': { name: 'Applied Materials Inc.', url: 'https://www.appliedmaterials.com/' },
  'NFLX': { name: 'Netflix Inc.', url: 'https://www.netflix.com/' },
  'QCOM': { name: 'Qualcomm Inc.', url: 'https://www.qualcomm.com/' },
  'SMCI': { name: 'Super Micro Computer Inc.', url: 'https://www.supermicro.com/' },
  'ANET': { name: 'Arista Networks Inc.', url: 'https://www.arista.com/' },
  'RBRK': { name: 'Rubrik Inc.', url: 'https://www.rubrik.com/' },
  'SPCX': { name: 'SpaceX Inc.', url: 'https://www.spacex.com/' }
};

// Fetch from Yahoo Finance v8 API
function fetchQuote(ticker) {
  return new Promise((resolve, reject) => {
    const url = `https://query1.finance.yahoo.com/v8/finance/chart/${ticker}?interval=1d&range=5d`;
    https.get(url, { headers: { 'User-Agent': 'Mozilla/5.0' } }, (res) => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        try {
          const json = JSON.parse(data);
          const result = json.chart?.result?.[0];
          if (!result) return resolve(null);
          const meta = result.meta;
          const quotes = result.indicators?.quote?.[0];
          const timestamps = result.timestamp || [];
          // Use actual quote closes for accuracy, not chartPreviousClose
          const closes = quotes?.close?.filter(c => c != null) || [];
          const opens = quotes?.open || [];
          const highs = quotes?.high || [];
          const lows = quotes?.low || [];
          const volumes = quotes?.volume || [];
          const current = closes.length ? closes[closes.length - 1] : (meta.regularMarketPrice || null);
          const close = closes.length >= 2 ? closes[closes.length - 2] : (meta.chartPreviousClose || null);
          const open = opens.filter(o => o != null)?.[0] || null;
          const change = current && close ? current - close : null;
          const changePercent = current && close ? (change / close) * 100 : null;
          const volume = volumes[volumes.length - 1] || null;
          const info = COMPANY_INFO[ticker] || {};

          // Extract OHLC chart candles from the response
          const ohlcCandles = [];
          for (let i = 0; i < timestamps.length; i++) {
            const ts = timestamps[i];
            const o = opens[i];
            const h = highs[i];
            const l = lows[i];
            const c = closes[i];
            const v = volumes[i];
            if (o != null && h != null && l != null && c != null && ts) {
              const date = new Date(ts * 1000);
              const dateStr = date.toISOString().split('T')[0];
              ohlcCandles.push({
                time: dateStr,
                open: Math.round(o * 100) / 100,
                high: Math.round(h * 100) / 100,
                low: Math.round(l * 100) / 100,
                close: Math.round(c * 100) / 100,
                volume: v || 0,
              });
            }
          }

          resolve({
            ticker,
            name: info.name || ticker,
            companyUrl: info.url || null,
            price: current,
            open,
            previousClose: close,
            change,
            changePercent,
            volume,
            ohlcCandles,  // Fresh OHLC data to update financials.json
            lastUpdated: new Date().toISOString()
          });
        } catch (e) { reject(e); }
      });
    }).on('error', reject);
  });
}

async function main() {
  // Read existing prices to preserve manually-set data for tickers not on Yahoo
  const pricesPath = path.join(__dirname, '..', 'data', 'prices.json');
  let prices = {};
  if (fs.existsSync(pricesPath)) {
    try { prices = JSON.parse(fs.readFileSync(pricesPath, 'utf8')); } catch (_) {}
  }
  // Fetch in batches to avoid rate limiting
  const batchSize = 5;
  for (let i = 0; i < TICKERS.length; i += batchSize) {
    const batch = TICKERS.slice(i, i + batchSize);
    const results = await Promise.allSettled(batch.map(fetchQuote));
    for (const r of results) {
      if (r.status === 'fulfilled' && r.value) {
        const key = TICKER_MAP[r.value.ticker] || r.value.ticker;
        r.value.ticker = key;
        prices[key] = r.value;
      }
    }
    // Small delay between batches
    if (i + batchSize < TICKERS.length) await new Promise(r => setTimeout(r, 1000));
  }
  fs.writeFileSync(pricesPath, JSON.stringify(prices, null, 2));
  console.log(`✅ Fetched prices for ${Object.keys(prices).length}/${TICKERS.length} tickers`);

  // ── Also update financials.json chartData with fresh OHLC from Yahoo ──
  const financialsPath = path.join(__dirname, '..', 'data', 'financials.json');
  if (fs.existsSync(financialsPath)) {
    try {
      let financials = JSON.parse(fs.readFileSync(financialsPath, 'utf8'));
      let updated = 0;
      for (const [key, val] of Object.entries(prices)) {
        const candles = val.ohlcCandles;
        if (!candles || !candles.length) continue;
        const fin = financials[key];
        if (!fin) continue;
        const existing = fin.chartData || [];
        // Build a map of existing dates for quick lookup
        const dateMap = new Map();
        for (const c of existing) dateMap.set(c.time, c);
        // Upsert: update existing candles, add new ones
        for (const c of candles) {
          if (dateMap.has(c.time)) {
            const old = dateMap.get(c.time);
            // Only update if the new data has non-zero volume (real day, not empty)
            if (c.volume > 0) {
              old.open = c.open; old.high = c.high; old.low = c.low; old.close = c.close; old.volume = c.volume;
            }
          } else {
            existing.push(c);
            dateMap.set(c.time, c);
          }
        }
        // Sort by time ascending
        existing.sort((a, b) => a.time.localeCompare(b.time));
        fin.chartData = existing;
        updated++;
      }
      if (updated > 0) {
        fs.writeFileSync(financialsPath, JSON.stringify(financials, null, 2));
        console.log(`  ✅ Updated chartData in financials.json for ${updated}/${Object.keys(prices).length} tickers`);
      }
    } catch (e) {
      console.log(`  ⚠️  financials.json chartData update failed: ${e.message}`);
    }
  }
}

main().catch(console.error);
