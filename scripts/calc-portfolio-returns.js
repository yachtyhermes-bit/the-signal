#!/usr/bin/env node
/**
 * The Signal — Portfolio Return Calculator
 * 
 * Fetches historical prices and calculates portfolio returns vs SPY and QQQ.
 * Results saved to data/portfolio-returns.json for the page to consume.
 * 
 * Usage: node scripts/calc-portfolio-returns.js
 */

const path = require('path');
const fs = require('fs');

const PORTFOLIO_PATH = path.join(__dirname, '..', 'data', 'portfolio.json');
const RETURNS_PATH = path.join(__dirname, '..', 'data', 'portfolio-returns.json');

const BENCHMARKS = [
  { ticker: 'SPY', label: "S&P 500" },
  { ticker: 'QQQ', label: "Nasdaq 100" }
];

// Anchors are derived from the run date so the windows never go stale.
// 1Y = trailing twelve months (this is what the page labels "Trailing 12 Months").
function daysAgoISO(days) {
  const d = new Date();
  d.setUTCDate(d.getUTCDate() - days);
  return d.toISOString().slice(0, 10);
}
const YTD_ANCHOR = `${new Date().getUTCFullYear()}-01-01`;
const ONE_YEAR_ANCHOR = daysAgoISO(365);

async function fetchClosePrice(ticker, dateStr) {
  const fromTs = Math.floor(new Date(dateStr).getTime() / 1000);
  const toTs = fromTs + 86400 * 3;
  try {
    const resp = await fetch(
      `https://query1.finance.yahoo.com/v8/finance/chart/${ticker}?interval=1d&period1=${fromTs}&period2=${toTs}`,
      { headers: { 'User-Agent': 'Mozilla/5.0' }, signal: AbortSignal.timeout(10000) }
    );
    if (!resp.ok) return null;
    const data = await resp.json();
    const result = data.chart?.result?.[0];
    if (!result) return null;
    const quotes = result.indicators?.quote?.[0];
    const closes = quotes?.close?.filter(c => c != null) || [];
    const timestamps = result.timestamp || [];
    for (let i = 0; i < timestamps.length; i++) {
      if (timestamps[i] >= fromTs && closes[i] != null) {
        return { price: closes[i], date: new Date(timestamps[i] * 1000).toISOString().slice(0,10) };
      }
    }
    if (closes.length > 0) {
      return { price: closes[closes.length - 1], date: new Date(timestamps[timestamps.length - 1] * 1000).toISOString().slice(0,10) };
    }
    return null;
  } catch { return null; }
}

async function fetchCurrentPrice(ticker) {
  try {
    const resp = await fetch(
      `https://query1.finance.yahoo.com/v8/finance/chart/${ticker}?interval=1d&range=5d`,
      { headers: { 'User-Agent': 'Mozilla/5.0' }, signal: AbortSignal.timeout(10000) }
    );
    if (!resp.ok) return null;
    const data = await resp.json();
    const result = data.chart?.result?.[0];
    if (!result) return null;
    const quotes = result.indicators?.quote?.[0];
    const closes = quotes?.close?.filter(c => c != null) || [];
    const price = closes.length > 0 ? closes[closes.length - 1] : result.meta?.regularMarketPrice;
    return { price, date: new Date().toISOString().slice(0,10) };
  } catch { return null; }
}

function calcReturn(fromPrice, toPrice) {
  if (!fromPrice || !toPrice) return null;
  return ((toPrice - fromPrice) / fromPrice) * 100;
}

