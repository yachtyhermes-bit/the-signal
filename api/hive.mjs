// The Hive API — Vercel serverless function
// Simulated trading & portfolio leaderboard for The Signal
// Supports username/password auth with stateless signed tokens
// DATA_VERSION: 2 (30-trader leaderboard restored Jun 7)
// DATA_VERSION: 3 (holdings format fix)
// GET  /api/hive?uid=XXX       → user portfolio
// POST /api/hive               → submit trade { uid, ticker, action, shares }
// GET  /api/hive?leaderboard=weekly|monthly|alltime → top 50
// GET  /api/hive?signal-master  → aggregated top 10% holdings
// GET  /api/hive?meta           → system stats
// GET  /api/hive?action=me&token=X → get current user
// POST /api/hive?action=register → create account { username, password, displayName }
// POST /api/hive?action=login  → authenticate { username, password }
// POST /api/hive?action=google-auth → auth with Google { credential }
// GET  /api/hive?stocks=true   → full stock list with prices

import crypto from 'crypto';
const HIVE_PATH = '/tmp/hive-data.json';

// GitHub persistence settings — data/hive-data.json in the repo
const GITHUB_TOKEN = process.env.GITHUB_TOKEN || '';
const GITHUB_OWNER = 'yachtyhermes-bit';
const GITHUB_REPO = 'the-signal';
const GITHUB_PATH = 'data/hive-data.json';
const GITHUB_BRANCH = 'main';

// In-memory cache to reduce GitHub API calls
let memoryCache = null;
let memoryCacheTime = 0;
const MEMORY_CACHE_TTL = 30000; // 30 seconds

// Game backdate — makes it look like a mature competition
const GAME_START = '2025-07-01T00:00:00.000Z';

// Server secret for stateless token signing
const SERVER_SECRET = 'hive_signal_secret_2026_' + (process.env.HIVE_SECRET || 'default_dev_secret');

const COVERAGE_UNIVERSE = new Set([
  // AI
  'NVDA','AMD','AVGO','MRVL','TSM','ASML','MU','CBRS','CRWV','NBIS','INTC','IREN','LRCX','AMAT','QCOM','SMCI',
  // Cyber
  'CRWD','PANW','FTNT','ZS','S','CHKP','CYBR','TENB','RBRK',
  // Defense
  'LMT','RTX','NOC','GD','LHX','KTOS','AVAV','PL','AXON','GE','PLTR',
  // Space
  'RKLB','RDW','LUNR','ASTS',
  // Mega-Cap
  'AAPL','MSFT','GOOGL','AMZN','META','TSLA','NFLX',
  // Quantum
  'IONQ','QBTS','QUBT','RGTI'
]);

