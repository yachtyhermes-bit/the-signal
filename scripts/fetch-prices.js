#!/usr/bin/env node
// Fetch prices for tracked tickers using Yahoo Finance public API
const https = require('https');
const fs = require('fs');
const path = require('path');

const TICKERS = [
  // AI & Semis
  'NVDA', 'AMD', 'AVGO', 'MRVL', 'TSM', 'ASML', 'MU', 'CBRS',
  // Cybersecurity
  'CRWD', 'PANW', 'FTNT', 'ZS', 'S', 'CHKP', 'CYBR', 'TENB',
  // AI Software
  'PLTR', 'DDOG', 'SNOW', 'NOW', 'NET', 'AI',
  // Defense Primes
  'LMT', 'RTX', 'NOC', 'GD', 'LHX',
  // Space & Emerging Defense
  'RKLB', 'RDW', 'KTOS', 'AVAV', 'LUNR', 'ASTS', 'PL',
  // Mega-cap Tech
  'AAPL', 'MSFT', 'GOOGL', 'AMZN', 'META', 'TSLA'
];

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
  'GD': { name: 'General Dynamics', url: 'https://www.gd.com/' },
  'LHX': { name: 'L3Harris Technologies', url: 'https://www.l3harris.com/' },
  'KTOS': { name: 'Kratos Defense & Security', url: 'https://www.kratosdefense.com/' },
  'AVAV': { name: 'AeroVironment Inc.', url: 'https://www.avinc.com/' },
  'LUNR': { name: 'Intuitive Machines', url: 'https://www.intuitivemachines.com/' },
  'ASTS': { name: 'AST SpaceMobile', url: 'https://www.ast-science.com/' },
  'PL': { name: 'Planet Labs', url: 'https://www.planet.com/' }
};

// Fetch from Yahoo Finance v8 API
function fetchQuote(ticker) {
  return new Promise((resolve, reject) => {
    const url = `https://query1.finance.yahoo.com/v8/finance/chart/${ticker}?interval=1d&range=2d`;
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
          const close = meta.chartPreviousClose || null;
          const current = meta.regularMarketPrice || quotes?.close?.[quotes.close.length - 1] || null;
          const open = quotes?.open?.[0] || null;
          const change = current && close ? current - close : null;
          const changePercent = current && close ? (change / close) * 100 : null;
          const volume = quotes?.volume?.[quotes.volume.length - 1] || null;
          const info = COMPANY_INFO[ticker] || {};
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
            lastUpdated: new Date().toISOString()
          });
        } catch (e) { reject(e); }
      });
    }).on('error', reject);
  });
}

async function main() {
  const prices = {};
  // Fetch in batches to avoid rate limiting
  const batchSize = 5;
  for (let i = 0; i < TICKERS.length; i += batchSize) {
    const batch = TICKERS.slice(i, i + batchSize);
    const results = await Promise.allSettled(batch.map(fetchQuote));
    for (const r of results) {
      if (r.status === 'fulfilled' && r.value) {
        prices[r.value.ticker] = r.value;
      }
    }
    // Small delay between batches
    if (i + batchSize < TICKERS.length) await new Promise(r => setTimeout(r, 1000));
  }
  fs.writeFileSync(path.join(__dirname, '..', 'data', 'prices.json'), JSON.stringify(prices, null, 2));
  console.log(`✅ Fetched prices for ${Object.keys(prices).length}/${TICKERS.length} tickers`);
}

main().catch(console.error);
