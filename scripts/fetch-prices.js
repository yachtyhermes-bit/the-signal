#!/usr/bin/env node
// Fetch prices for tracked tickers using Yahoo Finance public API
const https = require('https');
const fs = require('fs');
const path = require('path');

const TICKERS = [
  // AI & Semis
  'NVDA', 'AMD', 'AVGO', 'MRVL', 'TSM', 'ASML', 'MU', 'CBRS', 'INTC', 'IREN', 'LRCX', 'AMAT', 'QCOM', 'SMCI',
  // Cybersecurity
  'CRWD', 'PANW', 'FTNT', 'ZS', 'S', 'CHKP', 'CYBR', 'TENB',
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
  // Special tickers (mapped to different keys)
  'SPCX'   // stored as SPACEX
];

// Ticker mapping: Yahoo ticker → internal key
const TICKER_MAP = {
  'SPCX': 'SPACEX'
};

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
  'SMCI': { name: 'Super Micro Computer Inc.', url: 'https://www.supermicro.com/' }
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
          // Use actual quote closes for accuracy, not chartPreviousClose
          const closes = quotes?.close?.filter(c => c != null) || [];
          const current = closes.length ? closes[closes.length - 1] : (meta.regularMarketPrice || null);
          const close = closes.length >= 2 ? closes[closes.length - 2] : (meta.chartPreviousClose || null);
          const open = quotes?.open?.filter(o => o != null)?.[0] || null;
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
}

main().catch(console.error);