const COMPANY_INFO = {
  'NVDA': { name: 'NVIDIA Corporation', sector: 'AI' },
  'AMD': { name: 'Advanced Micro Devices', sector: 'AI' },
  'AVGO': { name: 'Broadcom Inc.', sector: 'AI' },
  'MRVL': { name: 'Marvell Technology', sector: 'AI' },
  'TSM': { name: 'Taiwan Semiconductor', sector: 'AI' },
  'ASML': { name: 'ASML Holding', sector: 'AI' },
  'MU': { name: 'Micron Technology', sector: 'AI' },
  'CBRS': { name: 'Cerebras Systems', sector: 'AI' },
  'CRWV': { name: 'CoreWeave Inc.', sector: 'AI' },
  'NBIS': { name: 'Nebius Group', sector: 'AI' },
  'INTC': { name: 'Intel Corporation', sector: 'AI' },
  'IREN': { name: 'Iris Energy', sector: 'AI' },
  'LRCX': { name: 'Lam Research Corp.', sector: 'AI' },
  'AMAT': { name: 'Applied Materials Inc.', sector: 'AI' },
  'QCOM': { name: 'Qualcomm Inc.', sector: 'AI' },
  'SMCI': { name: 'Super Micro Computer Inc.', sector: 'AI' },
  'CRWD': { name: 'CrowdStrike Holdings', sector: 'Cybersecurity' },
  'PANW': { name: 'Palo Alto Networks', sector: 'Cybersecurity' },
  'FTNT': { name: 'Fortinet Inc.', sector: 'Cybersecurity' },
  'ZS': { name: 'Zscaler Inc.', sector: 'Cybersecurity' },
  'S': { name: 'SentinelOne Inc.', sector: 'Cybersecurity' },
  'CHKP': { name: 'Check Point Software', sector: 'Cybersecurity' },
  'CYBR': { name: 'CyberArk Software', sector: 'Cybersecurity' },
  'TENB': { name: 'Tenable Holdings', sector: 'Cybersecurity' },
  'RBRK': { name: 'Rubrik Inc.', sector: 'Cybersecurity' },
  'LMT': { name: 'Lockheed Martin', sector: 'Defense' },
  'RTX': { name: 'RTX Corporation', sector: 'Defense' },
  'NOC': { name: 'Northrop Grumman', sector: 'Defense' },
  'GD': { name: 'General Dynamics', sector: 'Defense' },
  'LHX': { name: 'L3Harris Technologies', sector: 'Defense' },
  'KTOS': { name: 'Kratos Defense & Security', sector: 'Defense' },
  'AVAV': { name: 'AeroVironment Inc.', sector: 'Defense' },
  'PL': { name: 'Planet Labs', sector: 'Defense' },
  'AXON': { name: 'Axon Enterprise', sector: 'Defense' },
  'GE': { name: 'GE Aerospace', sector: 'Defense' },
  'PLTR': { name: 'Palantir Technologies', sector: 'Defense' },
  'RKLB': { name: 'Rocket Lab USA', sector: 'Space' },
  'RDW': { name: 'Redwire Corporation', sector: 'Space' },
  'LUNR': { name: 'Intuitive Machines', sector: 'Space' },
  'ASTS': { name: 'AST SpaceMobile', sector: 'Space' },
  'AAPL': { name: 'Apple Inc.', sector: 'Mega-Cap' },
  'MSFT': { name: 'Microsoft Corporation', sector: 'Mega-Cap' },
  'GOOGL': { name: 'Alphabet Inc.', sector: 'Mega-Cap' },
  'AMZN': { name: 'Amazon.com Inc.', sector: 'Mega-Cap' },
  'META': { name: 'Meta Platforms', sector: 'Mega-Cap' },
  'TSLA': { name: 'Tesla Inc.', sector: 'Mega-Cap' },
  'NFLX': { name: 'Netflix Inc.', sector: 'Mega-Cap' },
  'IONQ': { name: 'IonQ Inc.', sector: 'Quantum' },
  'QBTS': { name: 'D-Wave Quantum Inc.', sector: 'Quantum' },
  'QUBT': { name: 'Quantum Computing Inc.', sector: 'Quantum' },
  'RGTI': { name: 'Rigetti Computing Inc.', sector: 'Quantum' }
};

const INITIAL_CASH = 100000;
const MIN_STOCKS = 3;
const MAX_STOCKS = 15;
const MAX_ALLOCATION = 0.40;

async function readData() {
  // 1. Check in-memory cache first
  if (memoryCache && (Date.now() - memoryCacheTime) < MEMORY_CACHE_TTL) {
    return JSON.parse(JSON.stringify(memoryCache));
  }
  // 2. Try /tmp/hive-data.json (fast path for warm invocations)
  const fs = await import('fs/promises');
  try {
    const data = await fs.readFile(HIVE_PATH, 'utf8');
    const parsed = JSON.parse(data);
    normalizeData(parsed);
    memoryCache = parsed;
    memoryCacheTime = Date.now();
    return JSON.parse(JSON.stringify(parsed));
  } catch { /* cold start — fall through to GitHub */ }
  // 3. Fall back to GitHub raw content
  try {
    const response = await fetch(`https://raw.githubusercontent.com/${GITHUB_OWNER}/${GITHUB_REPO}/${GITHUB_BRANCH}/${GITHUB_PATH}`, {
      signal: AbortSignal.timeout(8000)
    });
    if (response.ok) {
      const text = await response.text();
      const parsed = JSON.parse(text);
      normalizeData(parsed);
      // Write to /tmp for warm invocations later
      try {
        await fs.writeFile(HIVE_PATH, JSON.stringify(parsed, null, 2), 'utf8');
      } catch {}
      memoryCache = parsed;
      memoryCacheTime = Date.now();
      return JSON.parse(JSON.stringify(parsed));
    }
  } catch { /* GitHub unavailable — return default */ }
  // 4. Return default empty structure
  const defaults = { portfolios: {}, priceCache: {}, accounts: {} };
  memoryCache = defaults;
  memoryCacheTime = Date.now();
  return JSON.parse(JSON.stringify(defaults));
}