async function main() {
  console.log('📊 Signal vs. The Street — Return Calculator\n');

  const config = JSON.parse(fs.readFileSync(PORTFOLIO_PATH, 'utf8'));
  const positions = config.positions;
  const totalWeight = positions.reduce((s, p) => s + p.weight, 0);
  const allTickers = [...new Set([...positions.map(p => p.ticker), ...BENCHMARKS.map(b => b.ticker)])];

  console.log(`Portfolio: ${positions.length} positions\n`);

  // Fetch prices for all tickers at all relevant dates
  const priceData = {};
  for (const ticker of allTickers) {
    process.stdout.write(`  ${ticker}... `);
    priceData[ticker] = {};

    const inc = await fetchClosePrice(ticker, '2024-06-01');
    priceData[ticker].inception = inc?.price || null;

    const ytd = await fetchClosePrice(ticker, YTD_ANCHOR);
    priceData[ticker].ytd = ytd?.price || null;

    const oneY = await fetchClosePrice(ticker, ONE_YEAR_ANCHOR);
    priceData[ticker].oneYear = oneY?.price || null;

    const cur = await fetchCurrentPrice(ticker);
    priceData[ticker].current = cur?.price || null;

    console.log(priceData[ticker].current ? '✅' : '⚠️');
    await new Promise(r => setTimeout(r, 400));
  }

  // Calculate returns
  const results = {
    name: config.name,
    inception: config.inception,
    lastUpdated: new Date().toISOString(),
    periods: {},
    holdings: null
  };

  for (const period of [
    { key: 'sinceInception', fromKey: 'inception', toKey: 'current', label: 'Since Inception' },
    { key: 'ytd', fromKey: 'ytd', toKey: 'current', label: 'YTD' },
    { key: 'oneYear', fromKey: 'oneYear', toKey: 'current', label: '1 Year' },
  ]) {
    let weightedReturn = 0, validWeight = 0;
    const posReturns = [];

    for (const pos of positions) {
      const from = priceData[pos.ticker]?.[period.fromKey];
      const to = priceData[pos.ticker]?.[period.toKey];
      const ret = calcReturn(from, to);
      if (ret !== null) {
        posReturns.push({ ticker: pos.ticker, weight: pos.weight, return: Math.round(ret * 100) / 100 });
        weightedReturn += (pos.weight / totalWeight) * ret;
        validWeight += pos.weight;
      }
    }

    const spyRet = calcReturn(priceData['SPY']?.[period.fromKey], priceData['SPY']?.[period.toKey]);
    const qqqRet = calcReturn(priceData['QQQ']?.[period.fromKey], priceData['QQQ']?.[period.toKey]);

    const portRet = validWeight > 0 ? Math.round(weightedReturn * 100) / 100 : null;

    results.periods[period.key] = {
      label: period.label,
      portfolioReturn: portRet,
      spyReturn: spyRet !== null ? Math.round(spyRet * 100) / 100 : null,
      qqqReturn: qqqRet !== null ? Math.round(qqqRet * 100) / 100 : null,
      vsSPY: (portRet && spyRet) ? Math.round((portRet - spyRet) * 100) / 100 : null,
      vsQQQ: (portRet && qqqRet) ? Math.round((portRet - qqqRet) * 100) / 100 : null,
    };
  }

  // Build holdings list for display (top 5 visible, rest premium-locked)
  const sortedPositions = [...positions].sort((a, b) => b.weight - a.weight);
  results.holdings = sortedPositions.map(p => {
    const incReturn = calcReturn(priceData[p.ticker]?.inception, priceData[p.ticker]?.current);
    return {
      ticker: p.ticker,
      weight: p.weight,
      return: incReturn !== null ? Math.round(incReturn * 100) / 100 : null
    };
  });

  // NOTE: this block used to hardcode the 1Y figure to 81.49% (an "actual brokerage
  // figure" captured 2026-06-05, when the anchor was pinned at 2025-05-30). Both the
  // pinned date and the constant went stale: by Nov 2026 the window was ~17 months
  // while the page still labelled it "Trailing 12 Months". Every period now computes
  // from price history. Re-enter a fresh brokerage number here only if it is current,
  // and delete it once it ages out.

  fs.writeFileSync(RETURNS_PATH, JSON.stringify(results, null, 2));

  // Print summary
  for (const [key, r] of Object.entries(results.periods)) {
    console.log(`\n${r.label}:`);
    console.log(`  🐝 Signal:  ${r.portfolioReturn !== null ? r.portfolioReturn.toFixed(2) + '%' : 'N/A'}`);
    console.log(`  📊 SPY:     ${r.spyReturn !== null ? r.spyReturn.toFixed(2) + '%' : 'N/A'}`);
    console.log(`  ⚡ QQQ:     ${r.qqqReturn !== null ? r.qqqReturn.toFixed(2) + '%' : 'N/A'}`);
    if (r.vsSPY !== null) console.log(`  🔥 vs SPY:  ${r.vsSPY >= 0 ? '+' : ''}${r.vsSPY.toFixed(2)}%`);
  }

  console.log(`\n✅ Saved to ${RETURNS_PATH}`);
}

main().catch(err => { console.error(err.message); process.exit(1); });