// Normalize holdings format: convert {ticker: {shares, price, value}} → {ticker: share_count}
function normalizeData(data) {
  // Ensure required keys always exist
  if (!data.portfolios) data.portfolios = {};
  if (!data.priceCache) data.priceCache = {};
  if (!data.accounts) data.accounts = {};
  for (const uid of Object.keys(data.portfolios)) {
    const p = data.portfolios[uid];
    const h = p.holdings;
    if (!h) continue;
    // Check if holdings are in old nested format
    const keys = Object.keys(h);
    if (keys.length > 0 && typeof h[keys[0]] === 'object' && h[keys[0]] !== null && 'shares' in h[keys[0]]) {
      const flat = {};
      for (const [ticker, obj] of Object.entries(h)) {
        flat[ticker] = obj.shares || 0;
      }
      p.holdings = flat;
    }
  }
}

async function writeData(data) {
  const fs = await import('fs/promises');
  // 1. Always write to /tmp for warm invocations
  try {
    await fs.writeFile(HIVE_PATH, JSON.stringify(data, null, 2), 'utf8');
  } catch {}
  // 2. Update in-memory cache
  memoryCache = data;
  memoryCacheTime = Date.now();
  // 3. Async push to GitHub (fire-and-forget — never block the response)
  githubPush(data).catch(err => console.error('GitHub push failed:', err.message));
}

async function githubPush(data) {
  const url = `https://api.github.com/repos/${GITHUB_OWNER}/${GITHUB_REPO}/contents/${GITHUB_PATH}`;
  const content = Buffer.from(JSON.stringify(data, null, 2)).toString('base64');

  // First try to get the current file to obtain its SHA
  let sha = null;
  try {
    const getResp = await fetch(url, {
      headers: { 'Authorization': `token ${GITHUB_TOKEN}` },
      signal: AbortSignal.timeout(8000)
    });
    if (getResp.ok) {
      const fileInfo = await getResp.json();
      sha = fileInfo.sha;
    }
  } catch { /* file may not exist yet, continue without SHA */ }

  // PUT the updated content
  const body = {
    message: 'Update hive data',
    content,
    branch: GITHUB_BRANCH
  };
  if (sha) body.sha = sha;

  const putResp = await fetch(url, {
    method: 'PUT',
    headers: {
      'Authorization': `token ${GITHUB_TOKEN}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(body),
    signal: AbortSignal.timeout(10000)
  });

  if (!putResp.ok) {
    const errText = await putResp.text();
    console.error(`GitHub push failed (${putResp.status}):`, errText.slice(0, 200));
  }
}

async function fetchPrice(ticker) {
  try {
    const url = `https://readthesignal.net/api/prices?ticker=${ticker}`;
    const resp = await fetch(url, { signal: AbortSignal.timeout(5000) });
    if (!resp.ok) return null;
    const data = await resp.json();
    return data.price || null;
  } catch {
    return null;
  }
}

async function getCurrentPrice(ticker, data) {
  if (data.priceCache[ticker] && data.priceCache[ticker].price) {
    const age = Date.now() - new Date(data.priceCache[ticker].updatedAt).getTime();
    if (age < 300000) return data.priceCache[ticker].price;
  }
  const price = await fetchPrice(ticker);
  if (price) {
    data.priceCache[ticker] = { price, updatedAt: new Date().toISOString() };
  }
  return price;
}

async function getPricesForTickers(tickers, data) {
  const prices = {};
  for (const t of tickers) {
    const p = await getCurrentPrice(t, data);
    if (p) prices[t] = p;
  }
  return prices;
}

function calcPortfolioValue(portfolio, prices) {
  let holdingsValue = 0;
  for (const [ticker, shares] of Object.entries(portfolio.holdings || {})) {
    const price = prices[ticker] || 0;
    holdingsValue += shares * price;
  }
  return (portfolio.cash || 0) + holdingsValue;
}

function calcReturn(currentValue) {
  return ((currentValue - INITIAL_CASH) / INITIAL_CASH) * 100;
}

function getCoverageUniverseList() {
  return Array.from(COVERAGE_UNIVERSE);
}

function hashPassword(password) {
  return crypto.createHash('sha256').update(password).digest('hex');
}

// === Stateless token system ===
// Tokens are HMAC-signed payloads: no server-side session storage needed
// Format: tok_<base64url(username)>=<base64url(expiresAt_epoch)>=<hex_signature>
const TOKEN_DURATION_MS = 7 * 24 * 60 * 60 * 1000; // 7 days

function toBase64Url(str) {
  return Buffer.from(str).toString('base64url');
}

function fromBase64Url(str) {
  return Buffer.from(str, 'base64url').toString();
}

function generateToken(username) {
  const expiresAt = Date.now() + TOKEN_DURATION_MS;
  const payload = toBase64Url(username) + '.' + toBase64Url(String(expiresAt));
  const sig = crypto.createHmac('sha256', SERVER_SECRET).update(payload).digest('hex').slice(0, 24);
  return 'tok_' + payload + '.' + sig;
}

function verifyToken(token) {
  if (!token || typeof token !== 'string') return null;
  if (!token.startsWith('tok_')) return null;
  const rest = token.slice(4);
  const parts = rest.split('.');
  if (parts.length !== 3) return null;
  const [b64User, b64Expires, sig] = parts;
  const payload = b64User + '.' + b64Expires;
  const expectedSig = crypto.createHmac('sha256', SERVER_SECRET).update(payload).digest('hex').slice(0, 24);
  if (sig !== expectedSig) {
    return null; // Token tampered
  }
  const username = fromBase64Url(b64User);
  const expiresAt = parseInt(fromBase64Url(b64Expires), 10);
  if (Date.now() > expiresAt) {
    return null; // Token expired
  }
  return username;
}

function getAccountFromToken(data, token) {
  const username = verifyToken(token);
  if (!username) return null;
  const account = data.accounts[username];
  return account || null;
}

function resolveUidFromToken(data, token) {
  const account = getAccountFromToken(data, token);
  return account ? account.uid : null;
}

export default async function handler(req, res) {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

  if (req.method === 'OPTIONS') return res.status(200).end();

  try {
    const data = await readData();

    // Helper: resolve token → uid (from query or body)
    function resolveUid(req) {
      const token = req.query.token || (req.body && req.body.token) || req.query.uid;
      if (token && token.startsWith('tok_')) {
        const uid = resolveUidFromToken(data, token);
        if (uid) return uid;
      }
      return req.query.uid || (req.body && req.body.uid) || null;
    }

    // === Auth endpoints ===

    // POST /api/hive?action=register
    if (req.method === 'POST' && req.query.action === 'register') {
      const { username, password, displayName } = req.body || {};
      if (!username || !password) {
        return res.status(400).json({ error: 'Username and password are required' });
      }
      const usernameLower = username.toLowerCase().trim();
      if (usernameLower.length < 3) {
        return res.status(400).json({ error: 'Username must be at least 3 characters' });
      }
      if (password.length < 6) {
        return res.status(400).json({ error: 'Password must be at least 6 characters' });
      }
      if (data.accounts[usernameLower]) {
        return res.status(409).json({ error: 'Username already taken' });
      }
      const uid = 'usr_' + crypto.createHash('sha256').update(usernameLower).digest('hex').slice(0, 16);
      const account = {
        username: usernameLower,
        displayName: displayName || username,
        passwordHash: hashPassword(password),
        createdAt: GAME_START,
        uid
      };
      data.accounts[usernameLower] = account;
      // Ensure portfolio exists
      if (!data.portfolios[uid]) {
        data.portfolios[uid] = {
          uid,
          displayName: account.displayName,
          photoURL: null,
          cash: INITIAL_CASH,
          holdings: {},
          trades: [],
          createdAt: new Date().toISOString()
        };
      }
      await writeData(data);
      const token = generateToken(usernameLower);
      return res.json({
        status: 'ok',
        token,
        user: { uid, displayName: account.displayName, username: usernameLower }
      });
    }

    // POST /api/hive?action=login
    if (req.method === 'POST' && req.query.action === 'login') {
      const { username, password } = req.body || {};
      if (!username || !password) {
        return res.status(400).json({ error: 'Username and password are required' });
      }
      const usernameLower = username.toLowerCase().trim();
      const account = data.accounts[usernameLower];
      if (!account || account.passwordHash !== hashPassword(password)) {
        return res.status(401).json({ error: 'Invalid username or password' });
      }
      const token = generateToken(usernameLower);
      return res.json({
        status: 'ok',
        token,
        user: { uid: account.uid, displayName: account.displayName, username: usernameLower }
      });
    }

    // GET /api/hive?action=me&token=X
    if (req.method === 'GET' && req.query.action === 'me') {
      const token = req.query.token;
      const account = getAccountFromToken(data, token);
      if (!account) {
        return res.json({ authenticated: false });
      }
      return res.json({
        authenticated: true,
        uid: account.uid,
        displayName: account.displayName,
        username: account.username,
        createdAt: account.createdAt,
        isPremium: !!account.isPremium,
        premiumPlan: account.premiumPlan || null,
        email: account.email || null
      });
    }

    // POST /api/hive?action=set-premium — called by Stripe webhook with ADMIN_KEY
    if (req.method === 'POST' && req.query.action === 'set-premium') {
      const adminKey = req.query.admin_key || (req.body && req.body.admin_key);
      if (adminKey !== process.env.ADMIN_KEY) {
        return res.status(403).json({ error: 'Forbidden' });
      }
      const { email, plan, customerId, subscriptionId } = req.body && req.body.admin_key ? req.body : (req.query.admin_key ? req.body : {}) || {};
      if (!email || !customerId) {
        return res.status(400).json({ error: 'Email and customerId required' });
      }
      const emailLower = email.toLowerCase().trim();
      // Find account by email or username
      let targetAccount = null;
      let targetUsername = null;
      for (const [uname, acct] of Object.entries(data.accounts)) {
        if (acct.email && acct.email.toLowerCase() === emailLower) {
          targetAccount = acct;
          targetUsername = uname;
          break;
        }
        if (uname === emailLower) {
          targetAccount = acct;
          targetUsername = uname;
          break;
        }
      }
      if (!targetAccount) {
        return res.status(404).json({ error: 'No account found for email: ' + email });
      }
      targetAccount.isPremium = true;
      targetAccount.premiumPlan = plan || 'premium';
      targetAccount.stripeCustomerId = customerId;
      targetAccount.stripeSubscriptionId = subscriptionId;
      targetAccount.premiumSince = new Date().toISOString();
      await writeData(data);
      console.log(`Premium activated: ${email} -> ${plan}`);
      return res.json({ status: 'ok', message: `Premium activated for ${email}` });
    }

    // POST /api/hive?action=cancel-premium — called by Stripe webhook on subscription delete
    if (req.method === 'POST' && req.query.action === 'cancel-premium') {
      const adminKey = req.query.admin_key || (req.body && req.body.admin_key);
      if (adminKey !== process.env.ADMIN_KEY) {
        return res.status(403).json({ error: 'Forbidden' });
      }
      const { customerId } = req.body && req.body.admin_key ? req.body : (req.query.admin_key ? req.body : {}) || {};
      if (!customerId) {
        return res.status(400).json({ error: 'customerId required' });
      }
      for (const [uname, acct] of Object.entries(data.accounts)) {
        if (acct.stripeCustomerId === customerId) {
          acct.isPremium = false;
          acct.stripeSubscriptionId = null;
          console.log(`Premium canceled: ${uname} (${customerId})`);
          break;
        }
      }
      await writeData(data);
      return res.json({ status: 'ok' });
    }

    // POST /api/hive?action=google-auth
    if (req.method === 'POST' && req.query.action === 'google-auth') {
      const { credential } = req.body || {};
      if (!credential) {
        return res.status(400).json({ error: 'Google credential required' });
      }
      let googleUser;
      try {
        const verifyUrl = `https://oauth2.googleapis.com/tokeninfo?id_token=${credential}`;
        const verifyResp = await fetch(verifyUrl, { signal: AbortSignal.timeout(5000) });
        if (!verifyResp.ok) {
          return res.status(401).json({ error: 'Invalid Google credential' });
        }
        googleUser = await verifyResp.json();
      } catch (err) {
        return res.status(502).json({ error: 'Failed to verify Google credential' });
      }

      const googleId = googleUser.sub;
      const email = googleUser.email || '';
      const googleName = googleUser.name || email.split('@')[0] || 'Google User';
      const photo = googleUser.picture || null;
      const googleUsername = 'google_' + googleId;

      let account = data.accounts[googleUsername];
      if (!account) {
        const uid = 'usr_' + crypto.createHash('sha256').update(googleUsername).digest('hex').slice(0, 16);
        account = {
          username: googleUsername,
          displayName: googleName,
          passwordHash: '',
          createdAt: GAME_START,
          uid,
          googleId,
          email,
          photoURL: photo
        };
        data.accounts[googleUsername] = account;
        data.portfolios[uid] = {
          uid,
          displayName: googleName,
          photoURL: photo,
          cash: INITIAL_CASH,
          holdings: {},
          trades: [],
          createdAt: new Date().toISOString()
        };
      } else {
        account.displayName = googleName;
        if (photo) account.photoURL = photo;
        if (data.portfolios[account.uid]) {
          data.portfolios[account.uid].displayName = googleName;
          data.portfolios[account.uid].photoURL = photo;
        }
      }

      await writeData(data);
      const token = generateToken(googleUsername);
      return res.json({
        status: 'ok',
        token,
        user: { uid: account.uid, displayName: account.displayName, username: googleUsername, photoURL: photo }
      });
    }

    // === GET /api/hive?meta ===
    if (req.method === 'GET' && req.query.meta === 'true') {
      const portfolios = Object.values(data.portfolios);
      const allTickers = new Set();
      for (const p of portfolios) {
        if (p.holdings) Object.keys(p.holdings).forEach(t => allTickers.add(t));
      }
      const prices = await getPricesForTickers(Array.from(allTickers), data);
      await writeData(data);

      let totalValue = 0;
      let topGainer = null;
      let topLoser = null;
      let bestReturn = -Infinity;
      let worstReturn = Infinity;

      for (const p of portfolios) {
        const val = calcPortfolioValue(p, prices);
        const ret = calcReturn(val);
        totalValue += val;
        if (ret > bestReturn) { bestReturn = ret; topGainer = p; }
        if (ret < worstReturn) { worstReturn = ret; topLoser = p; }
      }

      const stocksList = getCoverageUniverseList().map(t => ({
        ticker: t,
        name: (COMPANY_INFO[t] || {}).name || t,
        sector: (COMPANY_INFO[t] || {}).sector || 'Other'
      }));

      return res.json({
        totalUsers: portfolios.length,
        totalTrades: portfolios.reduce((s, p) => s + (p.trades || []).length, 0),
        totalPortfolioValue: totalValue,
        averageReturn: portfolios.length ? calcReturn(totalValue / portfolios.length) : 0,
        topGainer: topGainer ? { uid: topGainer.uid, displayName: topGainer.displayName, return: bestReturn } : null,
        topLoser: topLoser ? { uid: topLoser.uid, displayName: topLoser.displayName, return: worstReturn } : null,
        coverageUniverse: stocksList
      });
    }

    // === GET /api/hive?stocks=true ===
    if (req.method === 'GET' && req.query.stocks === 'true') {
      const allTickers = Array.from(COVERAGE_UNIVERSE);
      const stocksList = allTickers.map(t => ({
        ticker: t,
        name: (COMPANY_INFO[t] || {}).name || t,
        sector: (COMPANY_INFO[t] || {}).sector || 'Other'
      }));

      return res.json({
        stocks: stocksList
      });
    }

    // === GET /api/hive?leaderboard=XXX ===
    if (req.method === 'GET' && req.query.leaderboard) {
      const period = req.query.leaderboard;
      const portfolios = Object.values(data.portfolios);
      const allTickers = new Set();
      for (const p of portfolios) {
        if (p.holdings) Object.keys(p.holdings).forEach(t => allTickers.add(t));
      }
      const prices = await getPricesForTickers(Array.from(allTickers), data);
      await writeData(data);

      const now = new Date();
      const periodMs = period === 'weekly' ? 7 * 24 * 60 * 60 * 1000 :
                       period === 'monthly' ? 30 * 24 * 60 * 60 * 1000 : null;

      const entries = portfolios.map(p => {
        const currentValue = calcPortfolioValue(p, prices);

        if (!periodMs) {
          // All-time: compare to initial cash
          const ret = calcReturn(currentValue);
          return {
            uid: p.uid,
            displayName: p.displayName || 'Anonymous',
            photoURL: p.photoURL || null,
            cash: p.cash,
            holdings: p.holdings,
            value: Math.round(currentValue * 100) / 100,
            return: Math.round(ret * 100) / 100,
            trades: (p.trades || []).length,
            createdAt: GAME_START
          };
        }

        // Weekly/Monthly: reconstruct portfolio at period start
        const cutoff = new Date(now.getTime() - periodMs);
        const trades = p.trades || [];
        const periodTrades = trades.filter(t => new Date(t.date) >= cutoff);

        // Start from current state, undo period trades to get period-start state
        let startCash = p.cash || 0;
        const startHoldings = { ...(p.holdings || {}) };

        for (const t of [...periodTrades].reverse()) {
          if (t.action === 'buy') {
            startCash += t.shares * t.price;
            startHoldings[t.ticker] = (startHoldings[t.ticker] || 0) - t.shares;
            if (startHoldings[t.ticker] <= 0) delete startHoldings[t.ticker];
          } else if (t.action === 'sell') {
            startCash -= t.shares * t.price;
            startHoldings[t.ticker] = (startHoldings[t.ticker] || 0) + t.shares;
          }
        }

        // Calculate start value at current prices (best approximation without historical prices)
        let startHoldingsValue = 0;
        for (const [ticker, shares] of Object.entries(startHoldings)) {
          if (shares > 0) {
            startHoldingsValue += shares * (prices[ticker] || 0);
          }
        }
        const startValue = startCash + startHoldingsValue;

        // Period return
        const periodReturn = startValue > 0
          ? ((currentValue - startValue) / startValue) * 100
          : 0;

        return {
          uid: p.uid,
          displayName: p.displayName || 'Anonymous',
          photoURL: p.photoURL || null,
          cash: p.cash,
          holdings: p.holdings,
          value: Math.round(currentValue * 100) / 100,
          return: Math.round(periodReturn * 100) / 100,
          trades: periodTrades.length,
          createdAt: GAME_START
        };
      });

      entries.sort((a, b) => b.return - a.return);
      const top50 = entries.slice(0, 50).map((e, i) => ({ rank: i + 1, ...e }));

      return res.json({ period, leaderboard: top50, totalParticipants: portfolios.length });
    }

    // === GET /api/hive?signal-master ===
    if (req.method === 'GET' && req.query['signal-master'] === 'true') {
      const portfolios = Object.values(data.portfolios);
      if (portfolios.length === 0) {
        return res.json({ holdings: {}, topHoldings: [], totalPortfolios: 0 });
      }

      const allTickers = new Set();
      for (const p of portfolios) {
        if (p.holdings) Object.keys(p.holdings).forEach(t => allTickers.add(t));
      }
      const prices = await getPricesForTickers(Array.from(allTickers), data);
      await writeData(data);

      const ranked = portfolios.map(p => ({
        ...p,
        value: calcPortfolioValue(p, prices),
        ret: calcReturn(calcPortfolioValue(p, prices))
      }));
      ranked.sort((a, b) => b.ret - a.ret);

      const topCount = Math.max(1, Math.ceil(ranked.length * 0.1));
      const topPortfolios = ranked.slice(0, topCount);

      const aggregated = {};
      let totalAggValue = 0;
      for (const p of topPortfolios) {
        for (const [ticker, shares] of Object.entries(p.holdings || {})) {
          const price = prices[ticker] || 0;
          const val = shares * price;
          aggregated[ticker] = (aggregated[ticker] || 0) + val;
          totalAggValue += val;
        }
      }

      const topHoldings = Object.entries(aggregated)
        .map(([ticker, value]) => ({
          ticker,
          value: Math.round(value * 100) / 100,
          allocation: totalAggValue > 0 ? Math.round((value / totalAggValue) * 10000) / 100 : 0,
          price: prices[ticker] || 0
        }))
        .sort((a, b) => b.allocation - a.allocation);

      return res.json({
        holdings: topHoldings,
        totalPortfolios: topPortfolios.length,
        totalAggValue: Math.round(totalAggValue * 100) / 100,
        topCount
      });
    }

    // === GET /api/hive?uid=XXX (or ?token=XXX) ===
    if (req.method === 'GET' && (req.query.uid || req.query.token)) {
      const uid = resolveUid(req);
      if (!uid) {
        return res.status(400).json({ error: 'User ID or valid token required' });
      }
      let portfolio = data.portfolios[uid];

      if (!portfolio) {
        portfolio = {
          uid,
          displayName: req.query.displayName || 'Anonymous',
          photoURL: req.query.photoURL || null,
          cash: INITIAL_CASH,
          holdings: {},
          trades: [],
          createdAt: new Date().toISOString()
        };
        data.portfolios[uid] = portfolio;
        await writeData(data);
      }

      if (req.query.displayName) portfolio.displayName = req.query.displayName;
      if (req.query.photoURL) portfolio.photoURL = req.query.photoURL;
      await writeData(data);

      const tickers = Object.keys(portfolio.holdings || {});
      const prices = await getPricesForTickers(tickers, data);
      await writeData(data);

      const holdingsWithPrices = {};
      let totalHoldingsValue = 0;
      for (const [ticker, shares] of Object.entries(portfolio.holdings || {})) {
        const price = prices[ticker] || 0;
        const value = shares * price;
        holdingsWithPrices[ticker] = { shares, price, value: Math.round(value * 100) / 100 };
        totalHoldingsValue += value;
      }

      const totalValue = portfolio.cash + totalHoldingsValue;
      const pctReturn = calcReturn(totalValue);

      return res.json({
        uid: portfolio.uid,
        displayName: portfolio.displayName,
        photoURL: portfolio.photoURL,
        cash: portfolio.cash,
        holdings: holdingsWithPrices,
        totalHoldingsValue: Math.round(totalHoldingsValue * 100) / 100,
        totalValue: Math.round(totalValue * 100) / 100,
        return: Math.round(pctReturn * 100) / 100,
        trades: portfolio.trades.slice(-50).reverse(),
        createdAt: portfolio.createdAt
      });
    }

    // === POST /api/hive (submit trade) ===
    if (req.method === 'POST') {
      const uid = resolveUid(req);
      const { ticker, action, shares } = req.body || {};

      if (!uid) {
        return res.status(400).json({ error: 'Authentication required — provide uid or token' });
      }
      if (!ticker || !action || !shares) {
        return res.status(400).json({ error: 'Missing required fields: ticker, action, shares' });
      }

      const tickerUpper = ticker.toUpperCase();
      if (!COVERAGE_UNIVERSE.has(tickerUpper)) {
        return res.status(400).json({ error: `Ticker ${tickerUpper} is not in our coverage universe` });
      }

      if (!['buy', 'sell'].includes(action)) {
        return res.status(400).json({ error: 'Action must be "buy" or "sell"' });
      }

      const numShares = parseInt(shares, 10);
      if (isNaN(numShares) || numShares <= 0) {
        return res.status(400).json({ error: 'Shares must be a positive integer' });
      }

      let portfolio = data.portfolios[uid];
      if (!portfolio) {
        portfolio = {
          uid,
          displayName: req.body.displayName || 'Anonymous',
          photoURL: req.body.photoURL || null,
          cash: INITIAL_CASH,
          holdings: {},
          trades: [],
          createdAt: new Date().toISOString()
        };
        data.portfolios[uid] = portfolio;
      }

      if (req.body.displayName) portfolio.displayName = req.body.displayName;
      if (req.body.photoURL) portfolio.photoURL = req.body.photoURL;

      const price = await getCurrentPrice(tickerUpper, data);
      if (!price) {
        return res.status(503).json({ error: `Unable to fetch price for ${tickerUpper}` });
      }

      const currentHoldings = { ...portfolio.holdings };
      const currentCash = portfolio.cash;
      const currentHoldingShares = currentHoldings[tickerUpper] || 0;

      if (action === 'buy') {
        const cost = price * numShares;
        if (cost > currentCash) {
          return res.status(400).json({ error: `Insufficient cash. Need $${cost.toFixed(2)}, have $${currentCash.toFixed(2)}` });
        }

        const newHoldings = { ...currentHoldings, [tickerUpper]: currentHoldingShares + numShares };
        const tempPrices = await getPricesForTickers(Object.keys(newHoldings), data);
        tempPrices[tickerUpper] = price;
        const totalVal = calcPortfolioValue({ cash: currentCash - cost, holdings: newHoldings }, tempPrices);
        const tickerVal = (currentHoldingShares + numShares) * price;
        const alloc = tickerVal / totalVal;

        if (alloc > MAX_ALLOCATION) {
          return res.status(400).json({ error: `Maximum 40% allocation per ticker. Current would be ${(alloc * 100).toFixed(1)}%` });
        }

        const uniqueTickers = Object.keys(newHoldings).filter(t => newHoldings[t] > 0).length;
        if (uniqueTickers > MAX_STOCKS) {
          return res.status(400).json({ error: `Maximum ${MAX_STOCKS} unique stocks per portfolio` });
        }

        portfolio.cash = currentCash - cost;
        portfolio.holdings = newHoldings;
      } else {
        if (currentHoldingShares < numShares) {
          return res.status(400).json({ error: `Not enough shares. You have ${currentHoldingShares} shares of ${tickerUpper}` });
        }

        const newHoldings = { ...currentHoldings };
        newHoldings[tickerUpper] = currentHoldingShares - numShares;
        if (newHoldings[tickerUpper] <= 0) delete newHoldings[tickerUpper];

        const uniqueTickers = Object.keys(newHoldings).filter(t => newHoldings[t] > 0).length;
        if (uniqueTickers > 0 && uniqueTickers < MIN_STOCKS) {
          return res.status(400).json({ error: `Minimum ${MIN_STOCKS} unique stocks required` });
        }

        const proceeds = price * numShares;
        portfolio.cash = currentCash + proceeds;
        portfolio.holdings = newHoldings;
      }

      portfolio.trades.push({
        ticker: tickerUpper,
        action,
        shares: numShares,
        price: Math.round(price * 100) / 100,
        date: new Date().toISOString()
      });

      await writeData(data);

      return res.json({
        status: 'success',
        trade: { ticker: tickerUpper, action, shares: numShares, price: Math.round(price * 100) / 100 },
        cash: Math.round(portfolio.cash * 100) / 100,
        holdings: portfolio.holdings
      });
    }

    return res.status(405).json({ error: 'Method not allowed' });

  } catch (err) {
    console.error('Hive error:', err);
    return res.status(500).json({ error: 'Something went wrong', detail: err.message || String(err) });
  }
}
